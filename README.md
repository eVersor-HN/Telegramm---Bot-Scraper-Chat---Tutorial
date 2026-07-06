# Raspberry Pi Telegram Bot Guide

Practical English guide and copy/paste examples for building and running Telegram bots on a Raspberry Pi.

This repository contains a light, beginner-friendly PDF guide plus generic example files for setting up a Telegram bot on Raspberry Pi OS. It covers the basic path from creating a bot with BotFather to running Python code as a persistent `systemd` service.

## Download the guide

[Open the PDF guide](docs/raspberry_pi_telegram_bot_guide_light_en.pdf)

## What is included

- Telegram BotFather setup overview
- Raspberry Pi preparation notes
- SSH-based workflow
- Python virtual environment setup
- Generic Telegram bot example
- Generic note-vault bot example using SQLite
- `.env.example` configuration template
- `systemd` service example
- Git ignore rules for tokens, databases and local files
- Raspberry Pi 3 / 4 / 5 expectations
- Notes about local AI models, Ollama and Huihui model examples

## Suggested repo structure

```text
raspberry-pi-telegram-bot-guide/
├─ README.md
├─ LICENSE
├─ .gitignore
├─ .env.example
├─ docs/
│  └─ raspberry_pi_telegram_bot_guide_light_en.pdf
└─ examples/
   ├─ basic_echo_bot.py
   ├─ simple_notes_bot.py
   └─ telegram-bot.service
```

## Quick start

Create a bot with Telegram BotFather, copy the token into `.env`, install the Python dependencies, then run one of the examples.

```bash
python3 -m venv venv
./venv/bin/pip install --upgrade pip
./venv/bin/pip install python-telegram-bot python-dotenv
cp .env.example .env
nano .env
./venv/bin/python examples/basic_echo_bot.py
```

## Security note

Never commit real Telegram bot tokens, API keys, passwords, private SSH keys, personal chat IDs, `.env` files, SQLite databases or backup files.

Use `.env.example` as the public template and keep your real `.env` private.

## License

No rights reserved. The PDF, text and example files in this repository are released for unrestricted use. You may copy, modify, share, publish, translate, sell or reuse them for any purpose.

See [LICENSE](LICENSE).
