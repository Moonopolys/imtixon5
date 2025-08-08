from typing import Optional
from telebot.types import ReplyKeyboardMarkup, KeyboardButton

from config import ADMINS


def main_buttons(names: list, row_width: int = 2, back: bool = False, admin_id: Optional[int] = None):
    markup = ReplyKeyboardMarkup(resize_keyboard=True, row_width=row_width)
    buttons = ["books", "genres"]
    for name in names:
        btn = KeyboardButton(name)
        buttons.append(btn)
    markup.add(*buttons)

    if admin_id in ADMINS:
        btn = KeyboardButton("️👮‍♂️Admin buyruqlari")
        markup.add(btn)

    if back:
        text = "⬅️Ortga"
        btn = KeyboardButton(text)
        markup.add(btn)

    return markup