#!/bin/bash

echo "Installing AI Terminal CLI..."

# Check if running as root
if [ "$EUID" -eq 0 ]; then
    echo "Please don't run this script as root. It will ask for sudo when needed."
    exit 1
fi

# Create directories
sudo mkdir -p /usr/local/bin

# Copy binary
sudo cp ai-terminal /usr/local/bin/
sudo chmod +x /usr/local/bin/ai-terminal

# Create symlink for easier access
sudo ln -sf /usr/local/bin/ai-terminal /usr/local/bin/ai-terminal-cli

echo "AI Terminal CLI installed successfully!"
echo ""
echo "Usage:"
echo "  ai-terminal     # Start the AI terminal"
echo "  ai-terminal-cli # Alternative command"
echo ""
echo "First run will prompt you to enter your Gemini API key."
echo "Get your API key at: https://aistudio.google.com/app/apikey"
