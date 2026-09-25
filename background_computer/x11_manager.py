import subprocess
import time
import os
import signal
import sys

class XvfbManager:
    def __init__(self, display_num=99, width=1280, height=800, depth=24):
        self.display_num = display_num
        self.width = width
        self.height = height
        self.depth = depth
        self.xvfb_proc = None
        self.wm_proc = None

    def start(self):
        display_str = f":{self.display_num}"
        # Start Xvfb
        try:
            self.xvfb_proc = subprocess.Popen(
                ["Xvfb", display_str, "-screen", "0", f"{self.width}x{self.height}x{self.depth}"],
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            print("Error: Xvfb not found. Please install xvfb (e.g., sudo apt-get install xvfb).")
            sys.exit(1)

        # Wait for Xvfb to start
        time.sleep(1)
        
        # Set environment variable for future subprocesses
        os.environ["DISPLAY"] = display_str

        # Start a lightweight window manager if available
        try:
            self.wm_proc = subprocess.Popen(
                ["fluxbox"],
                env=os.environ,
                stdout=subprocess.DEVNULL,
                stderr=subprocess.DEVNULL
            )
        except FileNotFoundError:
            try:
                self.wm_proc = subprocess.Popen(
                    ["openbox"],
                    env=os.environ,
                    stdout=subprocess.DEVNULL,
                    stderr=subprocess.DEVNULL
                )
            except FileNotFoundError:
                print("Warning: Neither fluxbox nor openbox found. Windows might not be resizable/movable.")

    def stop(self):
        if self.wm_proc:
            self.wm_proc.terminate()
            self.wm_proc = None
        if self.xvfb_proc:
            self.xvfb_proc.terminate()
            self.xvfb_proc = None

    def __enter__(self):
        self.start()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.stop()
