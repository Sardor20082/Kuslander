from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputFile
from telegram.ext import ContextTypes
from downloader import download_video
from languages import LANGS, get_lang_keyboard
from utils import is_subscribed, add_user

USER_LANG = {}

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    user_id = update.effective_user.id
    add_user(user_id)
    if not await is_subscribed(update, context):
        await update.message.reply_text(LANGS['uz']['sub'])
        return
    await update.message.reply_text("Tilni tanlang:", reply_markup=get_lang_keyboard())

async def set_language(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = query.data.split("_")[1]
    USER_LANG[query.from_user.id] = lang
    await query.edit_message_text(
        text=LANGS[lang]['choose'],
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton("YouTube", callback_data="yt")],
            [InlineKeyboardButton("TikTok", callback_data="tt")],
            [InlineKeyboardButton("Instagram", callback_data="ig")],
            [InlineKeyboardButton(LANGS[lang]['admin'], callback_data="admin")]
        ])
    )

async def handle_platform(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    lang = USER_LANG.get(query.from_user.id, 'uz')
    await query.edit_message_text(LANGS[lang]["link"])

async def handle_link(update: Update, context: ContextTypes.DEFAULT_TYPE):
    url = update.message.text
    user_id = update.effective_user.id
    lang = USER_LANG.get(user_id, 'uz')
    msg = await update.message.reply_text("⏳ Yuklab olinmoqda...")
    try:
        path = download_video(url)
        with open(path, 'rb') as f:
            await msg.delete()
            await update.message.reply_video(InputFile(f))
    except Exception as e:
        await msg.edit_text("Xatolik yuz berdi: " + str(e))

def setup_handlers(app):
    from telegram.ext import CommandHandler, MessageHandler, CallbackQueryHandler, filters
    app.add_handler(CommandHandler("start", start))
    app.add_handler(CallbackQueryHandler(set_language, pattern="^lang_"))
    app.add_handler(CallbackQueryHandler(handle_platform, pattern="^(yt|tt|ig)$"))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_link))