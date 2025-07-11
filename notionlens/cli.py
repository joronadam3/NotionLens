import os
import subprocess
import sys
import signal
import click
from pyfiglet import Figlet
from .config import load_config, save_config, LOG_PATH, CONFIG_DIR, PID_PATH
from .capture import capture_loop


def _get_error_logs(limit: int = 5):
    """Return the last error lines from the log file."""
    if not LOG_PATH.exists():
        return []
    with open(LOG_PATH, "r", encoding="utf-8") as f:
        lines = f.readlines()
    error_lines = [l.strip() for l in lines if "ERROR" in l or "Error" in l or "CRITICAL" in l]
    if not error_lines:
        error_lines = [l.strip() for l in lines[-limit:]]
    return error_lines[-limit:]

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
    proc = subprocess.Popen(
        cmd, stdout=log_handle, stderr=log_handle, preexec_fn=os.setsid
    )
    PID_PATH.write_text(str(proc.pid))
    click.echo(
        f"NotionLens started in background (PID {proc.pid}). Logs: {LOG_PATH}"
    )

@cli.command()
def status():
    """Show status and live logs."""
    error_logs = _get_error_logs()
    if PID_PATH.exists():
        pid = int(PID_PATH.read_text())
        running = True
        err_msg = ""
        try:
            os.kill(pid, 0)
        except OSError as e:
            running = False
            err_msg = str(e)
        if running:
            click.echo(
                f"NotionLens running (PID {pid}). Showing logs - press Ctrl+C to exit."
            )
            subprocess.run(["tail", "-n", "20", "-f", str(LOG_PATH)])
            return
        else:
            click.echo("NotionLens PID file exists but process not running.")
            if err_msg:
                click.echo(f"Error: {err_msg}")
    else:
        click.echo("NotionLens is not running.")

    if error_logs:
        click.echo("Last error logs:")
        for line in error_logs:
            click.echo(line)

@cli.command()
def stop():
    """Stop the background process."""
    if not PID_PATH.exists():
        click.echo("NotionLens is not running.")
        return
    pid = int(PID_PATH.read_text())
    try:
        os.killpg(pid, signal.SIGTERM)
        click.echo("NotionLens stopped.")
    except OSError as e:
        click.echo(f"Error stopping NotionLens: {e}")
    PID_PATH.unlink(missing_ok=True)

@cli.command(hidden=True)
def capture():
    """Internal command used for the background process."""
    capture_loop()

