import logging
from googletrans import Translator
import requests
from PIL import Image
import numpy as np
from g4f import Client
from io import BytesIO
import telegram
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup, KeyboardButton, ReplyKeyboardRemove
from telegram.ext import Updater, MessageHandler, Filters, CommandHandler, CallbackContext, CallbackQueryHandler
from concurrent.futures import ThreadPoolExecutor
import os
import json
import re
from deep_translator import GoogleTranslator


logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(),
        logging.FileHandler("output.log", mode='w')
    ]
)

bot_token = "your-telegram-bot-token"
AUTH_FILE = "user_auth.json"
CHANNEL_USERNAME = "@YourChannelUsername"
MAX_DAILY_IMAGES = float('inf')
authenticated_users = {}
user_stats = {}
executor = ThreadPoolExecutor(max_workers=100)
bot = telegram.Bot(token=bot_token)
translator = Translator()
client = Client()

def error_handler(func):
    def wrapper(*args, **kwargs):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            logging.error(f"🚨 خطای غیرمنتظره: {e}")
            update = args[0] if len(args) > 0 and isinstance(args[0], Update) else None
            if update:
                update.message.reply_text("متاسفانه خطایی رخ داد. لطفاً بعداً تلاش کنید.")
    return wrapper

def convert_persian_numbers_to_english(text):
    persian_to_english_digits = str.maketrans('۰۱۲۳۴۵۶۷۸۹', '0123456789')
    return text.translate(persian_to_english_digits)

def translate(text):
    clean_text = convert_persian_numbers_to_english(text)


    return GoogleTranslator(source='fa', target='en').translate(clean_text)

def generate_image(prompt):
    try:
        print(prompt)
        translated = translate(prompt)
        print(translated)
        logging.info(f"Translated prompt: {translated}")

        response = client.images.generate(
            model="flux-dev",
            prompt=translated,
            response_format="url",
            quality=1000,
            size="1024x1024"
        )

        image_url = response.data[0].url
        response = requests.get(image_url)
        img = Image.open(BytesIO(response.content))

        if img.mode != 'RGB':
            img = img.convert('RGB')

        byte_io = BytesIO()
        img.save(byte_io, format="JPEG")
        byte_io.seek(0)
        return byte_io

    except Exception as e:
        logging.error(f"Error generating image: {e}")
        return None

def load_data():
    global user_stats, authenticated_users
    if os.path.exists("user_stats.json"):
        with open("user_stats.json", "r", encoding="utf-8") as f:
            user_stats = json.load(f)
    else:
        user_stats = {}

    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r", encoding="utf-8") as f:
            authenticated_users = json.load(f)
    else:
        authenticated_users = {}

def save_data():
    with open("user_stats.json", "w", encoding="utf-8") as f:
        json.dump(user_stats, f, ensure_ascii=False, indent=2)
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(authenticated_users, f, ensure_ascii=False, indent=2)

@error_handler
def process_message(update: Update, context: CallbackContext) -> None:
    message = update.effective_message
    chat = update.effective_chat
    text = message.text.strip()


    if chat.type != "private" and not text.startswith('/:'):
        return


    if chat.type in ["group", "supergroup"] and text.startswith('/:'):
        prompt = text[2:].lstrip()
    else:
        prompt = text.strip()  

    # حالا ادامه پردازش پیام
    user_id = update.effective_user.id
    text = message.text.strip()

    user_id = str(update.message.from_user.id)
    chat_id = update.message.chat_id
    reply_id = update.message.message_id

    prompt = text[1:].strip()
    loading = bot.send_message(chat_id, "⌛", reply_to_message_id=reply_id)
    image_data = generate_image(prompt)
    bot.delete_message(chat_id=chat_id, message_id=loading.message_id)

    if image_data:
        sent_msg = bot.send_photo(chat_id=chat_id, photo=image_data, reply_to_message_id=reply_id)
        bot.send_message(chat_id=chat_id, text="اینم از تصویر مورد نظرت! 🎨", reply_to_message_id=sent_msg.message_id)
        user_stats.setdefault(user_id, {"total_images": 0})
        user_stats[user_id]["total_images"] += 1
        save_data()
    else:
        bot.send_message(chat_id=chat_id, text="نتوانستم تصویر را تولید کنم 😢", reply_to_message_id=reply_id)

@error_handler
def handle_message(update: Update, context: CallbackContext):
    load_data()
    if update.message:
        executor.submit(process_message, update, context)

def bug_report(update: Update, context: CallbackContext):
    update.message.reply_text("باگ دیدی؟!\nاشکالی نداره بهم بگو چی بود👇👇\n              @AmirStPlays")

# info func
def show_info(update: Update, context: CallbackContext):
    user = update.message.from_user
    user_id = str(user.id)
    
    # Initialize stats if not exists
    user_stats.setdefault(user_id, {
        "total_images": 0,
        "messages_sent": 0,
        "daily_voices": 0
    })
    
    stats = user_stats[user_id]
    
    info_text = (
        f"ℹ️ اطلاعات کاربر:\n"
        f"👤 نام: {user.first_name}\n"
        f"🌐 نام کاربری: @{user.username or 'ندارد'}\n"
        f"🆔 آیدی عددی: {user.id}\n"
        f"🖼️ تعداد عکس‌های ساخته شده: {stats['total_images']}"
    )
    update.message.reply_text(info_text)

def load_data():
    global user_stats, authenticated_users, user_memories
    # بارگذاری user_stats
    if os.path.exists("user_stats.json"):
        with open("user_stats.json", "r", encoding="utf-8") as f:
            user_stats = json.load(f)
    else:
        user_stats = {}
    
    for user_id in user_stats:
        user_stats[user_id].setdefault("total_images", 0)
        user_stats[user_id].setdefault("daily_image_analysis", 0)
    
    # بارگذاری authenticated_users
    if os.path.exists(AUTH_FILE):
        with open(AUTH_FILE, "r", encoding="utf-8") as f:
            authenticated_users = json.load(f)
    else:
        authenticated_users = {}

def send_channel_join_request(chat_id):
    keyboard = [
        [InlineKeyboardButton("عضویت در کانال", url=f"https://t.me/{CHANNEL_USERNAME[1:]}")],
        [InlineKeyboardButton("عضو شدم ✅", callback_data="check_membership")]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    bot.send_message(
        chat_id=chat_id,
        text="جهت ادامه در ربات ابتدا در کانال زیر عضو شوید:",
        reply_markup=reply_markup
    )

def save_data():
    with open("user_stats.json", "w", encoding="utf-8") as f:
        json.dump(user_stats, f, ensure_ascii=False, indent=2)

    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(authenticated_users, f, ensure_ascii=False, indent=2)
    
def is_user_authenticated(user_id):
    return str(user_id) in authenticated_users

def is_user_member_of_channel(user_id):
    try:
        chat_member = bot.get_chat_member(chat_id=CHANNEL_USERNAME, user_id=user_id)
        return chat_member.status in ["member", "administrator", "creator"]
    except Exception as e:
        print(f"⚠️ خطا در بررسی عضویت کاربر: {e}")
        return False

def request_phone_number(chat_id):
    keyboard = [[KeyboardButton("اشتراک‌گذاری شماره تلفن 📱", request_contact=True)]]
    reply_markup = ReplyKeyboardMarkup(keyboard, resize_keyboard=True, one_time_keyboard=True)
    bot.send_message(
        chat_id=chat_id,
        text="جهت ادامه، لطفاً شماره تلفن خود را اشتراک بگذارید.",
        reply_markup=reply_markup
    )

def check_membership_and_auth(update: Update, context: CallbackContext):
    user_id = update.message.from_user.id
    chat_id = update.message.chat_id
    user_text = update.message.text.strip()
    is_private = update.message.chat.type == "private"

    if not is_private and not user_text.startswith("/:"):
        return

    if not is_private:
        user_text = user_text[1:].strip()

    if not is_user_member_of_channel(user_id):
        send_channel_join_request(chat_id)
        return

    if not is_user_authenticated(user_id):
        request_phone_number(chat_id)
    else:
        handle_message(update, context)

def save_auth():
    with open(AUTH_FILE, "w", encoding="utf-8") as f:
        json.dump(authenticated_users, f, ensure_ascii=False, indent=2)

def handle_contact(update: Update, context: CallbackContext):
    contact = update.message.contact
    user_id = update.message.from_user.id
    phone_number = contact.phone_number
    chat_id = update.message.chat_id
    # ذخیره شماره تلفن
    authenticated_users[str(user_id)] = phone_number
    save_auth()
    # پیام تأیید به کاربر
    bot.send_message(
        chat_id=chat_id,
        text=f"✅ شماره تلفن شما ({phone_number}) با موفقیت ثبت شد. حالا می‌توانید از ربات استفاده کنید.",
        reply_markup=ReplyKeyboardRemove()  # حذف منوی اشتراک‌گذاری شماره تلفن
    )
    # نمایش پیام استارت
    start(chat_id, context)

def start(update: Update, context: CallbackContext):
    chat_id = update.message.chat_id
    if not is_user_member_of_channel(update.message.from_user.id):
        send_channel_join_request(chat_id)
    else:
        if not is_user_authenticated(update.message.from_user.id):
            request_phone_number(chat_id)
        else:
            update.message.reply_text(
                text="""درود بر تو 🫵
اگر برای تولید عکس اومدی باید بهت بگم که جای درستی رو انتخاب کردی 👌
برای تولید عکس کافیه که توی چت خصوصی متن بدی تا ربات برات عکسشو بسازه .
هر چقدر متنت جزئیاتش بیشتر باشه ; تصویر بهتری دریافت میکنی .🙂
ربات هیچگونه محدودیتی برای تولید عکس نداره🤨 و تنها محدودیت اون کلته 🧠
برای راهنمایی بیشتر از این /help رو بزن 😉
و راستی یه نکته اینکه اگر بتونی متنت رو انگلیسی بنویسی خیلی بهتره، شاید تو ندونی چرا ولی من این پشت میدونم😉
"""
            )

def show_help(update: Update, context: CallbackContext):
    help_text = (
        "📖 راهنمای استفاده از ربات:\n"
        """- در گروه‌ها، پیام‌ها باید با "/:" شروع شوند.\n"""
        "- برای تولید عکس کافیست تا به ربات متن خود را ارسال کنید تا برای شما عکس بسازد.\n"
        "- از دستور /help برای مشاهده این راهنما استفاده کنید.\n"
        "- از دستور /info برای مشاهده اطلاعات خود استفاده کنید."
    )
    update.message.reply_text(help_text)
                              
def main():
    load_data()
    updater = Updater(bot_token, use_context=True)
    dp = updater.dispatcher
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, check_membership_and_auth))
    dp.add_handler(MessageHandler(Filters.contact & Filters.private, handle_contact))

    dp.add_handler(CommandHandler("start", start))
    dp.add_handler(CommandHandler("help", show_help))
    dp.add_handler(CommandHandler("info", show_info))
    dp.add_handler(CommandHandler("bug", bug_report))
    dp.add_handler(MessageHandler(Filters.contact, handle_contact))
    dp.add_handler(MessageHandler(Filters.text & ~Filters.command, handle_message))


    updater.start_polling()
    updater.idle()
if __name__ == "__main__":
    main()



