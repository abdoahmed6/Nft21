import logging
import requests
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application,
    CommandHandler,
    CallbackQueryHandler,
    MessageHandler,
    filters,
    CallbackContext,
)

logging.basicConfig(
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s", level=logging.INFO
)

API_URL = "https://api.coingecko.com/api/v3/simple/price?ids=the-open-network&vs_currencies=usd"

async def get_crypto_price():
    try:
        response = requests.get(API_URL)
        data = response.json()
        logging.info(f"API response: {data}")
        ton_price_usd = data.get('the-open-network', {}).get('usd')
        return ton_price_usd
    except Exception as e:
        logging.error(f"Error fetching price: {e}")
        return None

async def start(update: Update, context: CallbackContext):
    user_name = update.effective_user.first_name
    keyboard = [
        [InlineKeyboardButton("𝗗𝗘𝗩👨🏼‍💻", url="tg://resolve?domain=GuSt3bDo"),
         InlineKeyboardButton("𝗢𝗪𝗡𝗘𝗥🕶", url="tg://resolve?domain=GuSt3bDo")],
        [InlineKeyboardButton("𝗛𝗘𝗟𝗣", callback_data='help')]
    ]
    reply_markup = InlineKeyboardMarkup(keyboard)
    welcome_message = (
        f"Welcome, {user_name}!\n"
        "~ Start search and get info from NFT user\n"
        "~ Use HELP to see Commands"
    )
    await update.message.reply_text(welcome_message, reply_markup=reply_markup)

async def help_button(update: Update, context: CallbackContext):
    query = update.callback_query
    await query.answer()
    keyboard = [[InlineKeyboardButton("Back", callback_data='back')]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    help_text = (
        "COMMANDS:\n"
        "~ /start to see start message\n"
        "~ /mode to change use mode for sudo\n\n"
        "USAGE:\n"
        "~ add bot to group & send user with @\n"
        "~ send user with @ in bot private"
    )
    await query.edit_message_text(text=help_text, reply_markup=reply_markup)

async def handle_messages(update: Update, context: CallbackContext):
    text = update.message.text.lower()

    if any(word in text for word in ["id", "/id", "أيدي", "ايدي", "Id", "iD"]):
        user_id = update.effective_user.id
        keyboard = [
            [InlineKeyboardButton("انسخ الايدي👆", callback_data='copy_id')]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"الايدي بتاعك:\n`{user_id}`", parse_mode="Markdown", reply_markup=reply_markup
        )
        return

    if "منصه" in text:
        await update.message.reply_text("https://fragment.com/")
        return

    if "مطور البوت" in text or "المطور" in text:
        keyboard = [
            [InlineKeyboardButton("𝗮𝗯𝗱𝗲𝗹𝗿𝗮𝗵𝗺𝗮𝗻", url="https://t.me/GuSt3bDo")]
        ]
        reply_markup = InlineKeyboardMarkup(keyboard)
        caption = (
            "❲ Developers Bot ❳\n"
            "— — — — — — — — —\n"
            "𖥔 Dev Name : ˛ 𝗮𝗯𝗱𝗲𝗹𝗿𝗮𝗵𝗺𝗮𝗻\n"
            "𖥔 Dev Bio : لٰا شۨيٰء يـدۅم."
        )
        await update.message.reply_photo(
            photo="https://pin.it/27R70Jvvs",
            caption=caption,
            reply_markup=reply_markup
        )
        return

    if "تون" in text or "ton" in text:
        price = await get_crypto_price()
        if price is not None:
            message = f"{price}$"
        else:
            message = "حدث خطأ في جلب السعر!"
        await update.message.reply_text(message)
        return

def main():
    application = Application.builder().token("7725254743:AAEWSU6jbOKCCCy9t0q_HIy5H8IiMLMwf2w").build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(help_button, pattern='help'))
    application.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_messages))
    application.run_polling()

if __name__ == '__main__':
    main()
