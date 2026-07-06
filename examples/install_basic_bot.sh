#!/usr/bin/env bash
# SPDX-License-Identifier: CC0-1.0
set -euo pipefail

mkdir -p ~/telegram-bot
cd ~/telegram-bot

python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install python-telegram-bot python-dotenv

cat > .env.example <<'ENV'
BOT_TOKEN=put_your_telegram_bot_token_here
ENV

if [ ! -f .env ]; then
  cp .env.example .env
fi

echo "Edit ~/telegram-bot/.env and add your real Telegram bot token."
echo "Then place bot.py in this folder and run: ./venv/bin/python bot.py"
