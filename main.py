import os
from app import flask_app, setup_webhook
from telegram.ext import Application
from handlers import setup_handlers
from admin import setup_admin_handlers
from utils import init_db

# Token va webhook URL muhit o'zgaruvchilardan olinadi
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Telegram botni yaratish
application = Application.builder().token(TOKEN).build()

# Handlerlarni o‘rnatish
setup_handlers(application)
setup_admin_handlers(application)

# Webhookni sozlash
setup_webhook(application, flask_app, WEBHOOK_URL)

# SQLite DB ni ishga tushirish
init_db()

# Flask appni ishga tushirish (Render uchun)
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
