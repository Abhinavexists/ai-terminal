#!/bin/bash

echo "Uninstalling AI Terminal CLI..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please don't run this script as root. It will ask for sudo when needed."
    exit 1
fi

# Remove binary and symlink
sudo rm -f /usr/local/bin/ai-terminal
sudo rm -f /usr/local/bin/ai-terminal-cli

# Remove config file (optional)
read -p "Remove configuration file (~/.ai_terminal_config.json)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f ~/.ai_terminal_config.json
    echo "Configuration file removed."
fi

echo "AI Terminal CLI uninstalled successfully!"
