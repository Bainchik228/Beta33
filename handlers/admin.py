import os
import pandas as pd
from datetime import datetime
from aiogram import types
from aiogram.types import InputMediaPhoto, FSInputFile, InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.fsm.context import FSMContext

from bot import dp, bot
from database import User, Review, get_session
from states import AdminAuthState, FilterReviewsState
from keyboards import (
    get_admin_panel_keyboard,
    get_back_to_admin_keyboard,
    get_reviews_navigation_keyboard,
    get_cancel_admin_auth_keyboard,
    get_class_filter_keyboard,
    get_filter_classes_1_4_keyboard,
    get_filter_classes_5_9_keyboard,
    get_filter_classes_10_11_keyboard
)
from handlers.menu import show_main_menu

# Пароль для доступа к админ-панели (в реальном проекте лучше хранить в переменных окружения)
ADMIN_PASSWORD = "admin123"

@dp.callback_query(lambda c: c.data == "admin_panel")
async def start_admin_auth(callback_query: types.CallbackQuery, state: FSMContext):
    """Начинает процесс аутентификации администратора"""
    keyboard = get_cancel_admin_auth_keyboard()
    await callback_query.message.edit_text(
        "👨‍💼 Вход в панель администратора\n\n"
        "Пожалуйста, введите пароль доступа:",
        reply_markup=keyboard
    )
    await state.set_state(AdminAuthState.waiting_for_password)

@dp.message(AdminAuthState.waiting_for_password)
async def check_admin_password(message: types.Message, state: FSMContext):
    """Проверяет пароль администратора"""
    # Удаляем сообщение с паролем, чтобы пароль не отображался в истории чата
    await message.delete()
    
    if message.text == ADMIN_PASSWORD:
        # Пароль верный, показываем админ-панель
        keyboard = get_admin_panel_keyboard()
        await message.answer("✅ Пароль верный! Добро пожаловать в панель администратора", reply_markup=keyboard)
        await state.clear()
    else:
        # Пароль неверный
        keyboard = get_cancel_admin_auth_keyboard()
        await message.answer(
            "❌ Неверный пароль. Пожалуйста, попробуйте еще раз или нажмите отмена:",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "cancel_admin_auth")
async def cancel_admin_auth(callback_query: types.CallbackQuery, state: FSMContext):
    """Отменяет процесс аутентификации"""
    await callback_query.message.edit_text("Вход в админ-панель отменен")
    await show_main_menu(callback_query.message)
    await state.clear()

# Функционал админ-панели, доступный после аутентификации

@dp.callback_query(lambda c: c.data == "admin_home")
async def show_admin_panel(callback_query: types.CallbackQuery):
    """Показывает главное меню админ-панели"""
    keyboard = get_admin_panel_keyboard()
    
    try:
        # Пробуем отредактировать существующее сообщение
        await callback_query.message.edit_text("Панель администратора:", reply_markup=keyboard)
    except Exception as e:
        # Если не получается (например, сообщение с фото), удаляем и отправляем новое
        await callback_query.message.delete()
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="Панель администратора:",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "admin_stats")
async def show_admin_stats(callback_query: types.CallbackQuery):
    session = get_session()
    
    # Общее количество пользователей
    total_users = session.query(User).count()
    
    # Количество по классам
    class_stats = {}
    for user in session.query(User).all():
        if user.class_name in class_stats:
            class_stats[user.class_name] += 1
        else:
            class_stats[user.class_name] = 1
    
    # Формируем сообщение
    stats_text = f"📊 Статистика пользователей:\n\n"
    stats_text += f"Всего пользователей: {total_users}\n\n"
    stats_text += "По классам:\n"
    
    # Сортируем классы для более читаемого вывода
    sorted_classes = sorted(class_stats.keys())
    for class_name in sorted_classes:
        stats_text += f"• {class_name}: {class_stats[class_name]} учеников\n"
    
    session.close()
    
    keyboard = get_back_to_admin_keyboard()
    
    await callback_query.message.edit_text(stats_text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data == "admin_reviews")
async def show_admin_reviews(callback_query: types.CallbackQuery):
    session = get_session()
    
    # Получаем все отзывы с информацией о пользователях, сортируем по дате (новые сверху)
    reviews = session.query(Review, User).join(User).order_by(Review.date.desc()).all()
    
    if not reviews:
        keyboard = get_back_to_admin_keyboard()
        await callback_query.message.edit_text("Отзывов пока нет.", reply_markup=keyboard)
        session.close()
        return
    
    # Отправляем первый отзыв
    await send_review(callback_query.message, reviews, 0)
    session.close()

# Функционал фильтрации отзывов по классам

@dp.callback_query(lambda c: c.data == "admin_filter_reviews")
async def filter_reviews_menu(callback_query: types.CallbackQuery):
    """Показывает меню выбора классов для фильтрации отзывов"""
    keyboard = get_class_filter_keyboard()
    
    try:
        # Пробуем отредактировать существующее сообщение
        await callback_query.message.edit_text(
            "🔍 Фильтрация отзывов по классам\n\n"
            "Выберите группу классов для просмотра отзывов:",
            reply_markup=keyboard
        )
    except Exception as e:
        # Если не получается (например, сообщение с фото), удаляем и отправляем новое
        await callback_query.message.delete()
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="🔍 Фильтрация отзывов по классам\n\n"
                 "Выберите группу классов для просмотра отзывов:",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "filter_1_4")
async def show_filter_1_4(callback_query: types.CallbackQuery):
    """Показывает клавиатуру выбора классов 1-4"""
    keyboard = get_filter_classes_1_4_keyboard()
    
    try:
        await callback_query.message.edit_text(
            "Выберите класс для просмотра отзывов:", 
            reply_markup=keyboard
        )
    except Exception as e:
        await callback_query.message.delete()
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="Выберите класс для просмотра отзывов:",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "filter_5_9")
async def show_filter_5_9(callback_query: types.CallbackQuery):
    """Показывает клавиатуру выбора классов 5-9"""
    keyboard = get_filter_classes_5_9_keyboard()
    
    try:
        await callback_query.message.edit_text(
            "Выберите класс для просмотра отзывов:", 
            reply_markup=keyboard
        )
    except Exception as e:
        await callback_query.message.delete()
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="Выберите класс для просмотра отзывов:",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data == "filter_10_11")
async def show_filter_10_11(callback_query: types.CallbackQuery):
    """Показывает клавиатуру выбора классов 10-11"""
    keyboard = get_filter_classes_10_11_keyboard()
    
    try:
        await callback_query.message.edit_text(
            "Выберите класс для просмотра отзывов:", 
            reply_markup=keyboard
        )
    except Exception as e:
        await callback_query.message.delete()
        await bot.send_message(
            chat_id=callback_query.message.chat.id,
            text="Выберите класс для просмотра отзывов:",
            reply_markup=keyboard
        )

@dp.callback_query(lambda c: c.data.startswith("filter_class_"))
async def show_filtered_reviews(callback_query: types.CallbackQuery):
    """Показывает отзывы от выбранного класса"""
    class_name = callback_query.data.replace("filter_class_", "")
    
    session = get_session()
    
    # Получаем отзывы только от выбранного класса
    reviews = session.query(Review, User).join(User).filter(User.class_name == class_name).order_by(Review.date.desc()).all()
    
    if not reviews:
        await callback_query.message.edit_text(
            f"Отзывов от класса {class_name} пока нет.", 
            reply_markup=get_back_to_admin_keyboard()
        )
        session.close()
        return
    
    # Отправляем первый отзыв с указанием фильтра в заголовке
    review, user = reviews[0]
    
    review_text = f"Отзывы от класса {class_name} (1 из {len(reviews)})\n\n"
    review_text += f"От: {user.full_name}\n"
    review_text += f"Дата: {review.date.strftime('%d.%m.%Y %H:%M')}\n"
    review_text += f"Оценка: {review.rating*'⭐'}\n\n"
    review_text += f"{review.text}"
    
    # Создаем клавиатуру навигации с дополнительной информацией о фильтре
    keyboard = get_filtered_reviews_navigation_keyboard(0, len(reviews), class_name)
    
    # Обрабатываем отправку сообщения с фото или без
    if review.photo_id:
        try:
            # Если текущее сообщение можно отредактировать
            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                media=InputMediaPhoto(
                    media=review.photo_id,
                    caption=review_text
                ),
                reply_markup=keyboard
            )
        except Exception:
            # Если не удалось отредактировать
            await callback_query.message.delete()
            await bot.send_photo(
                chat_id=callback_query.message.chat.id,
                photo=review.photo_id,
                caption=review_text,
                reply_markup=keyboard
            )
    else:
        # Если фото нет, просто отправляем текст
        await callback_query.message.edit_text(review_text, reply_markup=keyboard)
    
    session.close()

def get_filtered_reviews_navigation_keyboard(index, total, class_name):
    """Создает клавиатуру навигации для отфильтрованных отзывов"""
    buttons = []
    
    if index > 0:
        buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"filtered_review_{class_name}_{index-1}"))
    
    # Кнопка возврата теперь отдельно обрабатывается
    buttons.append(InlineKeyboardButton(text="↩️ Назад", callback_data="filtered_back"))
    
    if index < total - 1:
        buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"filtered_review_{class_name}_{index+1}"))
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

@dp.callback_query(lambda c: c.data == "filtered_back")
async def filtered_back_to_filter(callback_query: types.CallbackQuery):
    """Возврат в меню выбора группы классов при фильтрации"""
    # Подтверждаем Callback, удаляем текущее сообщение, если оно есть
    await callback_query.answer()
    try:
        await callback_query.message.delete()
    except Exception:
        pass
    # Отправляем новое меню фильтрации
    keyboard = get_class_filter_keyboard()
    await bot.send_message(
        chat_id=callback_query.message.chat.id,
        text="🔍 Фильтрация отзывов по классам\n\nВыберите группу классов для просмотра отзывов:",
        reply_markup=keyboard
    )

@dp.callback_query(lambda c: c.data.startswith("filtered_review_"))
async def navigate_filtered_reviews(callback_query: types.CallbackQuery):
    """Обрабатывает навигацию по отфильтрованным отзывам"""
    # Парсим данные из callback_data: filtered_review_КЛАСС_ИНДЕКС
    parts = callback_query.data.split('_')
    class_name = parts[2]
    index = int(parts[3])
    
    session = get_session()
    
    # Получаем отзывы для данного класса
    reviews = session.query(Review, User).join(User).filter(User.class_name == class_name).order_by(Review.date.desc()).all()
    
    if not reviews or index >= len(reviews):
        await callback_query.message.edit_text(
            f"Отзывы не найдены или произошла ошибка.", 
            reply_markup=get_back_to_admin_keyboard()
        )
        session.close()
        return
    
    # Показываем отзыв по индексу
    review, user = reviews[index]
    
    review_text = f"Отзывы от класса {class_name} ({index+1} из {len(reviews)})\n\n"
    review_text += f"От: {user.full_name}\n"
    review_text += f"Дата: {review.date.strftime('%d.%m.%Y %H:%M')}\n"
    review_text += f"Оценка: {review.rating*'⭐'}\n\n"
    review_text += f"{review.text}"
    
    keyboard = get_filtered_reviews_navigation_keyboard(index, len(reviews), class_name)
    
    # Обрабатываем отправку сообщения с фото или без
    if review.photo_id:
        try:
            await bot.edit_message_media(
                chat_id=callback_query.message.chat.id,
                message_id=callback_query.message.message_id,
                media=InputMediaPhoto(
                    media=review.photo_id,
                    caption=review_text
                ),
                reply_markup=keyboard
            )
        except Exception:
            await callback_query.message.delete()
            await bot.send_photo(
                chat_id=callback_query.message.chat.id,
                photo=review.photo_id,
                caption=review_text,
                reply_markup=keyboard
            )
    else:
        await callback_query.message.edit_text(review_text, reply_markup=keyboard)
    
    session.close()

# Экспорт данных в Excel

@dp.callback_query(lambda c: c.data == "admin_export_stats")
async def export_stats(callback_query: types.CallbackQuery):
    """Экспортирует статистику пользователей в Excel файл"""
    # Сообщаем пользователю, что файл готовится
    await callback_query.answer("Подготовка файла...")
    
    session = get_session()
    
    # Получаем данные о пользователях
    users = session.query(User).all()
    
    # Создаем DataFrame для статистики пользователей
    user_data = []
    for user in users:
        user_data.append({
            'ID': user.user_id,
            'Имя пользователя': user.username,
            'Полное имя': user.full_name,
            'Класс': user.class_name,
            'Дата регистрации': user.registration_date
        })
    
    users_df = pd.DataFrame(user_data)
    
    # Создаем DataFrame для статистики по классам
    class_stats = {}
    for user in users:
        if user.class_name in class_stats:
            class_stats[user.class_name] += 1
        else:
            class_stats[user.class_name] = 1
    
    class_data = []
    for class_name, count in class_stats.items():
        class_data.append({
            'Класс': class_name,
            'Количество учеников': count
        })
    
    classes_df = pd.DataFrame(class_data)
    classes_df = classes_df.sort_values('Класс')
    
    # Закрываем сессию
    session.close()
    
    # Создаем Excel файл с двумя листами
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = f"stats_{timestamp}.xlsx"
    
    with pd.ExcelWriter(excel_file) as writer:
        users_df.to_excel(writer, sheet_name='Пользователи', index=False)
        classes_df.to_excel(writer, sheet_name='Статистика по классам', index=False)
    
    # Отправляем файл пользователю
    doc = FSInputFile(excel_file)
    await bot.send_document(
        chat_id=callback_query.message.chat.id,
        document=doc,
        caption="📊 Статистика пользователей"
    )
    
    # Возвращаемся в админ-панель
    await show_admin_panel(callback_query)
    
    # Удаляем временный файл
    os.remove(excel_file)

@dp.callback_query(lambda c: c.data == "admin_export_reviews")
async def export_reviews(callback_query: types.CallbackQuery):
    """Экспортирует все отзывы в Excel файл"""
    # Сообщаем пользователю, что файл готовится
    await callback_query.answer("Подготовка файла...")
    
    session = get_session()
    
    # Получаем все отзывы с информацией о пользователях
    reviews = session.query(Review, User).join(User).all()
    
    if not reviews:
        await callback_query.message.edit_text(
            "Отзывов пока нет.", 
            reply_markup=get_back_to_admin_keyboard()
        )
        session.close()
        return
    
    # Создаем DataFrame для отзывов
    review_data = []
    for review, user in reviews:
        review_data.append({
            'ID отзыва': review.id,
            'Пользователь': user.full_name,
            'Класс': user.class_name,
            'Текст отзыва': review.text,
            'Оценка': review.rating,
            'Есть фото': 'Да' if review.photo_id else 'Нет',
            'Дата': review.date
        })
    
    reviews_df = pd.DataFrame(review_data)
    
    # Закрываем сессию
    session.close()
    
    # Создаем Excel файл
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    excel_file = f"reviews_{timestamp}.xlsx"
    
    reviews_df.to_excel(excel_file, index=False)
    
    # Отправляем файл пользователю
    doc = FSInputFile(excel_file)
    await bot.send_document(
        chat_id=callback_query.message.chat.id,
        document=doc,
        caption="📝 Отзывы пользователей"
    )
    
    # Возвращаемся в админ-панель
    await show_admin_panel(callback_query)
    
    # Удаляем временный файл
    os.remove(excel_file)

async def send_review(message: types.Message, reviews, index):
    review, user = reviews[index]
    
    # Формируем сообщение
    review_text = f"Отзыв #{index+1} из {len(reviews)}\n\n"
    review_text += f"От: {user.full_name} ({user.class_name})\n"
    review_text += f"Дата: {review.date.strftime('%d.%m.%Y %H:%M')}\n"
    review_text += f"Оценка: {review.rating*'⭐'}\n\n"
    review_text += f"{review.text}"
    
    keyboard = get_reviews_navigation_keyboard(index, len(reviews))
    
    # Отправляем сообщение
    if review.photo_id:
        # Если есть фото, пробуем отредактировать существующее сообщение
        try:
            await bot.edit_message_media(
                chat_id=message.chat.id,
                message_id=message.message_id,
                media=InputMediaPhoto(
                    media=review.photo_id,
                    caption=review_text
                ),
                reply_markup=keyboard
            )
        except Exception:
            # Если не удалось отредактировать (например, если предыдущее сообщение было без фото)
            await message.delete()
            await bot.send_photo(
                chat_id=message.chat.id,
                photo=review.photo_id,
                caption=review_text,
                reply_markup=keyboard
            )
    else:
        # Если фото нет, просто отправляем текст
        await message.edit_text(review_text, reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("review_"))
async def navigate_reviews(callback_query: types.CallbackQuery):
    index = int(callback_query.data.replace("review_", ""))
    
    session = get_session()
    reviews = session.query(Review, User).join(User).order_by(Review.date.desc()).all()
    
    await send_review(callback_query.message, reviews, index)
    session.close() 