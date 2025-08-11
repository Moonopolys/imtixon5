from telebot.types import Message

from data.loader import bot, db
from keyboards.default import main_buttons

@bot.message_handler(commands=["start"])
def show_genres(message):
    genres = db.get_genres()
    markup = main_buttons(
        [genre[1] for genre in genres],
        row_width=2,
        admin_id=message.from_user.id
    )
    bot.send_message(
        message.chat.id,
        "Ganre tanlang:",
        reply_markup=markup
    )