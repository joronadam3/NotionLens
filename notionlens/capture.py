import os
import subprocess
import time
from datetime import datetime
import requests
import tempfile
import logging
from .config import load_config, LOG_PATH, CONFIG_DIR

NOTION_API_URL = "https://api.notion.com/v1/pages"


def retry_request(func, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            logging.error(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    logging.error("All retries failed")
    return None


def get_display_count():
    """Return the number of connected displays on macOS."""
    try:
        out = subprocess.check_output(
            [
                "osascript",
                "-e",
                'tell application "System Events" to count of desktops',
            ]
        )
        return int(out.strip())
    except Exception as e:
        logging.error(f"Could not determine display count: {e}")
        return 1


def capture_loop():
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format="%(asctime)s [%(levelname)s] %(message)s",
    )
    logging.info("Capture loop started")

    cfg = load_config()
    run_interval = cfg.get("interval", 1)
    notion_api_key = cfg.get("notion_api_key")
    database_id = cfg.get("database_id")
    s3_base_url = cfg.get("s3_upload_url")

    while True:
        timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        temp_dir = tempfile.gettempdir()
        display_count = get_display_count()

        for display in range(1, display_count + 1):
            screenshot_filename = f"screenshot_{timestamp}_screen{display}.png"
            screenshot_path = os.path.join(temp_dir, screenshot_filename)

            result = subprocess.run([
                "screencapture",
                "-x",
                "-D",
                str(display),
                screenshot_path,
            ])
            if result.returncode != 0:
                logging.error(
                    "Screen capture failed. Ensure the terminal has Screen Recording permission."
                )
                continue
            logging.info(f"Screenshot saved: {screenshot_path}")

            s3_url = f"{s3_base_url}{screenshot_filename}"

            def upload_to_s3():
                with open(screenshot_path, "rb") as file:
                    resp = requests.put(
                        s3_url, data=file, headers={"Content-Type": "image/png"}
                    )
                    resp.raise_for_status()
                    logging.info("Uploaded to S3")
                    return True

            def upload_to_notion():
                headers = {
                    "Authorization": f"Bearer {notion_api_key}",
                    "Content-Type": "application/json",
                    "Notion-Version": "2022-06-28",
                }
                payload = {
                    "parent": {"database_id": database_id},
                    "properties": {
                        "Name": {
                            "title": [
                                {"text": {"content": f"{timestamp} screen {display}"}}
                            ]
                        },
                        "Image": {
                            "files": [
                                {
                                    "name": f"Screenshot {display}",
                                    "type": "external",
                                    "external": {"url": s3_url},
                                }
                            ]
                        },
                    },
                }
                resp = requests.post(NOTION_API_URL, headers=headers, json=payload)
                resp.raise_for_status()
                logging.info("Uploaded to Notion")

            if retry_request(upload_to_s3):
                retry_request(upload_to_notion)

            try:
                os.remove(screenshot_path)
            except OSError as e:
                logging.error(f"Could not delete screenshot: {e}")

        logging.info(f"Waiting {run_interval} minute(s)...")
        time.sleep(run_interval * 60)
