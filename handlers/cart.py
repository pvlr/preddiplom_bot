from aiogram import Router, F
from aiogram.types import Message, CallbackQuery, InlineKeyboardMarkup, InlineKeyboardButton
from database.db import Database
from database.memory_cart import MemoryCart

router = Router()

def register_cart_handlers(dp, db: Database, cart: MemoryCart):
    
    async def render_cart(user_id: int, target):
        items = cart.get_cart(user_id)

        if not items:
            await target.answer("Ваша корзина пуста ☹️")
            return

        text = "<b>🛒 Ваша корзина:</b>\n\n"
        total = 0
        kb = []

        for i, item in enumerate(items, 1):
            subtotal = item['price'] * item['quantity']
            total += subtotal
            text += (
                f"{i}. <b>{item['name']}</b> - {item['quantity']} шт. × {item['price']} ₽ = {subtotal:.2f} ₽\n"
            )
            kb.append([
                InlineKeyboardButton(
                    text=f"Удалить {item['name']}",
                    callback_data=f"remove:{item['product_id']}"
                )
            ])

        text += f"\nИтого: <b>{total:.2f} ₽</b>"
        kb.append([InlineKeyboardButton(text="✅ Оформить заказ", callback_data="order_confirm")])

        await target.answer(text, reply_markup=InlineKeyboardMarkup(inline_keyboard=kb), parse_mode="HTML")

    @router.message(F.text == "🛒 Корзина" or "/cart")
    async def cart_button(message: Message):
        await render_cart(message.from_user.id, message)


    @router.callback_query(F.data.startswith("remove:"))
    async def remove_item(callback: CallbackQuery):
        product_id = int(callback.data.split(":")[1])
        cart.remove_item(callback.from_user.id, product_id)
        await callback.answer("Товар удален из корзины")
        await render_cart(callback.from_user.id, callback.message)

    @router.callback_query(F.data == "order_confirm")
    async def confirm_order(callback: CallbackQuery):
        user_id = callback.from_user.id
        items = cart.get_cart(user_id)

        if not items:
            await callback.answer("Ваша корзина пуста", show_alert=True)
            return

        order_id = db.create_order(user_id)
        for item in items:
            db.add_order_item(order_id, item['product_id'], item['quantity'])

        cart.clear_cart(user_id)
        await callback.message.answer("✅ Ваш заказ оформлен! Мы скоро с вами свяжемся")

    dp.include_router(router)
