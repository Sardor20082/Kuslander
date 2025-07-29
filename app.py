from flask import Flask, request
from telegram import Update
from telegram.ext import Application

flask_app = Flask(__name__)
application: Application = None

def setup_webhook(app, flask_app, webhook_url):
    global application
    application = app
    application.bot.set_webhook(webhook_url)

@flask_app.route('/', methods=['POST'])
def webhook():
    update = Update.de_json(request.get_json(force=True), application.bot)
    application.update_queue.put_nowait(update)
    return 'ok'