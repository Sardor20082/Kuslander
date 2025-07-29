import os
from app import flask_app, setup_webhook
from telegram.ext import Application
from handlers import setup_handlers
from admin import setup_admin_handlers
from utils import init_db

# .env o‘rniga Render environment variables ishlatiladi
TOKEN = os.environ.get("BOT_TOKEN")
WEBHOOK_URL = os.environ.get("WEBHOOK_URL")

# Telegram bot ilovasini yaratish
application = Application.builder().token(TOKEN).build()

# Bot handlerlarini ulash
setup_handlers(application)
setup_admin_handlers(application)

# Flask va Telegramni webhook orqali bog‘lash
setup_webhook(application, flask_app, WEBHOOK_URL)

# Ma'lumotlar bazasini boshlash (SQLite)
init_db()

# Flask serverni ishga tushurish
if __name__ == "__main__":
    flask_app.run(host="0.0.0.0", port=5000)
