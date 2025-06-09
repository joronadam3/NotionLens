import os
import subprocess
import time
from datetime import datetime
import requests
import tempfile
from .config import load_config

NOTION_API_URL = "https://api.notion.com/v1/pages"


def retry_request(func, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    print("All retries failed")
    return None


def capture_once(cfg=None):
    """Capture a single screenshot and upload it."""
    cfg = cfg or load_config()
    notion_api_key = cfg.get("notion_api_key")
    database_id = cfg.get("database_id")
    s3_base_url = cfg.get("s3_upload_url")

    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_filename = f"screenshot_{timestamp}.png"
    temp_dir = tempfile.gettempdir()
    screenshot_path = os.path.join(temp_dir, screenshot_filename)

    subprocess.run(["screencapture", "-x", screenshot_path], check=True)
    print(f"Screenshot saved: {screenshot_path}")

    s3_url = f"{s3_base_url}{screenshot_filename}"

    def upload_to_s3():
        with open(screenshot_path, "rb") as file:
            resp = requests.put(s3_url, data=file, headers={"Content-Type": "image/png"})
            resp.raise_for_status()
            print("Uploaded to S3")
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
                "Name": {"title": [{"text": {"content": timestamp}}]},
                "Image": {
                    "files": [
                        {
                            "name": "Screenshot",
                            "type": "external",
                            "external": {"url": s3_url},
                        }
                    ]
                },
            },
        }
        resp = requests.post(NOTION_API_URL, headers=headers, json=payload)
        resp.raise_for_status()
        print("Uploaded to Notion")
        return True

    try:
        if retry_request(upload_to_s3) and retry_request(upload_to_notion):
            return True
        raise RuntimeError("Upload retries exhausted")
    finally:
        try:
            os.remove(screenshot_path)
        except OSError as e:
            print(f"Could not delete screenshot: {e}")


def capture_loop():
    cfg = load_config()
    run_interval = cfg.get("interval", 1)

    while True:
        capture_once(cfg)
        print(f"Waiting {run_interval} minute(s)...\n")
        time.sleep(run_interval * 60)
