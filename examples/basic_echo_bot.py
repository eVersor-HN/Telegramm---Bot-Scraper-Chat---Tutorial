#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

"""
Minimal Telegram echo bot example.

Install:
    python3 -m venv venv
    ./venv/bin/pip install python-telegram-bot python-dotenv

Run:
    cp .env.example .env
    # edit .env and add BOT_TOKEN
    ./venv/bin/python examples/basic_echo_bot.py
"""

import os
from pathlib import Path

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


BASE_DIR = Path(__file__).resolve().parents[1]
load_dotenv(BASE_DIR / ".env")

BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "Bot online. Send me a message and I will echo it back."
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("STATUS // ONLINE")


async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = update.message.text or ""
    await update.message.reply_text(f"ECHO // {text}")


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN missing. Copy .env.example to .env and add your token.")

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
