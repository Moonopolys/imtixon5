from telebot.types import CallbackQuery, Message
from data.loader import bot, db
from keyboards.inline import books_page_buttons, book_images_buttons
from handlers.admins.text_handlers import BOOK


def get_books_page(page_number=1, items_per_page=5, genre_id=None):
    if genre_id:
        genre_name = db.get_genre_by_id(genre_id)[1]
        text_message = f"📚 Kitoblar janrda «{genre_name}»:\n\n"
        books = db.get_books_by_genre(genre_id, offset=(page_number - 1) * items_per_page, limit=items_per_page)
    else:
        text_message = "📚 Barcha kitoblar:\n\n"
        books = db.get_books(offset=(page_number - 1) * items_per_page, limit=items_per_page)

    for index, book in enumerate(books, start=(page_number - 1) * items_per_page + 1):
        _, title, author = book
        text_message += f"{index}. {title} — {author}\n"

    keyboard = books_page_buttons(page_number, items_per_page, genre_id)
    return text_message, keyboard

@bot.callback_query_handler(func=lambda call: call.data.startswith("books_page_"))
def reaction_to_books_page(call: CallbackQuery):
    chat_id = call.message.chat.id
    user_id = call.from_user.id
    parts = call.data.split("_")

    if "genre" in parts:
        page = int(parts[2])
        genre_id = int(parts[-1])
        books = db.get_books_by_genre(genre_id, offset=(page - 1) * 5, limit=5)
        genre_name = db.get_genre_by_id(genre_id)[1]
        text = f"📚 Kitoblar janrda «{genre_name}»:\n\n"
    else:
        page = int(parts[2])
        genre_id = None
        books = db.get_books(offset=(page - 1) * 5, limit=5)
        text = "📚 Barcha kitoblar:\n\n"

    bot.delete_message(chat_id, call.message.message_id)

    for idx, book in enumerate(books, start=(page - 1) * 5 + 1):
        id, title, author, info = book
        BOOK[user_id] = {
            "title": title,
            "author": author,
            "info": info
        }
        text += f"{idx}. {title} — {author}\n"

    bot.send_message(chat_id, text, reply_markup=books_page_buttons(page, 5, genre_id))


@bot.callback_query_handler(func=lambda call: "info_" in call.data)
def reaction_to_inline(call: CallbackQuery):
    chat_id = call.message.chat.id
    from_user_id = call.from_user.id
    bot.delete_message(chat_id, call.message.message_id)
    book_id = int(call.data.split("_")[1])
    title, author, info = db.get_book_details(book_id)
    text = f'''
<b>Nomi:</b> {title},
<b>Mu'olif:</b> {author},
<b>Haqida:</b> {info}.
'''
    buttons = call.message.reply_markup.keyboard[0]
    page = 1
    for button in buttons:
        if button.callback_data == "current_page":
            page = int(button.text.split("/")[0])

    image = db.get_book_image(book_id)
    markup = books_page_buttons(page, 5)
    bot.send_photo(chat_id, image, caption=text, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: "next_image_" in call.data)
def reaction_to_next_image(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, _, id, page = call.data.split("_")
    image, markup = book_images_buttons(int(id), int(page))
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_photo(chat_id, image, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data.startswith("prev_image_"))
def reaction_to_prev_image(call: CallbackQuery):
    chat_id = call.message.chat.id
    _, _, id, page = call.data.split("_")
    image, markup = book_images_buttons(int(id), int(page))
    bot.delete_message(chat_id, call.message.message_id)
    bot.send_photo(chat_id, image, reply_markup=markup)

@bot.callback_query_handler(func=lambda call: call.data == "back_to_books")
def reaction_to_back(call: CallbackQuery):
    chat_id = call.message.chat.id
    bot.delete_message(chat_id, call.message.message_id)
    books = db.get_books(offset=0, limit=5)
    text = "📚 Barcha kitoblar:\n\n"
    for idx, book in enumerate(books, start=1):
        _, title, author = book
        text += f"{idx}. {title} — {author}\n"
    bot.send_message(chat_id, text, reply_markup=books_page_buttons(1, 5))
