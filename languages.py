from telegram import InlineKeyboardMarkup, InlineKeyboardButton

LANGS = {
    "uz": {
        "name": "🇺🇿 O‘zbek", "choose": "Qaysi platformani tanlaysiz?",
        "sub": "Iltimos, kanalga obuna bo‘ling",
        "admin": "🔧 Sozlamalar", "link": "Video linkni yuboring:",
        "stat": "👤 Foydalanuvchilar soni: {}",
        "broadcast_prompt": "Xabar matnini yuboring:"
    },
    "ru": {
        "name": "🇷🇺 Русский", "choose": "Выберите платформу",
        "sub": "Пожалуйста, подпишитесь на канал",
        "admin": "🔧 Настройки", "link": "Отправьте ссылку на видео:",
        "stat": "👤 Пользователей: {}",
        "broadcast_prompt": "Отправьте текст сообщения:"
    },
    "en": {
        "name": "🇺🇸 English", "choose": "Choose a platform",
        "sub": "Please subscribe to the channel",
        "admin": "🔧 Settings", "link": "Send the video link:",
        "stat": "👤 Users: {}",
        "broadcast_prompt": "Send your broadcast message:"
    }
}

def get_lang_keyboard():
    return InlineKeyboardMarkup([
        [InlineKeyboardButton(v['name'], callback_data=f"lang_{k}")]
        for k, v in LANGS.items()
    ])