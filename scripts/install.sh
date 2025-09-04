#!/bin/bash

set -euo pipefail

APP_NAME="dwarp"
BIN_TARGET="/usr/local/bin/${APP_NAME}"

echo "Installing ${APP_NAME}..."

if [ "${EUID}" -eq 0 ]; then
    echo "Please don't run this script as root. It will ask for sudo when needed."
    exit 1
fi

if [ ! -f "${APP_NAME}" ]; then
    echo "Error: '${APP_NAME}' binary not found in current directory."
    echo "Run this script from inside the extracted '${APP_NAME}-linux' folder."
    exit 1
fi

sudo mkdir -p /usr/local/bin
sudo install -m 755 "${APP_NAME}" "${BIN_TARGET}"

# Backward-compatibility symlinks (optional)
sudo ln -sf "${BIN_TARGET}" /usr/local/bin/ai-terminal || true
sudo ln -sf "${BIN_TARGET}" /usr/local/bin/ai-terminal-cli || true

echo "${APP_NAME} installed to ${BIN_TARGET}"
echo "You can run it with: ${APP_NAME}"
echo "Legacy commands (if you used them before) will still work: ai-terminal, ai-terminal-cli"

