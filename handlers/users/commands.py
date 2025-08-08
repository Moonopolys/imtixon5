from telebot.types import Message

from data.loader import bot, db
from keyboards.default import main_buttons

@bot.message_handler(commands=["start"])
def start(message: Message):
    chat_id = message.chat.id
    user_name = message.from_user.full_name
    from_user_id = message.from_user.id
    text = f"Assalomu alaykum {user_name}\n\nBu kurslar toplangan bot"
    bot.send_message(chat_id, text, reply_markup=main_buttons([], admin_id=from_user_id))