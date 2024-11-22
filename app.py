from datetime import datetime, timezone
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup, InputMediaVideo, InputMediaPhoto, InputMediaAnimation, CallbackQuery
from telegram.ext import ApplicationBuilder, CallbackQueryHandler, CommandHandler, ContextTypes
import requests
import logging
import asyncio

# Set up logging
logging.basicConfig(
    format='%(asctime)s - %(name)s - %(levelname)s',
    level=logging.INFO
)

logger = logging.getLogger(__name__)

# Bitly access token and link
bitly_access_token = "ff565d00c7ea0bd23670a3ecf1be5d035536a709"
bitly_link = "https://bit.ly/3Udxzk9"

# First container pages (Login and Page 1)
container1_pages = [
    {
        "image": "https://imgur.com/a/ycWQ7fs.jpeg",
        "text": "Hi there, cutie! 💖\n\nSo happy to see you here! Get comfy, and let's dive into something fun together! 🌟\n\nI've got some adorable surprises waiting just for you! 😘✨",
        "type": "photo"
    },
    {
        "gif": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExdnN1a3FybnJ6b29qMzFjb200NWsyZHVlZ3NtN3ltNWZ6N250cmZtcyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/hlhvi4cqSR73BdsBza/giphy.gif",
        "text": "Hey there, beautiful! 💋 Ready to explore some tempting surprises? Let's make it a fun ride! 😉",
        "type": "animation"
    }
]

# Second container pages (Verification and Language Selection)
container2_pages = [
    {
        "gif": "https://i.giphy.com/media/v1.Y2lkPTc5MGI3NjExaHdiazI2Y3A3d3N2OHJtMXd2YzBhb2RxM2NrM3Rscnpwc29tYWh3ZyZlcD12MV9pbnRlcm5hbF9naWZfYnlfaWQmY3Q9Zw/roFcvZ66RArp8ifVFP/giphy-downsized-large.gif",
        "text": "Want to unlock exclusive, private treasures? Just verify your access, and let the fun begin! 💖✨"
    },
    {
        "gif": "https://media.giphy.com/media/QRNEol60rQ0bbtY0Q4/giphy.gif",
        "text": "Hey there, you naughty thing! 😉\n\nLet's get this party started! 💖\n\nChoose what feels right, and let the fun begin, cutie! 🌍✨"
    }
]

# Global trackers for current pages
current_container1_page = 0
current_container2_page = 0

async def update_container1(query: CallbackQuery, page: int):
    global current_container1_page
    current_container1_page = page
    
    if page == 0:
        keyboard = [[InlineKeyboardButton("Login 🔐", callback_data="login_process")]]
    else:
        keyboard = [[InlineKeyboardButton("Get Started 🚀", callback_data="open_container2")]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    if container1_pages[page]["type"] == "photo":
        media = InputMediaPhoto(
            media=container1_pages[page]["image"],
            caption=container1_pages[page]["text"]
        )
    else:
        media = InputMediaAnimation(
            media=container1_pages[page]["gif"],
            caption=container1_pages[page]["text"]
        )
    
    await query.message.edit_media(media=media, reply_markup=reply_markup)

async def show_loading_animation(message):
    loading_text = "Loading... [□□□□□□□□□□] 0%"
    loading_message = await message.reply_text(loading_text)
    
    for i in range(1, 11):
        percentage = i * 10
        blocks = "■" * i + "□" * (10 - i)
        await loading_message.edit_text(f"Loading... [{blocks}] {percentage}%")
        await asyncio.sleep(0.5)
    
    await loading_message.delete()
    return True

async def show_dialog(message, text, is_success=True):
    emoji = "✅" if is_success else "❌"
    box_top = "╔" + "═" * 50 + "╗"
    box_bottom = "╚" + "═" * 50 + "╝"
    dialog_text = f"""
{box_top}
║ {emoji} NOTIFICATION {emoji}
║
║ {text}
{box_bottom}
"""
    await message.reply_text(dialog_text, parse_mode='Markdown')

async def start(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_container1_page
    current_container1_page = 0
    keyboard = [[InlineKeyboardButton("Login 🔐", callback_data="login_process")]]
    reply_markup = InlineKeyboardMarkup(keyboard)
    await update.message.reply_photo(
        photo=container1_pages[0]["image"],
        caption=container1_pages[0]["text"],
        reply_markup=reply_markup
    )

async def update_container2(query: CallbackQuery, page: int):
    global current_container2_page
    current_container2_page = page
    
    if page == 0:
        keyboard = [
            [InlineKeyboardButton("Verify ✅", url=bitly_link),
             InlineKeyboardButton("How to Verify ❓", callback_data="how_to_verify")],
            [InlineKeyboardButton("Get Access 🔑", callback_data="get_access")]
        ]
    else:
        keyboard = [[
            InlineKeyboardButton("Hindi 🇮🇳", callback_data="hindi"),
            InlineKeyboardButton("English 🇬🇧", callback_data="english"),
            InlineKeyboardButton("Arabic 🇸🇦", callback_data="arabic")
        ]]
    
    reply_markup = InlineKeyboardMarkup(keyboard)
    
    media = InputMediaAnimation(
        media=container2_pages[page]["gif"],
        caption=container2_pages[page]["text"]
    )
    
    await query.message.edit_media(media=media, reply_markup=reply_markup)

async def button_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    global current_container1_page, current_container2_page
    query = update.callback_query
    await query.answer()

    if query.data == "login_process":
        loading_success = await show_loading_animation(query.message)
        if loading_success:
            await update_container1(query, 1)
        return

    if query.data == "open_container2":
        current_container2_page = 0
        await update_container2(query, 0)
        return

    if query.data == "how_to_verify":
        verify_text = (
            "Hey there, sweetie! 🍭\n\n"
            "• First, click on 'Verify' to begin your journey! 💕\n\n"
            "• You'll be taken to a cute bot. Inside, join the channel and spin the wheel for fun! 🎡\n\n"
            "• Once you've spun the wheel, come back here to continue!\n\n"
            "• Click 'Verify' again, and get ready for some super spicy surprises! 😉🌶️"
        )
        await query.message.reply_photo(
            photo="https://imgur.com/a/ycWQ7fs.jpeg",
            caption=verify_text
        )
        return

    if query.data == "get_access":
        if await verify_bitly_link(context.user_data):
            await show_dialog(
                query.message,
                "Yea Bro you done it thank you, if you are weak u cant even watch the video fully 💪 Good luck 🍀",
                True
            )
            await update_container2(query, 1)
        else:
            await show_dialog(
                query.message,
                "Hey honey, are u trying to trick me huh? 😏 Complete the task to get butterflies inside your whole body 🦋😉",
                False
            )
        return

    if query.data in ["english", "hindi", "arabic"]:
        await send_language_content(query, query.data)

async def verify_bitly_link(user_data):
    try:
        response = requests.get(bitly_link)
        return response.status_code == 200
    except requests.exceptions.RequestException:
        return False

async def send_language_content(query: CallbackQuery, language: str):
    content = {
        "english": {
            "caption": "John in his Revelation says that the sexually immoral shall have their part with murderers, sorcerers, enchanters, liars, idolators and such others, in the lake which burns with fire and brimstone, which is the second death (Revelation 21:8).",
            "video": "https://drive.google.com/uc?id=101PjHH-3pL6xPLZZMAlGYvMsnA2fBWMg"
        },
        "arabic": {
            "caption": "سَبَبُ الشَّـرِّ غَلَبَةُ الشَّهْوَةِ",
            "video": "https://drive.google.com/uc?id=109oKbal4EPY5_c-hg8jmQJ5nrUlztSNy"
        },
        "hindi": {
            "caption": "BG 3.37: The Supreme Lord said: It is lust alone, which is born of contact with the mode of passion, and later transformed into anger. Know this as the sinful, all-devouring enemy in the world.",
            "video": "https://drive.google.com/uc?id=105lBd5vGLO7_LVNXlB_2IqlEBH6Spcze"
        }
    }
    
    if language in content:
        await query.message.reply_video(
            video=content[language]["video"],
            caption=content[language]["caption"]
        )

def main():
    application = ApplicationBuilder().token('7698667294:AAHz6uWANG6DxpwkCT-HkeCgPyIcHDB-yj4').build()
    application.add_handler(CommandHandler("start", start))
    application.add_handler(CallbackQueryHandler(button_handler))
    application.run_polling()

if __name__ == "__main__":
    main()