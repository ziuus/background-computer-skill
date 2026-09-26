---
name: background-computer
description: >-
  Allows AI agents to perform GUI and computer-use automation inside a dedicated, 
  background X11 virtual display (DISPLAY=:99) without hijacking or interfering with 
  the user's physical mouse, keyboard, or primary display.
---

# Background Computer Skill

Use this skill when you need to perform computer-use tasks (opening desktop apps, controlling browsers, clicking UI elements, taking screenshots, or executing GUI workflows) on the user's Linux host without taking over their physical screen (`DISPLAY=:0`).

---

## 📐 Architecture & Principles

1. **Display Isolation:**
   - User's Primary Desktop: `DISPLAY=:0` (Do NOT interact with or hijack this display).
   - Agent's Background Desktop: `DISPLAY=:99` (All agent GUI operations, clicks, and screenshots take place here).

2. **Host Context:**
   - You are running on the user's host machine as the same Linux user.
   - You have access to local project files, CLI binaries, environment variables, and network resources.

---

## 🧰 Available Tools & Usage Protocol

When using the `background_computer` MCP server tools:

### 1. `execute_command(command)`
- Launch GUI applications or terminal commands inside `DISPLAY=:99`.
- Example: `execute_command("google-chrome --no-sandbox https://google.com &")`
- Example: `execute_command("xdotool search --name Chrome windowactivate")`

### 2. `screenshot()`
- Always take a screenshot after performing GUI actions to observe the updated state on `DISPLAY=:99`.
- Use image coordinates `[x, y]` from screenshots for precision mouse actions.

### 3. `mouse_move(coordinate=[x, y])`
- Move the cursor to specific coordinates on the 1280x800 background desktop.

### 4. `mouse_click(action)`
- Actions: `left_click`, `right_click`, `middle_click`, `double_click`, `left_click_drag`.

### 5. `keyboard_type(text)`
- Type literal strings into focused UI elements.

### 6. `keyboard_key(text)`
- Send key combos (e.g., `Return`, `BackSpace`, `Tab`, `ctrl+c`, `ctrl+v`, `alt+Tab`).

---

## 🎯 Best Practices for Agents

- **Observe First:** Take a `screenshot()` before performing input actions to confirm element position.
- **Verify Execution:** After running a command or clicking an element, take another `screenshot()` to verify the result.
- **Non-Blocking Execution:** When launching long-running GUI apps via `execute_command`, append `&` to run them in the background.
- **Respect User Focus:** Never attempt to touch `DISPLAY=:0` or use system xdotool calls without specifying `DISPLAY=:99`.
