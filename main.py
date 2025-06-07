import subprocess
import os
import time
from datetime import datetime
import requests # type: ignore
from dotenv import load_dotenv # type: ignore
import tempfile

# Load environment variables from .env file
load_dotenv()

# Get secrets securely
NOTION_API_KEY = os.getenv("NOTION_API_KEY")
DATABASE_ID = os.getenv("DATABASE_ID")
S3_UPLOAD_URL = os.getenv("S3_UPLOAD_URL")  # e.g. https://bucket.s3.amazonaws.com/

# Notion API endpoint
NOTION_API_URL = "https://api.notion.com/v1/pages"

# Interval in minutes
run_interval = 1

def retry_request(func, retries=3, delay=5):
    for attempt in range(retries):
        try:
            return func()
        except Exception as e:
            print(f"Attempt {attempt + 1} failed: {e}")
            time.sleep(delay)
    print("All retries failed.")
    return None

while True:
    # Generate timestamped screenshot name
    timestamp = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    screenshot_filename = f"screenshot_{timestamp}.png"
    temp_dir = tempfile.gettempdir()
    screenshot_path = os.path.join(temp_dir, screenshot_filename)

    # Take screenshot
    subprocess.run(["screencapture", "-x", screenshot_path])
    print(f"✅ Screenshot saved: {screenshot_path}")

    # S3 upload
    s3_url = f"{S3_UPLOAD_URL}{screenshot_filename}"

    def upload_to_s3():
        with open(screenshot_path, "rb") as file:
            response = requests.put(s3_url, data=file, headers={"Content-Type": "image/png"})
            response.raise_for_status()
            print("✅ Uploaded to S3")
    
    if not retry_request(upload_to_s3):
        continue

    # Notion API headers and payload
    headers = {
        "Authorization": f"Bearer {NOTION_API_KEY}",
        "Content-Type": "application/json",
        "Notion-Version": "2022-06-28"
    }

    payload = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {
                "title": [{"text": {"content": timestamp}}]
            },
            "Image": {
                "files": [{
                    "name": "Screenshot",
                    "type": "external",
                    "external": {"url": s3_url}
                }]
            },
            "Date": {
                "date": {"start": datetime.now().isoformat()}
            }
        }
    }

    def upload_to_notion():
        response = requests.post(NOTION_API_URL, headers=headers, json=payload)
        response.raise_for_status()
        print("✅ Uploaded to Notion")

    if not retry_request(upload_to_notion):
        continue

    # Delete local screenshot
    try:
        os.remove(screenshot_path)
        print(f"🧹 Deleted local screenshot: {screenshot_path}")
    except OSError as e:
        print(f"⚠️ Could not delete screenshot: {e}")

    print(f"⏳ Waiting {run_interval} minute(s)...\n")
    time.sleep(run_interval * 60)