from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
from data.loader import db

def books_page_buttons(page=1, per_page=5, genre_id=None):
    markup = InlineKeyboardMarkup(row_width=1)
    if genre_id:
        total_books = db.count_books_by_genre(genre_id)
        books = db.get_books_by_genre(genre_id, offset=(page - 1) * per_page, limit=per_page)
    else:
        total_books = db.count_books()
        books = db.get_books(offset=(page - 1) * per_page, limit=per_page)

    total_pages = (total_books + per_page - 1) // per_page

    for index, book in enumerate(books, start=(page - 1) * per_page + 1):
        book_id, title, _ = book
        markup.add(InlineKeyboardButton(f"{index}.", callback_data=f"info_{book_id}"))

    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"books_page_{page - 1}_genre_{genre_id}" if genre_id else f"books_page_{page - 1}"))
    nav.append(InlineKeyboardButton(f"{page}/{total_pages}", callback_data="noop"))
    if page < total_pages:
        nav.append(InlineKeyboardButton("➡️", callback_data=f"books_page_{page + 1}_genre_{genre_id}" if genre_id else f"books_page_{page + 1}"))

    if nav:
        markup.row(*nav)

    return markup

def book_images_buttons(book_id, page=1):
    markup = InlineKeyboardMarkup()
    total_images = db.count_images(book_id)
    per_page = 1
    offset = (page - 1) * per_page
    image_data = db.select_image_by_pagination(book_id, offset, per_page)
    nav = []
    if page > 1:
        nav.append(InlineKeyboardButton("⬅️", callback_data=f"prev_image_{book_id}_{page - 1}"))
    nav.append(InlineKeyboardButton(f"{page}/{total_images}", callback_data="noop"))
    if page < total_images:
        nav.append(InlineKeyboardButton("➡️", callback_data=f"next_image_{book_id}_{page + 1}"))
    if nav:
        markup.row(*nav)
    markup.add(InlineKeyboardButton("ℹ️", callback_data=f"info_{book_id}_{page}"))
    markup.add(InlineKeyboardButton("🔙 Orqaga", callback_data="back_to_books"))
    return (image_data[1] if image_data else None), markup
