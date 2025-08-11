from telebot.types import Message, ReplyKeyboardRemove
from data.loader import bot, db
from keyboards.default import main_buttons
from config import ADMINS

admin_buttons_name = [
    "➕ Kitob qo'shihs",
    "➕ Janr qo'shish",
    "✏️ Kitob O'zgartirish",
    "✏️ Janr O'zgartirish",
    "🗑 Kitob O'chirish",
    "🗑 Janr O'chirish"
]

BOOK = {}
GENRES = {}


@bot.message_handler(func=lambda message: message.text == "️👮‍♂️Admin buyruqlari")
def reaction_to_admin_commands(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        bot.send_message(chat_id, "️👮‍♂️️Admin buyruqlari",
            reply_markup=main_buttons(admin_buttons_name, back=True)
        )


@bot.message_handler(func=lambda message: message.text == "➕ Kitob qo'shihs")
def add_book_start(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Kitob nomini kiriting", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_name_book)


def get_name_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    BOOK[from_user_id] = {"title": message.text}
    msg = bot.send_message(chat_id, "Muallifni kiriting")
    bot.register_next_step_handler(msg, get_auth_name)


def get_auth_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    BOOK[from_user_id]["author"] = message.text
    msg = bot.send_message(chat_id, "Kitobga qisqacha tarif bering")
    bot.register_next_step_handler(msg, get_info_book)


def get_info_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    BOOK[from_user_id]["info"] = message.text

    genres = db.get_genres()
    genre_names = [g[1] for g in genres]

    msg = bot.send_message(
        chat_id,
        "Janr tanlang:",
        reply_markup=main_buttons(genre_names)
    )
    bot.register_next_step_handler(msg, get_genre_for_book)


def get_genre_for_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    genre_name = message.text
    genre = db.get_genre_id_by_name(genre_name)

    if not genre:
        msg = bot.send_message(chat_id, "❌Bunday janr yo'q. Boshqa tanlang")
        bot.register_next_step_handler(msg, get_genre_for_book)
        return

    BOOK[from_user_id]["genre_id"] = genre[0]

    msg = bot.send_message(chat_id, "Kitobni rasimini linkini yuboring", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(msg, get_image_book)

def get_image_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if not BOOK[from_user_id].get("images"):
        BOOK[from_user_id]['images'] = [message.text]
    else:
        BOOK[from_user_id]['images'].append(message.text)
    msg = bot.send_message(chat_id, "Yana rasm qo'shasizmi?", reply_markup=main_buttons(["Yes", "No"]))
    bot.register_next_step_handler(msg, save_book)

def save_book(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if message.text == "No":
        title = BOOK[from_user_id]["title"]
        auth = BOOK[from_user_id]["author"]
        info = BOOK[from_user_id]["info"]
        genre_id = BOOK[from_user_id]["genre_id"]
        images = BOOK[from_user_id]["images"]

        book_id = db.insert_book(title, auth, info, genre_id)

        for image in images:
            db.insert_image(image, book_id)

        del BOOK[from_user_id]
        bot.send_message(chat_id, "✅ Kitob saqlandi!", reply_markup=main_buttons(admin_buttons_name, back=True))
    else:
        msg = bot.send_message(chat_id, "Kitob rasmini linkini yuboring:", reply_markup=ReplyKeyboardRemove())
        bot.register_next_step_handler(msg, get_image_book)

# --------  GENRE QOSHISH  -----------
@bot.message_handler(func=lambda message: message.text == "➕ Janr qo'shish")
def reaction_to_admin(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if from_user_id in ADMINS:
        msg = bot.send_message(chat_id, "Janr nomini kiriting")
        bot.register_next_step_handler(msg, get_genre_name)


def get_genre_name(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    if from_user_id not in GENRES:
        GENRES[from_user_id] = []

    GENRES[from_user_id].append(message.text)


    msg = bot.send_message(chat_id, "Yana janr qo'shasizmi?", reply_markup=main_buttons(["Yes", "No"]))
    bot.register_next_step_handler(msg, save_genre)

def save_genre(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id

    if message.text == "No":

        for genre_name in GENRES[from_user_id]:
            db.insert_genre(genre_name)

        del GENRES[from_user_id]
        bot.send_message(chat_id, "Janrlar muvaffaqiyatli saqlandi!!!✅", reply_markup=main_buttons(admin_buttons_name, back=True))
    elif message.text == 'Yes':
        msg = bot.send_message(chat_id, "Janr nomini kiriting")
        bot.register_next_step_handler(msg, get_genre_name)



@bot.message_handler(func=lambda message: message.text == "⬅️Ortga")
def reaction_to_back(message: Message):
    chat_id = message.chat.id
    from_user_id = message.from_user.id
    genres = db.get_genres()
    markup = main_buttons(
        [genre[1] for genre in genres],
        row_width=2,
        admin_id=from_user_id
    )
    bot.send_message(chat_id, "Genre tanlang:", reply_markup=markup)

# --------  KITOB O'ZGARTIRISH -----------
@bot.message_handler(func=lambda m: m.text == "✏️ Kitob O'zgartirish")
def edit_book_start(message: Message):
    from_user_id = message.from_user.id
    if from_user_id in ADMINS:
        msg = bot.send_message(message.chat.id, "O'zgartirish uchun kitob nomini kiriting:")
        bot.register_next_step_handler(msg, get_book_title_for_edit)


def get_book_title_for_edit(message: Message):
    from_user_id = message.from_user.id
    BOOK[from_user_id] = {"title_search": message.text}
    msg = bot.send_message(message.chat.id, "Kitob muallifini kiriting:")
    bot.register_next_step_handler(msg, get_book_author_for_edit)


def get_book_author_for_edit(message: Message):
    from_user_id = message.from_user.id
    BOOK[from_user_id]["author_search"] = message.text
    book = db.get_book_by_title_author(
        BOOK[from_user_id]["title_search"],
        BOOK[from_user_id]["author_search"]
    )
    if not book:
        BOOK.pop(from_user_id)
        bot.send_message(message.chat.id, "❌ Bunday kitob topilmadi.")
        return

    BOOK[from_user_id]["id"] = book[0]
    msg = bot.send_message(message.chat.id, "Yangi nomni kiriting:")
    bot.register_next_step_handler(msg, edit_book_title)


def edit_book_title(message: Message):
    from_user_id = message.from_user.id

    BOOK[from_user_id]["title"] = message.text
    msg = bot.send_message(message.chat.id, "Yangi muallifni kiriting:")
    bot.register_next_step_handler(msg, edit_book_author)


def edit_book_author(message: Message):
    from_user_id = message.from_user.id
    BOOK[from_user_id]["author"] = message.text
    msg = bot.send_message(message.chat.id, "Yangi ma'lumotni kiriting:")
    bot.register_next_step_handler(msg, edit_book_info)


def edit_book_info(message: Message):
    from_user_id = message.from_user.id
    BOOK[from_user_id]["info"] = message.text
    book = BOOK.pop(from_user_id)
    db.update_book(book["id"], book["title"], book["author"], book["info"])
    bot.send_message(message.chat.id, "✅ Kitob yangilandi!", reply_markup=main_buttons(admin_buttons_name, back=True))


# ----------- KITOB O'CHIRISH ------------
@bot.message_handler(func=lambda m: m.text == "🗑 Kitob O'chirish")
def del_book_start(message: Message):
    if message.from_user.id in ADMINS:
        msg = bot.send_message(message.chat.id, "O'chirish uchun kitob nomini kiriting:")
        bot.register_next_step_handler(msg, get_book_title_for_del)


def get_book_title_for_del(message: Message):
    BOOK[message.from_user.id] = {"title_search": message.text}
    msg = bot.send_message(message.chat.id, "Kitob muallifini kiriting:")
    bot.register_next_step_handler(msg, get_book_author_for_del)


def get_book_author_for_del(message: Message):
    BOOK[message.from_user.id]["author_search"] = message.text
    book = db.get_book_by_title_author(
        BOOK[message.from_user.id]["title_search"],
        BOOK[message.from_user.id]["author_search"]
    )
    if not book:
        BOOK.pop(message.from_user.id, None)
        bot.send_message(message.chat.id, "❌ Bunday kitob topilmadi.")
        return

    db.delete_book(book[0])
    BOOK.pop(message.from_user.id, None)
    bot.send_message(message.chat.id, "✅ Kitob o'chirildi!", reply_markup=main_buttons(admin_buttons_name, back=True))


# ----------------- JANR O'ZGARTIRISH --------------------
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

@bot.message_handler(func=lambda message: message.text == "✏️ Janr O'zgartirish")
def start_edit_genre(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    if from_user_id in ADMINS:
        genres = db.get_genres()
        markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
        for _, genre_name in genres:
            markup.add(KeyboardButton(genre_name))
        markup.add(KeyboardButton("⬅️ Ortga"))
        bot.send_message(chat_id, "O'zgartirmoqchi bo'lgan janrni tanlang:", reply_markup=markup)
        bot.register_next_step_handler(message, choose_genre_to_edit)

def choose_genre_to_edit(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    genre_name = message.text
    if genre_name == "⬅️ Ortga":
        bot.send_message(chat_id, "Asosiy menyu", reply_markup=main_buttons(admin_buttons_name, back=True))
        return
    genre = db.get_genre_id_by_name(genre_name)
    GENRES[from_user_id] = {"id": genre}
    bot.send_message(chat_id, "Yangi janr nomini kiriting:", reply_markup=ReplyKeyboardRemove())
    bot.register_next_step_handler(message, save_new_genre_name)

def save_new_genre_name(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    new_name = message.text.strip()
    genre_id = GENRES[from_user_id]["id"]
    db.update_genre(new_name, genre_id)
    bot.send_message(chat_id, "✅ Janr muvaffaqiyatli o'zgartirildi!", reply_markup=main_buttons(admin_buttons_name, back=True))
    GENRES.pop(from_user_id)

# --------------------- JANR O'CHIRISH ----------------------------
@bot.message_handler(func=lambda m: m.text == "🗑 Janr O'chirish")
def delete_genre_start(message: Message):
    from_user_id = message.from_user.id
    chat_id = message.chat.id
    if from_user_id in ADMINS:
        genres = db.get_genres()
        genre_names = [f"{g[0]} - {g[1]}" for g in genres]
        msg = bot.send_message(chat_id, "O'chirish uchun janrni tanlang:",
                               reply_markup=main_buttons(genre_names, back=True))
        bot.register_next_step_handler(msg, confirm_delete_genre)

def confirm_delete_genre(message: Message):
    chat_id = message.chat.id

    parts = message.text.split(" - ")

    genre_id = int(parts[0])
    db.delete_genre(genre_id)
    bot.send_message(chat_id, "✅ Janr o'chirildi!", reply_markup=main_buttons(admin_buttons_name, back=True))

