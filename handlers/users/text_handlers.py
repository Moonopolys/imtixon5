from data.loader import bot, db
from .callbacks import get_books_page


@bot.message_handler(func=lambda message: message.text in [genre[1] for genre in db.get_genres()])
def show_books_by_genre(message):
    all_genres = db.get_genres()

    genre_id = None
    for genre in all_genres:
        if genre[1] == message.text:
            genre_id = genre[0]
            break

    if genre_id:
        text_message, keyboard = get_books_page(page_number=1, items_per_page=5, genre_id=genre_id)

        bot.send_message(message.chat.id, text_message, reply_markup=keyboard)
    else:
        bot.send_message(message.chat.id, "❌ В этом жанре книг пока нет.")
