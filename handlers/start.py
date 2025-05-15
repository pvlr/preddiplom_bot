from aiogram import Router, F
from aiogram.types import Message
from database.db import Database
from keyboards.main import get_main_keyboard

router = Router()

def register_start_handlers(dp, db: Database):
    @router.message(F.text == "/start")
    async def cmd_start(message: Message):
        user_id = message.from_user.id
        username = message.from_user.username or ""
        full_name = message.from_user.full_name

        db.add_user(user_id, username, full_name)

        await message.answer(
            f"Здравствуйте, {full_name}!\n"
            f"В боте FreshMeal Вы можете посмотреть наше меню, узнать об акциях и оформить заказ с доставкой.\n"
            f"Используй меню ниже для навигации",
            reply_markup=get_main_keyboard()
        )

    dp.include_router(router)
