#!/usr/bin/env python3
# SPDX-License-Identifier: CC0-1.0

"""
Simple Telegram notes bot using SQLite.

Normal message -> stored as a note.
/today         -> show today's notes.
/last          -> show latest notes.
/files         -> export txt + jsonl backup files.

This is generic example code, not a full production app.
"""

import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from dotenv import load_dotenv
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters


BASE_DIR = Path(__file__).resolve().parents[1]
DB_FILE = BASE_DIR / "notes.db"
BACKUP_DIR = BASE_DIR / "backups"
TZ = ZoneInfo("Europe/Berlin")

load_dotenv(BASE_DIR / ".env")
BOT_TOKEN = os.getenv("BOT_TOKEN", "").strip()


def now_local() -> datetime:
    return datetime.now(TZ)


def normalize(text: str) -> str:
    text = str(text or "").strip()
    text = re.sub(r"\s+", " ", text)
    for before, after in {
        " ,": ",",
        " .": ".",
        " !": "!",
        " ?": "?",
        " :": ":",
        " ;": ";",
    }.items():
        text = text.replace(before, after)
    return text.strip()


def db() -> sqlite3.Connection:
    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row
    return con


def init_db() -> None:
    con = db()
    con.execute(
        """
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            text TEXT NOT NULL
        )
        """
    )
    con.commit()
    con.close()


def insert_note(text: str) -> int:
    text = normalize(text)
    if not text:
        raise ValueError("empty note")

    con = db()
    cur = con.cursor()
    cur.execute(
        "INSERT INTO notes (created_at, text) VALUES (?, ?)",
        (now_local().isoformat(timespec="seconds"), text),
    )
    note_id = int(cur.lastrowid)
    con.commit()
    con.close()
    return note_id


def fetch_latest(limit: int = 20) -> list[sqlite3.Row]:
    con = db()
    rows = con.execute(
        "SELECT id, created_at, text FROM notes ORDER BY id DESC LIMIT ?",
        (limit,),
    ).fetchall()
    con.close()
    return list(reversed(rows))


def fetch_today() -> list[sqlite3.Row]:
    start = now_local().replace(hour=0, minute=0, second=0, microsecond=0)
    con = db()
    rows = con.execute(
        "SELECT id, created_at, text FROM notes WHERE created_at >= ? ORDER BY id ASC",
        (start.isoformat(timespec="seconds"),),
    ).fetchall()
    con.close()
    return list(rows)


def format_notes(rows: list[sqlite3.Row]) -> str:
    if not rows:
        return "VAULT.EMPTY // no notes found"
    return "\n".join(f"- #{row['id']} {row['text']}" for row in rows)


def make_backup_files() -> tuple[Path, Path]:
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = now_local().strftime("%Y%m%d-%H%M%S")
    txt_path = BACKUP_DIR / f"notes-backup-{stamp}.txt"
    jsonl_path = BACKUP_DIR / f"notes-backup-{stamp}.jsonl"

    rows = fetch_latest(100000)

    with txt_path.open("w", encoding="utf-8") as txt, jsonl_path.open("w", encoding="utf-8") as js:
        for row in rows:
            item = {"id": row["id"], "created_at": row["created_at"], "text": row["text"]}
            txt.write(f"#{item['id']} {item['created_at']} - {item['text']}\n")
            js.write(json.dumps(item, ensure_ascii=False) + "\n")

    return txt_path, jsonl_path


async def start(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text(
        "[NOTEVAULT]\n"
        "STATUS // ONLINE\n\n"
        "Send any normal message to store it as a note.\n"
        "/today - show today\n"
        "/last - show latest notes\n"
        "/files - export backups\n"
        "/status - bot status"
    )


async def status(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    con = db()
    count = con.execute("SELECT COUNT(*) AS c FROM notes").fetchone()["c"]
    con.close()
    await update.message.reply_text(f"[NOTEVAULT]\nSTATUS // ONLINE\nSTORED // {count} notes")


async def today(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    await update.message.reply_text("[TODAY]\n" + format_notes(fetch_today()))


async def last(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    limit = 20
    if context.args:
        try:
            limit = max(1, min(100, int(context.args[0])))
        except ValueError:
            limit = 20
    await update.message.reply_text("[LATEST]\n" + format_notes(fetch_latest(limit)))


async def files(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    txt_path, jsonl_path = make_backup_files()
    await update.message.reply_document(document=txt_path.open("rb"), filename=txt_path.name)
    await update.message.reply_document(document=jsonl_path.open("rb"), filename=jsonl_path.name)


async def save_note(update: Update, context: ContextTypes.DEFAULT_TYPE) -> None:
    text = normalize(update.message.text or "")
    if not text:
        await update.message.reply_text("INTAKE.REJECTED // empty signal")
        return

    note_id = insert_note(text)
    await update.message.reply_text(f"[LOGGED]\n- #{note_id} {text}")


def main() -> None:
    if not BOT_TOKEN:
        raise RuntimeError("BOT_TOKEN missing. Copy .env.example to .env and add your token.")

    init_db()

    app = Application.builder().token(BOT_TOKEN).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", start))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("today", today))
    app.add_handler(CommandHandler("last", last))
    app.add_handler(CommandHandler("files", files))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, save_note))
    app.run_polling(allowed_updates=Update.ALL_TYPES)


if __name__ == "__main__":
    main()
