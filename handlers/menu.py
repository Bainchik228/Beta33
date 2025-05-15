from aiogram import types
from bot import dp, bot
from keyboards import get_main_menu_keyboard

async def show_main_menu(message: types.Message):
    """Показывает главное меню бота"""
    keyboard = get_main_menu_keyboard()
    await message.answer("Главное меню:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "back_to_main")
async def back_to_main(callback_query: types.CallbackQuery):
    await show_main_menu(callback_query.message) 