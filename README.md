# Background Computer Skill 🖥️👻

Let AI agents use your real machine, with your real files and login sessions, **without interrupting your work**.

Inspired by [BrowserSkill](https://github.com/Tencent/BrowserSkill), this project provides a CLI and an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server that runs a fully functional, headless virtual desktop in the background. AI agents can open browsers, run GUI apps, type, and click around without ever hijacking your physical mouse or screen.

## Why?

Standard AI "Computer Use" APIs (like Anthropic's) take control of your main screen. The mouse moves, windows pop up, and you can't touch your computer while the agent is working. 

**Background Computer Skill** fixes this by containerizing the graphical environment (using Xvfb on Linux) while keeping the same user permissions, filesystem access, and local sessions. 

- 👻 **Invisible to you:** The agent gets its own virtual display.
- 🔐 **Real identity:** It runs as your user, meaning it has access to your logged-in browser profiles, ssh keys, and local files.
- 🤖 **Universal Agent Support:** Runs as a standard MCP server. Compatible with Claude Desktop, Antigravity, Cursor, and any other MCP-capable agent.

## Prerequisites

Currently optimized for Linux (or WSL2).

```bash
sudo apt-get install xvfb fluxbox scrot xdotool
```

## Installation

**One-line install (Recommended)**

```bash
curl -fsSL https://raw.githubusercontent.com/ziuus/background-computer-skill/main/install.sh | bash
```
*(This script automatically installs `xvfb`, `fluxbox`, and sets up the tool via `pipx` in an isolated environment).*

**Manual Installation (pipx)**

```bash
pipx install git+https://github.com/ziuus/background-computer-skill.git
```

**Docker (Universal cross-platform)**

If you are on Windows or macOS without X11, or just want a fully sandboxed environment:
```bash
docker build -t background-computer-skill .
docker run -d --name bg-computer background-computer-skill
```
*Note: For MCP over stdio with Docker, you can configure your agent to use `docker exec -i bg-computer bg-computer mcp`.*

## Usage

### 1. Start the Background Server

Run this to spin up the virtual desktop and the MCP server:

```bash
bg-computer start
```

This creates a hidden X11 display (usually `:99`), starts a lightweight window manager (`fluxbox`), and launches the MCP server on `stdio` or a local port.

### 2. Configure Your Agent (MCP)

Add this to your `mcp.json` or agent configuration:

```json
{
  "mcpServers": {
    "background_computer": {
      "command": "bg-computer",
      "args": ["mcp"]
    }
  }
}
```

## Available MCP Tools

Once connected, your agent will have access to the following tools, which strictly operate *only* inside the background desktop:

- `screenshot`: Capture the background display.
- `mouse_move`: Move the cursor to (x, y).
- `mouse_click`: Click (left, right, middle).
- `keyboard_type`: Type a string of text.
- `keyboard_key`: Press specific hotkeys (e.g., `Return`, `ctrl+c`).
- `run_command`: Execute a shell command inside the background display (e.g., `google-chrome`).

## Architecture

- **Xvfb (X Virtual Framebuffer):** Creates an in-memory display server.
- **Fluxbox:** A lightweight window manager so apps behave normally (can be resized, moved).
- **xdotool / scrot:** For stable headless input and screenshots.
- **MCP (Model Context Protocol):** Standardized interface for LLMs to invoke tools.

## License
MIT
