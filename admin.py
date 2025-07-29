import os
import sqlite3
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import ContextTypes
from languages import LANGS
from handlers import USER_LANG
from utils import get_user_count

ADMIN_ID = int(os.environ.get("ADMIN_ID", "123456"))

async def handle_admin(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    user_id = query.from_user.id
    if user_id != ADMIN_ID:
        return
    await query.answer()
    lang = USER_LANG.get(user_id, 'uz')
    await query.edit_message_text(
        "Admin panel:",
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("📊 Statistika", callback_data="stat")],
            [InlineKeyboardButton("📢 Xabar yuborish", callback_data="broadcast")],
        ])
    )

async def handle_stat(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    count = get_user_count()
    lang = USER_LANG.get(query.from_user.id, 'uz')
    await query.edit_message_text(LANGS[lang]["stat"].format(count))

async def handle_broadcast(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    context.user_data["broadcast"] = True
    lang = USER_LANG.get(query.from_user.id, 'uz')
    await query.message.reply_text(LANGS[lang]["broadcast_prompt"])
    await query.answer()

async def handle_broadcast_text(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if context.user_data.get("broadcast"):
        context.user_data["broadcast"] = False
        conn = sqlite3.connect("bot.db")
        c = conn.cursor()
        c.execute("SELECT user_id FROM users")
        user_ids = [r[0] for r in c.fetchall()]
        conn.close()
        for uid in user_ids:
            try:
                await context.bot.send_message(uid, update.message.text)
            except:
                continue
        await update.message.reply_text("✅ Xabar yuborildi.")

def setup_admin_handlers(app):
    from telegram.ext import CallbackQueryHandler, MessageHandler, filters
    app.add_handler(CallbackQueryHandler(handle_admin, pattern="^admin$"))
    app.add_handler(CallbackQueryHandler(handle_stat, pattern="^stat$"))
    app.add_handler(CallbackQueryHandler(handle_broadcast, pattern="^broadcast$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_broadcast_text))
