# Background Computer Skill 🖥️👻

Give AI agents their own virtual desktop — running in the background while you keep working normally.

Inspired by [BrowserSkill](https://github.com/Tencent/BrowserSkill), **Background Computer Skill** provides an [MCP (Model Context Protocol)](https://modelcontextprotocol.io/) server and CLI that creates a headless X11 display for AI agents. Instead of fighting you for your physical mouse and screen, agents operate on an isolated display while retaining access to your local machine's environment.

---

## 💡 Architecture & Design

Standard AI "Computer Use" APIs (like Anthropic's) operate directly on your primary display (`DISPLAY=:0`), hijacking your cursor and stealing window focus.

**Background Computer Skill** separates the human desktop from the agent desktop:

```
                  SAME USER / SAME HOST
                           │
             ┌─────────────┴─────────────┐
             │                           │
       User Session                  Agent Session
       (DISPLAY=:0)                  (DISPLAY=:99)
             │                           │
       ┌───────────┐              ┌───────────┐
       │ Physical  │              │ Xvfb      │
       │ Desktop   │              │ Display   │
       └───────────┘              └─────┬─────┘
                                       │
                                   Fluxbox WM
                                       │
                                  Computer Use
```

### Modes of Operation

- **Native Mode (Default):** Runs as your host user on `DISPLAY=:99`. The agent shares your machine's environment (filesystem, installed software, project directories, CLI credentials, environment variables, network) while its GUI applications run silently on the background display.
- **Docker Mode:** Runs inside an isolated Ubuntu container. Best when you prefer strong sandbox isolation or are running on macOS/Windows without X11.

---

## 🚀 Installation

**One-line install (Recommended for Linux / WSL2)**

```bash
curl -fsSL https://raw.githubusercontent.com/ziuus/background-computer-skill/main/install.sh | bash
```
*(This script installs `xvfb`, `fluxbox`, `xdotool`, `scrot`, and sets up `bg-computer` via `pipx`).*

**Manual Installation (pipx)**

```bash
pipx install git+https://github.com/ziuus/background-computer-skill.git
```

**Docker (Container Sandbox)**

```bash
docker build -t background-computer-skill .
docker run -d --name bg-computer background-computer-skill
```
*MCP with Docker: Configure your agent to run `docker exec -i bg-computer bg-computer mcp`.*

---

## 🛠️ Usage

### 1. Start the Background Server

```bash
bg-computer start
```

This creates an in-memory X11 display (`:99`), starts a lightweight window manager (`fluxbox`), and prepares the environment for computer-use actions.

### 2. Configure Your Agent (MCP)

Add this to your `mcp.json` (Claude Desktop, Antigravity, Cursor, etc.):

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

### 3. Register the Agent Skill (`SKILL.md`)

In addition to the MCP server, you can give your AI agent the operational rules and prompt instructions by copying [`SKILL.md`](./SKILL.md) into your agent's skill directory:

**For Antigravity / Agentic Coding Assistants:**
```bash
mkdir -p ~/.gemini/config/skills/background-computer
curl -fsSL https://raw.githubusercontent.com/ziuus/background-computer-skill/main/SKILL.md -o ~/.gemini/config/skills/background-computer/SKILL.md
```

**For Project-Level Workspace (.agents/):**
```bash
mkdir -p .agents/skills/background-computer
curl -fsSL https://raw.githubusercontent.com/ziuus/background-computer-skill/main/SKILL.md -o .agents/skills/background-computer/SKILL.md
```

### 4. Live Picture-in-Picture Monitor (Optional)

If you want to watch the agent work in real-time without letting it touch your real mouse or keyboard, run:

```bash
bg-computer view
```

This opens a lightweight floating preview window on your primary desktop (`DISPLAY=:0`) that mirrors the agent's background screen (`DISPLAY=:99`) in real-time. You can close or minimize it at any time while the agent continues running in the background.

---

## 🧰 Available MCP Tools

Agents connected to the MCP server can execute computer-use actions strictly isolated within `DISPLAY=:99`:

- `screenshot`: Capture the current frame of the background desktop.
- `mouse_move`: Move the cursor to target `[x, y]` coordinates.
- `mouse_click`: Click (`left`, `right`, `middle`, `double_click`).
- `keyboard_type`: Type strings of text.
- `keyboard_key`: Send hotkeys and special keys (e.g. `Return`, `ctrl+c`, `Tab`).
- `run_command`: Launch terminal commands or GUI apps (e.g. `google-chrome`) inside the background display.

---

## 📜 License

MIT

