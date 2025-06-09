import os
import subprocess
import sys
import click
from pyfiglet import Figlet
from .config import load_config, save_config, LOG_PATH, CONFIG_DIR
from .capture import capture_loop

@click.group()
def cli():
    """NotionLens command line interface."""
    pass

@cli.command()
def setup():
    """Interactively set up configuration."""
    fig = Figlet(font="slant")
    click.echo(fig.renderText("NotionLens"))
    cfg = load_config()
    cfg["notion_api_key"] = click.prompt("Notion API Key", default=cfg.get("notion_api_key", ""), hide_input=True)
    cfg["database_id"] = click.prompt("Notion Database ID", default=cfg.get("database_id", ""))
    cfg["s3_upload_url"] = click.prompt("S3 Upload Base URL", default=cfg.get("s3_upload_url", ""))
    cfg["interval"] = click.prompt("Capture interval (minutes)", default=cfg.get("interval", 1), type=int)
    save_config(cfg)
    click.echo("Configuration saved to ~/.notionlens/config.json")

@cli.command()
def start():
    """Start capturing screenshots as a background process."""
    cmd = [sys.executable, "-m", "notionlens", "capture"]
    CONFIG_DIR.mkdir(parents=True, exist_ok=True)
    log_handle = open(LOG_PATH, "a")
    subprocess.Popen(cmd, stdout=log_handle, stderr=log_handle, preexec_fn=os.setsid)
    click.echo(f"NotionLens started in background. Logs: {LOG_PATH}")

@cli.command(hidden=True)
def capture():
    """Internal command used for the background process."""
    capture_loop()

