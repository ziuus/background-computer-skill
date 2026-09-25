import click
import os
import sys
import time
from .x11_manager import XvfbManager

@click.group()
def main():
    """Background Computer Skill CLI"""
    pass

@main.command()
@click.option('--display', default=99, help='Display number to use (e.g. 99 for :99)')
@click.option('--width', default=1280, help='Screen width')
@click.option('--height', default=800, help='Screen height')
def start(display, width, height):
    """Start the background Xvfb server and optionally an MCP server."""
    click.echo(f"Starting Background Computer on DISPLAY=:{display}...")
    manager = XvfbManager(display_num=display, width=width, height=height)
    try:
        manager.start()
        click.echo("Background virtual desktop is running.")
        click.echo("Press Ctrl+C to stop.")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        click.echo("Stopping Background Computer...")
        manager.stop()
        click.echo("Stopped.")
    except Exception as e:
        click.echo(f"Error: {e}")
        manager.stop()

@main.command()
@click.option('--display', default=99, help='Display number to use (e.g. 99 for :99)')
def mcp(display):
    """
    Start the MCP server.
    This should usually be run by the AI agent's MCP client (like Claude Desktop).
    It will ensure Xvfb is running first if it isn't.
    """
    # Check if Xvfb is already running on this display
    display_str = f":{display}"
    
    # We will just set the environment variable. If Xvfb isn't running, tools might fail.
    # To be robust, we could auto-start Xvfb, but XvfbManager blocks if we wait. 
    # Let's start it in the background if it's not detected.
    import subprocess
    try:
        # Check if xdpyinfo works on the display
        os.environ["DISPLAY"] = display_str
        subprocess.run(["xdpyinfo"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=True)
    except Exception:
        # Auto-start xvfb since it's not running
        manager = XvfbManager(display_num=display)
        manager.start()
        import atexit
        atexit.register(manager.stop)

    # Start the MCP server via stdio
    from .mcp_server import run_server
    run_server()

if __name__ == '__main__':
    main()
