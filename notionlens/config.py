import json
import os
from pathlib import Path

CONFIG_DIR = Path.home() / ".notionlens"
CONFIG_PATH = CONFIG_DIR / "config.json"
LOG_PATH = CONFIG_DIR / "notionlens.log"
PID_PATH = CONFIG_DIR / "notionlens.pid"

DEFAULT_CONFIG = {
    "notion_api_key": "",
    "database_id": "",
    "s3_upload_url": "",
    "interval": 1
}

def load_config():
    if CONFIG_PATH.exists():
        with open(CONFIG_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    else:
        return DEFAULT_CONFIG.copy()

def save_config(config):
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    with open(CONFIG_PATH, "w", encoding="utf-8") as f:
        json.dump(config, f, indent=2)

