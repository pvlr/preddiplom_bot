from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

def get_main_keyboard():
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text="🧾 Меню"), KeyboardButton(text="🛍 Акции")],
            [KeyboardButton(text="🛒 Корзина")],
        ],
        resize_keyboard=True
    )
