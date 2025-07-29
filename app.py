from flask import Flask, request
from telegram.ext import Application

flask_app = Flask(__name__)
application: Application = None  # bu global o'zgaruvchi

def setup_webhook(app: Application, flask_app: Flask, webhook_url: str):
    global application
    application = app
    application.bot.set_webhook(webhook_url)

@flask_app.route("/", methods=["POST"])
def webhook_handler():
    if request.method == "POST":
        update = application.bot._parse_webhook_json(request.get_json(force=True))
        application.update_queue.put_nowait(update)
        return "OK", 200
