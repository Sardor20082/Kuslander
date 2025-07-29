from flask import Flask, request
from telegram import Update
import os

flask_app = Flask(__name__)
application = None  # bu global o‘zgaruvchi bo‘ladi

def setup_webhook(app_obj, flask_app_obj, webhook_url):
    global application
    application = app_obj
    flask_app_obj.add_url_rule('/', 'webhook', webhook_handler, methods=["POST"])
    flask_app_obj.before_first_request(lambda: application.bot.set_webhook(url=webhook_url))

async def webhook_handler():
    if request.method == "POST":
        data = request.get_json(force=True)
        update = Update.de_json(data, application.bot)
        await application.process_update(update)
        return "ok", 200
