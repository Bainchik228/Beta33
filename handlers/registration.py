from aiogram import types
from aiogram.fsm.context import FSMContext
from aiogram.filters import CommandStart

from bot import dp, bot
from states import RegisterState
from database import User, get_session
from keyboards import (
    get_class_keyboard_1_9,
    get_class_keyboard_5_9,
    get_class_keyboard_10_11,
    get_confirm_class_keyboard,
    get_main_menu_keyboard
)

from handlers.menu import show_main_menu

@dp.message(CommandStart())
async def cmd_start(message: types.Message, state: FSMContext):
    session = get_session()
    user = session.query(User).filter(User.user_id == message.from_user.id).first()
    
    if user:
        await message.answer(f"Привет, {user.full_name}! Ты уже зарегистрирован в классе {user.class_name}.")
        await show_main_menu(message)
    else:
        await message.answer(f"Добро пожаловать в бот школьной столовой, {message.from_user.full_name}! Для начала нужно зарегистрироваться.")
        await register_user(message, state, is_change=False)
    
    session.close()

async def register_user(message: types.Message, state: FSMContext, is_change: bool):
    """Показывает клавиатуру выбора класса. is_change=True для смены класса, добавляет кнопку отмены."""
    keyboard = get_class_keyboard_1_9()
    inline_kb = keyboard.inline_keyboard
    if is_change:
        # Добавляем кнопку отмены изменения
        inline_kb.append([types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_class_change")])
        markup = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)
        # Редактируем сообщение при смене класса
        await message.edit_text("Выбери свой класс:", reply_markup=markup)
    else:
        # Начальная регистрация
        await message.answer("Выбери свой класс:", reply_markup=keyboard)
    # Устанавливаем состояние ожидания класса
    await state.set_state(RegisterState.waiting_for_class)

@dp.callback_query(lambda c: c.data == "cancel_class_change")
async def cancel_class_change(callback_query: types.CallbackQuery, state: FSMContext):
    # Отмена смены/регистрации класса
    await callback_query.answer()
    await callback_query.message.edit_text("Изменение класса отменено.")
    await show_main_menu(callback_query.message)
    await state.clear()

@dp.callback_query(lambda c: c.data.startswith("class_"))
async def process_class_selection(callback_query: types.CallbackQuery, state: FSMContext):
    class_name = callback_query.data.replace("class_", "")
    
    # Сохраняем выбранный класс в состояние
    await state.update_data(selected_class=class_name)
    
    keyboard = get_confirm_class_keyboard()
    
    await callback_query.message.edit_text(f"Ты выбрал класс: {class_name}. Всё верно?", reply_markup=keyboard)
    await state.set_state(RegisterState.confirm_class)

@dp.callback_query(lambda c: c.data == "next_classes")
async def show_next_classes(callback_query: types.CallbackQuery, state: FSMContext):
    # Показать клавиатуру 5-9 с кнопкой отмены
    keyboard = get_class_keyboard_5_9()
    # Добавляем кнопку отмены
    inline_kb = keyboard.inline_keyboard
    inline_kb.append([types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_class_change")])
    modified_keyboard = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await callback_query.message.edit_text("Выбери свой класс:", reply_markup=modified_keyboard)

@dp.callback_query(lambda c: c.data == "last_classes")
async def show_last_classes(callback_query: types.CallbackQuery, state: FSMContext):
    # Показать клавиатуру 10-11 с кнопкой отмены
    keyboard = get_class_keyboard_10_11()
    inline_kb = keyboard.inline_keyboard
    inline_kb.append([types.InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_class_change")])
    modified_keyboard = types.InlineKeyboardMarkup(inline_keyboard=inline_kb)
    await callback_query.message.edit_text("Выбери свой класс:", reply_markup=modified_keyboard)

@dp.callback_query(lambda c: c.data == "prev_classes")
async def show_prev_classes(callback_query: types.CallbackQuery, state: FSMContext):
    # Переход с 5-9 обратно на 1-4 (первый экран)
    await register_user(callback_query.message, state, is_change=True)

@dp.callback_query(lambda c: c.data == "middle_classes")
async def show_middle_classes(callback_query: types.CallbackQuery, state: FSMContext):
    # Переход из 10-11 обратно на страницу 5-9
    await show_next_classes(callback_query, state)

@dp.callback_query(lambda c: c.data == "confirm_class")
async def confirm_class(callback_query: types.CallbackQuery, state: FSMContext):
    data = await state.get_data()
    class_name = data.get("selected_class")
    
    session = get_session()
    # Если пользователь уже есть, обновляем класс, иначе создаем нового
    user = session.query(User).filter(User.user_id == callback_query.from_user.id).first()
    if user:
        user.class_name = class_name
    else:
        user = User(
            user_id=callback_query.from_user.id,
            username=callback_query.from_user.username,
            full_name=callback_query.from_user.full_name,
            class_name=class_name
        )
        session.add(user)
    session.commit()
    session.close()
    
    await callback_query.message.edit_text(f"Отлично! Ты зарегистрирован в классе {class_name}.")
    await show_main_menu(callback_query.message)
    await state.clear()

@dp.callback_query(lambda c: c.data == "change_class")
async def change_class(callback_query: types.CallbackQuery, state: FSMContext):
    # Запуск процесса смены класса
    await register_user(callback_query.message, state, is_change=True)

@dp.callback_query(lambda c: c.data == "change_class_registered")
async def change_class_registered(callback_query: types.CallbackQuery, state: FSMContext):
    # Альтернативный вызов смены класса
    await register_user(callback_query.message, state, is_change=True) 