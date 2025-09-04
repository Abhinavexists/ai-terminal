#!/bin/bash

set -euo pipefail

APP_NAME="dwarp"
BIN_TARGET="/usr/local/bin/${APP_NAME}"

echo "Uninstalling ${APP_NAME}..."

if [ "${EUID}" -eq 0 ]; then
    echo "Please don't run this script as root. It will ask for sudo when needed."
    exit 1
fi

# Remove binary and symlinks
sudo rm -f "${BIN_TARGET}"
sudo rm -f /usr/local/bin/ai-terminal
sudo rm -f /usr/local/bin/ai-terminal-cli

# Optional: remove user config
read -p "Remove configuration file (~/.ai_terminal_config.json)? [y/N]: " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    rm -f ~/.ai_terminal_config.json
    echo "Configuration file removed."
fi

echo "${APP_NAME} uninstalled successfully!"

