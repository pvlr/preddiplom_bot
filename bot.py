# framework
import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.types import Message
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.enums import ParseMode
from aiogram.client.default import DefaultBotProperties

# memory
from config import load_config
from database.db import Database
from database.memory_cart import MemoryCart

# handlers
from handlers.start import register_start_handlers
from handlers.menu import register_menu_handlers
from handlers.cart import register_cart_handlers


# initialization
async def main():
    config = load_config()

    # bot
    bot = Bot(token=config.bot_token, default=DefaultBotProperties(parse_mode="HTML"))
    dp = Dispatcher(storage = MemoryStorage())

    # db & cart
    db = Database(config.db_path)
    cart = MemoryCart()

    # handlers
    register_start_handlers(dp, db)
    register_menu_handlers(dp, db, cart)
    register_cart_handlers(dp, db, cart)

    print("-Бот запущен-")

    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
