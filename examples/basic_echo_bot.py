import os
from pathlib import Path
from telegram import Update
from telegram.ext import Application, CommandHandler, MessageHandler, ContextTypes, filters
ENV_FILE = Path(__file__).resolve().parent / '.env'
def load_env():
    if ENV_FILE.exists():
        for line in ENV_FILE.read_text(encoding='utf-8').splitlines():
            if line.strip() and '=' in line and not line.startswith('#'):
                k, v = line.split('=', 1)
                os.environ.setdefault(k.strip(), v.strip().strip('"').strip("'"))
async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('BOT ONLINE // echo mode')
async def echo(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text('ECHO // ' + (update.message.text or ''))
def main():
    load_env()
    token = os.environ.get('BOT_TOKEN', '')
    if not token:
        raise RuntimeError('BOT_TOKEN missing in .env')
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler('start', start))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, echo))
    app.run_polling(allowed_updates=Update.ALL_TYPES, drop_pending_updates=True)
if __name__ == '__main__':
    main()
