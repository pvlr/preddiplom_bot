from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from database.memory_cart import MemoryCart

router = Router()

def register_menu_handlers(dp, db: Database, cart: MemoryCart):
    @router.message(F.text == "🧾 Меню" or F.text == "/menu")
    async def show_menu(message: Message):
        products = db.get_menu()
        if not products:
            await message.answer("Меню пока пустое.")
            return

        for item in products:
            kb = InlineKeyboardMarkup(inline_keyboard = [
                [InlineKeyboardButton(text = "Добавить в корзину", callback_data = f"add:{item['id']}")]
            ])
            await message.answer(
                f"<b>{item['name']}</b>\n{item['description'] or 'Без описания'}\nЦена: {item['price']} ₽",
                reply_markup = kb
            )

    @router.message(F.text == "🛍 Акции" or "/sales")
    async def show_promos(message: Message):
        promos = db.get_promos()
        if not promos:
            await message.answer("Нет активных акций")
            return

        for item in promos:
            await message.answer(
                f"🎁 <b>{item['name']}</b>\n{item['description'] or 'Без описания'}\nСкидочная цена: {item['price']} ₽"
            )

    @router.callback_query(F.data.startswith("add:"))
    async def add_to_cart(callback: CallbackQuery):
        product_id = int(callback.data.split(":")[1])
        product = db.get_product_info(product_id)

        if not product:
            await callback.answer("Товар не найден", show_alert = True)
            return

        cart.add_item(
            user_id = callback.from_user.id,
            item = {
                "product_id": product["id"],
                "name": product["name"],
                "price": product["price"],
                "quantity": 1
            }
        )
        await callback.answer(f"Добавлено: {product['name']}")

    dp.include_router(router)

