FROM ubuntu:22.04

# Avoid prompts during apt installs
ENV DEBIAN_FRONTEND=noninteractive

RUN apt-get update -qq && apt-get install -y \
    python3 \
    python3-pip \
    python3-venv \
    xvfb \
    fluxbox \
    scrot \
    xdotool \
    git \
    sudo \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Add a non-root user
RUN useradd -m -s /bin/bash agent && \
    echo "agent ALL=(ALL) NOPASSWD:ALL" >> /etc/sudoers

USER agent
WORKDIR /home/agent/workspace

# Install the tool
RUN python3 -m pip install --no-cache-dir pipx && \
    /home/agent/.local/bin/pipx install git+https://github.com/ziuus/background-computer-skill.git

ENV PATH="/home/agent/.local/bin:${PATH}"

# Expose MCP standard IO? No, for Docker it's usually better to run a command or SSE server.
# Here we just default to the background computer start. 
# A custom entrypoint to keep container alive
CMD ["bg-computer", "start"]
