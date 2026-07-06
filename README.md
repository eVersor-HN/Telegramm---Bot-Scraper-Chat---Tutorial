# Raspberry Pi Telegram Bot Guide

Practical multi-language Raspberry Pi Telegram bot guide with copy/paste setup blocks, PuTTY workflow, systemd autostart, recovery, examples and local AI notes.

## Repository contents

```text
raspberry-pi-telegram-bot-guide-v1_2/
├─ README.md
├─ LICENSE
├─ .env.example
├─ docs/
│  ├─ raspberry_pi_telegram_bot_guide_en_v1_2.pdf
└─ examples/
   ├─ basic_echo_bot.py
   ├─ instant_notes_bot.py
   ├─ telegram-bot.service
   ├─ install_minimal_pi_bot.sh
   ├─ safe_patch_example.sh
   └─ ollama_optional_smoke_test.sh
```

## Guides

- English PDF: `docs/raspberry_pi_telegram_bot_guide_en_v1_2.pdf`

## What it covers

- BotFather setup
- PuTTY / SSH workflow for beginners
- Raspberry Pi OS preparation
- Python virtual environment
- Generic Telegram bot code
- systemd autostart after reboot and power loss
- Logs, recovery, backups and restore
- Safe copy/paste code changes
- Optional Ollama / local AI notes
- Pi 3 / Pi 4 / Pi 5 expectations
- FAQ section

## Security

Never publish real bot tokens, `.env` files, databases, chat IDs, SSH keys, private logs or personal backups.

## License

Everything in this repository is released as broadly as possible under CC0/public-domain-style terms. See `LICENSE`.
