#!/usr/bin/env bash
set -e
sudo apt update
sudo apt install -y python3-venv python3-pip sqlite3 git curl ca-certificates
mkdir -p "$HOME/telegram-bot"
cd "$HOME/telegram-bot"
python3 -m venv venv
./venv/bin/python -m pip install --upgrade pip
./venv/bin/pip install python-telegram-bot==22.8
cp "$(dirname "$0")/instant_notes_bot.py" bot.py
cp "$(dirname "$0")/telegram-bot.service" telegram-bot.service
printf 'Now create .env with BOT_TOKEN, then install the service.
'
