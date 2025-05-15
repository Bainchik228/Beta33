from aiogram import types
from aiogram.fsm.context import FSMContext

from bot import dp, bot
from states import ReviewState
from database import Review, get_session
from keyboards import (
    get_photo_choice_keyboard,
    get_rating_keyboard,
    get_confirm_review_keyboard
)
from handlers.menu import show_main_menu

@dp.callback_query(lambda c: c.data == "leave_review")
async def start_review(callback_query: types.CallbackQuery, state: FSMContext):
    # Добавляем кнопку отмены
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_review_process")]
    ])
    await callback_query.message.edit_text("Напиши свой отзыв о школьной столовой или нажми кнопку отмены:", reply_markup=keyboard)
    await state.set_state(ReviewState.waiting_for_text)

@dp.message(ReviewState.waiting_for_text)
async def process_review_text(message: types.Message, state: FSMContext):
    await state.update_data(review_text=message.text)
    
    keyboard = get_photo_choice_keyboard()
    
    # Модифицируем клавиатуру, добавляя кнопку отмены
    inline_keyboard = keyboard.inline_keyboard
    inline_keyboard.append([types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_review_process")])
    modified_keyboard = types.InlineKeyboardMarkup(inline_keyboard=inline_keyboard)
    
    await message.answer("Хочешь добавить фото к отзыву?", reply_markup=modified_keyboard)
    await state.set_state(ReviewState.waiting_for_photo)

@dp.callback_query(lambda c: c.data == "add_photo")
async def request_photo(callback_query: types.CallbackQuery):
    # Добавляем кнопку отмены при запросе фотографии
    keyboard = types.InlineKeyboardMarkup(inline_keyboard=[
        [types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_review_process")]
    ])
    await callback_query.message.edit_text("Отправь фото к своему отзыву или нажми кнопку отмены:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "cancel_review_process")
async def cancel_review_process(callback_query: types.CallbackQuery, state: FSMContext):
    await callback_query.message.edit_text("Написание отзыва отменено.")
    await show_main_menu(callback_query.message)
    await state.clear()

@dp.callback_query(lambda c: c.data == "skip_photo")
async def skip_photo(callback_query: types.CallbackQuery, state: FSMContext):
    await state.update_data(photo_id=None)
    await request_rating(callback_query.message)

@dp.message(ReviewState.waiting_for_photo)
async def process_review_photo(message: types.Message, state: FSMContext):
    if message.photo:
        photo_id = message.photo[-1].file_id
        await state.update_data(photo_id=photo_id)
        await request_rating(message)
    else:
        await message.answer("Пожалуйста, отправь фото или нажми кнопку 'Нет', чтобы пропустить.")

async def request_rating(message: types.Message):
    keyboard = get_rating_keyboard()
    await message.answer("Оцени столовую от 1 до 5 звезд:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("rating_"))
async def process_rating(callback_query: types.CallbackQuery, state: FSMContext):
    rating = int(callback_query.data.replace("rating_", ""))
    await state.update_data(rating=rating)
    
    data = await state.get_data()
    review_text = data.get("review_text")
    photo_id = data.get("photo_id")
    
    # Формируем сообщение с предпросмотром отзыва
    preview_text = f"Твой отзыв:\n\n{review_text}\n\nОценка: {rating*'⭐'}"
    
    keyboard = get_confirm_review_keyboard()
    
    # Удаляем предыдущее сообщение в любом случае для единообразия
    await callback_query.message.delete()
    
    if photo_id:
        # Если есть фото, отправляем его с текстом
        sent_message = await bot.send_photo(
            chat_id=callback_query.from_user.id,
            photo=photo_id,
            caption=preview_text,
            reply_markup=keyboard
        )
    else:
        # Если фото нет, просто отправляем текст
        sent_message = await bot.send_message(
            chat_id=callback_query.from_user.id,
            text=preview_text,
            reply_markup=keyboard
        )
    
    # Сохраняем ID отправленного сообщения
    await state.update_data(preview_message_id=sent_message.message_id)
    await state.set_state(ReviewState.confirm_review)

@dp.callback_query(lambda c: c.data == "confirm_review")
async def save_review(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    review_text = data.get("review_text")
    photo_id = data.get("photo_id")
    rating = data.get("rating")
    
    session = get_session()
    new_review = Review(
        user_id=callback_query.from_user.id,
        text=review_text,
        rating=rating,
        photo_id=photo_id
    )
    
    session.add(new_review)
    session.commit()
    session.close()
    
    # Удаляем текущее сообщение чтобы избежать ошибок при редактировании
    await callback_query.message.delete()
    
    # Отправляем новое сообщение с подтверждением
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Спасибо за твой отзыв! Он поможет нам стать лучше."
    )
    
    await show_main_menu(callback_query.message)
    await state.clear()

@dp.callback_query(lambda c: c.data == "cancel_review")
async def cancel_review(callback_query: types.CallbackQuery, state: FSMContext):
    # Удаляем текущее сообщение чтобы избежать ошибок при редактировании
    await callback_query.message.delete()
    
    # Отправляем новое сообщение
    await bot.send_message(
        chat_id=callback_query.from_user.id,
        text="Отзыв отменен."
    )
    
    await show_main_menu(callback_query.message)
    await state.clear() 