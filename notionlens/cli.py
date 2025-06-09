import os
import subprocess
import sys
import click
from .config import load_config, save_config
from .capture import capture_loop

@click.group()
def cli():
    """NotionLens command line interface."""
    pass

@cli.command()
def setup():
    """Interactively set up configuration."""
    try:
        from pyfiglet import Figlet
        fig = Figlet(font="slant")
        click.echo(fig.renderText("NotionLens"))
    except ImportError:
        pass
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
    subprocess.Popen(cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, preexec_fn=os.setsid)
    click.echo("NotionLens started in background")

@cli.command(hidden=True)
def capture():
    """Internal command used for the background process."""
    capture_loop()

