import os
import subprocess
import base64
import pyautogui
from io import BytesIO
from mcp.server.fastmcp import FastMCP
from pydantic import BaseModel, Field
from typing import Optional, List

mcp = FastMCP("background_computer")

@mcp.tool()
def execute_command(command: str) -> str:
    """
    Execute a shell command inside the background virtual desktop.
    Applications launched this way will open in the background display.
    """
    try:
        # Use Popen and communicate so it runs inside the existing environment (with DISPLAY=:99)
        process = subprocess.Popen(
            command,
            shell=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True
        )
        # We wait briefly to see if it immediately fails, otherwise we return success.
        try:
            out, err = process.communicate(timeout=2)
            return f"Command executed. Output: {out}\nErrors: {err}"
        except subprocess.TimeoutExpired:
            return f"Command '{command}' launched successfully in the background."
    except Exception as e:
        return f"Error executing command: {str(e)}"

@mcp.tool()
def computer_action(
    action: str, 
    text: Optional[str] = None, 
    coordinate: Optional[List[int]] = None
) -> str:
    """
    Perform a computer action (mouse, keyboard, or screenshot) in the background display.
    
    Valid actions:
    - mouse_move: requires coordinate [x, y]
    - left_click, right_click, middle_click, double_click
    - left_click_drag: requires coordinate [x, y]
    - type: requires text
    - key: requires text (e.g. 'Return', 'ctrl+c')
    - screenshot: returns base64 image
    """
    # Ensure fail-safe is off so we can reach corners of virtual display
    pyautogui.FAILSAFE = False

    try:
        if action == "mouse_move":
            if not coordinate or len(coordinate) != 2:
                return "Error: coordinate [x, y] is required for mouse_move"
            pyautogui.moveTo(coordinate[0], coordinate[1])
            return f"Mouse moved to {coordinate}"
            
        elif action == "left_click":
            pyautogui.click()
            return "Left clicked"
            
        elif action == "right_click":
            pyautogui.click(button='right')
            return "Right clicked"
            
        elif action == "middle_click":
            pyautogui.click(button='middle')
            return "Middle clicked"
            
        elif action == "double_click":
            pyautogui.doubleClick()
            return "Double clicked"
            
        elif action == "left_click_drag":
            if not coordinate or len(coordinate) != 2:
                return "Error: coordinate [x, y] is required for left_click_drag"
            pyautogui.dragTo(coordinate[0], coordinate[1], button='left')
            return f"Left click dragged to {coordinate}"
            
        elif action == "type":
            if not text:
                return "Error: text is required for type action"
            pyautogui.write(text, interval=0.01)
            return f"Typed: {text}"
            
        elif action == "key":
            if not text:
                return "Error: text (key sequence) is required for key action"
            # Split hotkeys if they contain +
            keys = text.split('+')
            pyautogui.hotkey(*keys)
            return f"Pressed key(s): {text}"
            
        elif action == "screenshot":
            # Taking a screenshot of the virtual display
            screenshot = pyautogui.screenshot()
            buffered = BytesIO()
            screenshot.save(buffered, format="PNG")
            img_str = base64.b64encode(buffered.getvalue()).decode()
            # For FastMCP tools that return images, we return a special format if needed,
            # or just return the base64 string. 
            return f"data:image/png;base64,{img_str}"
            
        else:
            return f"Error: unknown action '{action}'"
            
    except Exception as e:
        return f"Error performing action {action}: {str(e)}"

def run_server():
    # If the user started this from the CLI, DISPLAY should already be set by x11_manager
    if "DISPLAY" not in os.environ:
        os.environ["DISPLAY"] = ":99"
    mcp.run()
