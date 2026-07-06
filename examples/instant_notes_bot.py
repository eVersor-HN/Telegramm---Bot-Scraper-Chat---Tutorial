import json
import os
import re
import sqlite3
from datetime import datetime
from pathlib import Path
from zoneinfo import ZoneInfo

from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters

BASE = Path(__file__).resolve().parent
DB_FILE = BASE / "bot.db"
ENV_FILE = BASE / ".env"
BACKUP_DIR = BASE / "backups"
TZ = ZoneInfo("Europe/Berlin")

def load_env():
    if not ENV_FILE.exists():
        return
    for line in ENV_FILE.read_text(encoding="utf-8", errors="ignore").splitlines():
        line = line.strip()
        if not line or line.startswith("#") or "=" not in line:
            continue
        key, value = line.split("=", 1)
        os.environ.setdefault(key.strip(), value.strip().strip('"').strip("'"))

def now_local():
    return datetime.now(TZ)

def clean_text(text):
    text = str(text or "").strip()
    text = re.sub(r"\s+", " ", text)
    for before, after in {" ,": ",", " .": ".", " !": "!", " ?": "?"}.items():
        text = text.replace(before, after)
    return text.strip()

def db():
    con = sqlite3.connect(DB_FILE)
    con.row_factory = sqlite3.Row
    return con

def init_db():
    con = db()
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS notes (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            created_at TEXT NOT NULL,
            text TEXT NOT NULL
        )
    """)
    con.commit()
    con.close()

def add_note(text):
    text = clean_text(text)
    if not text:
        raise ValueError("empty note")
    con = db()
    cur = con.cursor()
    cur.execute("INSERT INTO notes (created_at, text) VALUES (?, ?)", (now_local().isoformat(timespec="seconds"), text))
    note_id = cur.lastrowid
    con.commit()
    con.close()
    return note_id

def get_last(limit=10):
    con = db()
    rows = con.execute("SELECT id, created_at, text FROM notes ORDER BY id DESC LIMIT ?", (limit,)).fetchall()
    con.close()
    return list(reversed(rows))

def format_notes(rows):
    if not rows:
        return "VAULT.EMPTY // no notes stored"
    return "\n".join(f"- #{r['id']} {r['text']}" for r in rows)

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "[RASPI.BOT]\nNODE ONLINE // send normal text to store a note\n\n"
        "/status - health check\n/last - latest notes\n/files - export backups\n/help - command list"
    )

async def status(update: Update, context: ContextTypes.DEFAULT_TYPE):
    con = db()
    total = con.execute("SELECT COUNT(*) AS c FROM notes").fetchone()["c"]
    con.close()
    await update.message.reply_text(f"STATUS // ONLINE\nSTORED // {total} notes")

async def last(update: Update, context: ContextTypes.DEFAULT_TYPE):
    limit = 10
    if context.args:
        try:
            limit = max(1, min(50, int(context.args[0])))
        except ValueError:
            limit = 10
    await update.message.reply_text("[LATEST]\n" + format_notes(get_last(limit)))

async def files(update: Update, context: ContextTypes.DEFAULT_TYPE):
    BACKUP_DIR.mkdir(exist_ok=True)
    stamp = now_local().strftime("%Y%m%d-%H%M%S")
    txt = BACKUP_DIR / f"notes-{stamp}.txt"
    jsonl = BACKUP_DIR / f"notes-{stamp}.jsonl"
    rows = get_last(100000)
    txt.write_text(format_notes(rows) + "\n", encoding="utf-8")
    with jsonl.open("w", encoding="utf-8") as f:
        for r in rows:
            f.write(json.dumps(dict(r), ensure_ascii=False) + "\n")
    await update.message.reply_text("FILE.NODE // exporting backup files")
    await update.message.reply_document(document=txt.open("rb"), filename=txt.name)
    await update.message.reply_document(document=jsonl.open("rb"), filename=jsonl.name)

async def help_cmd(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await start(update, context)

async def store_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    text = clean_text(update.message.text)
    if not text:
        await update.message.reply_text("INTAKE.REJECTED // empty message")
        return
    note_id = add_note(text)
    await update.message.reply_text(f"[LOGGED]\n- #{note_id} {text}")

def main():
    load_env()
    token = os.environ.get("BOT_TOKEN", "").strip()
    if not token:
        raise RuntimeError("BOT_TOKEN missing in .env")
    init_db()
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CommandHandler("help", help_cmd))
    app.add_handler(CommandHandler("status", status))
    app.add_handler(CommandHandler("last", last))
    app.add_handler(CommandHandler("files", files))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, store_text))
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)

if __name__ == "__main__":
    main()
