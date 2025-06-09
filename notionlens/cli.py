import os
import subprocess
import sys
import click
from pyfiglet import Figlet
from .config import load_config, save_config
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
    log_path = os.path.expanduser("~/.notionlens/notionlens.log")
    os.makedirs(os.path.dirname(log_path), exist_ok=True)
    with open(log_path, "a") as log_file:
        proc = subprocess.Popen(
            cmd,
            stdout=log_file,
            stderr=log_file,
            preexec_fn=os.setsid,
        )
    click.echo(f"NotionLens started in background with PID {proc.pid}")
    click.echo("Find this PID in Activity Monitor to manage the process.")

@cli.command(hidden=True)
def capture():
    """Internal command used for the background process."""
    capture_loop()

