#!/bin/bash
set -e

echo "👻 Installing Background Computer Skill..."

# Detect OS
if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # Check for Debian/Ubuntu
    if [ -x "$(command -v apt-get)" ]; then
        echo "Installing system dependencies (xvfb, fluxbox, scrot, xdotool)..."
        sudo apt-get update -qq
        sudo apt-get install -y xvfb fluxbox scrot xdotool python3-venv python3-pip pipx
    elif [ -x "$(command -v pacman)" ]; then
        echo "Installing system dependencies for Arch Linux..."
        sudo pacman -Sy --noconfirm xorg-server-xvfb fluxbox scrot xdotool python-pipx
    else
        echo "Please ensure xvfb, fluxbox, scrot, and xdotool are installed."
    fi
elif [[ "$OSTYPE" == "darwin"* ]]; then
    echo "macOS detected. Note: True headless background X11 requires XQuartz."
    echo "For full seamless experience, running this within a Linux VM/WSL is recommended."
    if [ -x "$(command -v brew)" ]; then
        brew install pipx
    fi
else
    echo "Warning: Unrecognized OS ($OSTYPE). Proceeding with pipx installation."
fi

# Ensure pipx path
export PATH="$HOME/.local/bin:$PATH"

echo "Installing background-computer-skill via pipx..."
pipx install git+https://github.com/ziuus/background-computer-skill.git --force

# Install SKILL.md into global agent configuration directory
SKILL_DIR="$HOME/.gemini/config/skills/background-computer"
mkdir -p "$SKILL_DIR"
curl -fsSL https://raw.githubusercontent.com/ziuus/background-computer-skill/main/SKILL.md -o "$SKILL_DIR/SKILL.md"

echo "✅ Installation complete!"
echo "• Skill prompt registered at: $SKILL_DIR/SKILL.md"
echo "• Start server with: bg-computer start"

