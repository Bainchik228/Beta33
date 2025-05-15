from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_class_keyboard_1_9():
    """Клавиатура выбора класса 1-9"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1А", callback_data="class_1А"),
            InlineKeyboardButton(text="1Б", callback_data="class_1Б"),
            InlineKeyboardButton(text="1В", callback_data="class_1В"),
            InlineKeyboardButton(text="1Г", callback_data="class_1Г"),
            InlineKeyboardButton(text="1И", callback_data="class_1И"),
        ],
        [
            InlineKeyboardButton(text="2А", callback_data="class_2А"),
            InlineKeyboardButton(text="2Б", callback_data="class_2Б"),
            InlineKeyboardButton(text="2В", callback_data="class_2В"),
            InlineKeyboardButton(text="2Г", callback_data="class_2Г"),
            InlineKeyboardButton(text="2И", callback_data="class_2И"),
        ],
        [
            InlineKeyboardButton(text="3А", callback_data="class_3А"),
            InlineKeyboardButton(text="3Б", callback_data="class_3Б"),
            InlineKeyboardButton(text="3В", callback_data="class_3В"),
            InlineKeyboardButton(text="3Г", callback_data="class_3Г"),
            InlineKeyboardButton(text="3И", callback_data="class_3И"),
        ],
        [
            InlineKeyboardButton(text="4А", callback_data="class_4А"),
            InlineKeyboardButton(text="4Б", callback_data="class_4Б"),
            InlineKeyboardButton(text="4В", callback_data="class_4В"),
            InlineKeyboardButton(text="4Г", callback_data="class_4Г"),
            InlineKeyboardButton(text="4И", callback_data="class_4И"),
        ],
        [
            InlineKeyboardButton(text="5-9 классы →", callback_data="next_classes"),
        ],
    ])

def get_class_keyboard_5_9():
    """Клавиатура выбора класса 5-9"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="5А", callback_data="class_5А"),
            InlineKeyboardButton(text="5Б", callback_data="class_5Б"),
            InlineKeyboardButton(text="5В", callback_data="class_5В"),
            InlineKeyboardButton(text="5Г", callback_data="class_5Г"),
            InlineKeyboardButton(text="5И", callback_data="class_5И"),
        ],
        [
            InlineKeyboardButton(text="6А", callback_data="class_6А"),
            InlineKeyboardButton(text="6Б", callback_data="class_6Б"),
            InlineKeyboardButton(text="6В", callback_data="class_6В"),
            InlineKeyboardButton(text="6Г", callback_data="class_6Г"),
            InlineKeyboardButton(text="6И", callback_data="class_6И"),
        ],
        [
            InlineKeyboardButton(text="7А", callback_data="class_7А"),
            InlineKeyboardButton(text="7Б", callback_data="class_7Б"),
            InlineKeyboardButton(text="7В", callback_data="class_7В"),
            InlineKeyboardButton(text="7Г", callback_data="class_7Г"),
            InlineKeyboardButton(text="7И", callback_data="class_7И"),
        ],
        [
            InlineKeyboardButton(text="8А", callback_data="class_8А"),
            InlineKeyboardButton(text="8Б", callback_data="class_8Б"),
            InlineKeyboardButton(text="8В", callback_data="class_8В"),
            InlineKeyboardButton(text="8Г", callback_data="class_8Г"),
            InlineKeyboardButton(text="8И", callback_data="class_8И"),
        ],
        [
            InlineKeyboardButton(text="9А", callback_data="class_9А"),
            InlineKeyboardButton(text="9Б", callback_data="class_9Б"),
            InlineKeyboardButton(text="9В", callback_data="class_9В"),
            InlineKeyboardButton(text="9Г", callback_data="class_9Г"),
            InlineKeyboardButton(text="9И", callback_data="class_9И"),
        ],
        [
            InlineKeyboardButton(text="10-11 классы →", callback_data="last_classes"),
            InlineKeyboardButton(text="← Назад", callback_data="prev_classes"),
        ],
    ])

def get_class_keyboard_10_11():
    """Клавиатура выбора класса 10-11"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="10Т", callback_data="class_10Т"),
            InlineKeyboardButton(text="10Г", callback_data="class_10Г"),
        ],
        [
            InlineKeyboardButton(text="11Т", callback_data="class_11Т"),
            InlineKeyboardButton(text="11Г", callback_data="class_11Г"),
        ],
        [
            InlineKeyboardButton(text="← Назад", callback_data="middle_classes"),
        ],
    ])

def get_confirm_class_keyboard():
    """Клавиатура подтверждения выбора класса"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_class"),
            InlineKeyboardButton(text="❌ Изменить", callback_data="change_class"),
        ]
    ])

def get_main_menu_keyboard():
    """Клавиатура главного меню"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📝 Оставить отзыв", callback_data="leave_review"),
        ],
        [
            InlineKeyboardButton(text="🔄 Изменить класс", callback_data="change_class_registered"),
        ],
        [
            InlineKeyboardButton(text="👨‍💼 Панель администратора", callback_data="admin_panel"),
        ],
    ])

def get_photo_choice_keyboard():
    """Клавиатура выбора добавления фото к отзыву"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="Да", callback_data="add_photo"),
            InlineKeyboardButton(text="Нет", callback_data="skip_photo"),
        ]
    ])

def get_rating_keyboard():
    """Клавиатура оценки столовой"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⭐", callback_data="rating_1"),
            InlineKeyboardButton(text="⭐⭐", callback_data="rating_2"),
            InlineKeyboardButton(text="⭐⭐⭐", callback_data="rating_3"),
            InlineKeyboardButton(text="⭐⭐⭐⭐", callback_data="rating_4"),
            InlineKeyboardButton(text="⭐⭐⭐⭐⭐", callback_data="rating_5"),
        ]
    ])

def get_confirm_review_keyboard():
    """Клавиатура подтверждения отзыва"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="✅ Подтвердить", callback_data="confirm_review"),
            InlineKeyboardButton(text="❌ Отменить", callback_data="cancel_review"),
        ]
    ])

def get_admin_panel_keyboard():
    """Клавиатура админ-панели"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="📊 Статистика пользователей", callback_data="admin_stats"),
        ],
        [
            InlineKeyboardButton(text="📝 Все отзывы", callback_data="admin_reviews"),
            InlineKeyboardButton(text="🔍 Отзывы по классам", callback_data="admin_filter_reviews"),
        ],
        [
            InlineKeyboardButton(text="📥 Экспорт статистики", callback_data="admin_export_stats"),
            InlineKeyboardButton(text="📥 Экспорт отзывов", callback_data="admin_export_reviews"),
        ],
        [
            InlineKeyboardButton(text="↩️ Назад", callback_data="back_to_main"),
        ],
    ])

def get_back_to_admin_keyboard():
    """Клавиатура возврата в админ-панель"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="↩️ Назад", callback_data="admin_home"),
        ],
    ])

def get_cancel_admin_auth_keyboard():
    """Клавиатура для отмены ввода пароля администратора"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="❌ Отмена", callback_data="cancel_admin_auth"),
        ],
    ])

def get_reviews_navigation_keyboard(index, total):
    """Клавиатура навигации по отзывам"""
    buttons = []
    
    if index > 0:
        buttons.append(InlineKeyboardButton(text="◀️", callback_data=f"review_{index-1}"))
    
    buttons.append(InlineKeyboardButton(text="↩️ Назад", callback_data="admin_home"))
    
    if index < total - 1:
        buttons.append(InlineKeyboardButton(text="▶️", callback_data=f"review_{index+1}"))
    
    return InlineKeyboardMarkup(inline_keyboard=[buttons])

def get_class_filter_keyboard():
    """Клавиатура выбора класса для фильтрации отзывов"""
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="1А-4И", callback_data="filter_1_4"),
            InlineKeyboardButton(text="5А-9И", callback_data="filter_5_9"),
            InlineKeyboardButton(text="10Т-11Г", callback_data="filter_10_11"),
        ],
        [
            InlineKeyboardButton(text="↩️ Назад", callback_data="admin_home"),
        ],
    ])

def get_filter_classes_1_4_keyboard():
    """Клавиатура выбора 1-4 классов для фильтрации"""
    keyboard = []
    
    # Создаем ряды по 5 кнопок для классов 1-4
    for grade in range(1, 5):
        row = []
        for class_letter in ["А", "Б", "В", "Г", "И"]:
            class_name = f"{grade}{class_letter}"
            row.append(InlineKeyboardButton(text=class_name, callback_data=f"filter_class_{class_name}"))
        keyboard.append(row)
    
    # Добавляем кнопку "Назад"
    keyboard.append([InlineKeyboardButton(text="↩️ Назад", callback_data="admin_filter_reviews")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_filter_classes_5_9_keyboard():
    """Клавиатура выбора 5-9 классов для фильтрации"""
    keyboard = []
    
    # Создаем ряды по 5 кнопок для классов 5-9
    for grade in range(5, 10):
        row = []
        for class_letter in ["А", "Б", "В", "Г", "И"]:
            class_name = f"{grade}{class_letter}"
            row.append(InlineKeyboardButton(text=class_name, callback_data=f"filter_class_{class_name}"))
        keyboard.append(row)
    
    # Добавляем кнопку "Назад"
    keyboard.append([InlineKeyboardButton(text="↩️ Назад", callback_data="admin_filter_reviews")])
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_filter_classes_10_11_keyboard():
    """Клавиатура выбора 10-11 классов для фильтрации"""
    keyboard = [
        [
            InlineKeyboardButton(text="10Т", callback_data="filter_class_10Т"),
            InlineKeyboardButton(text="10Г", callback_data="filter_class_10Г"),
        ],
        [
            InlineKeyboardButton(text="11Т", callback_data="filter_class_11Т"),
            InlineKeyboardButton(text="11Г", callback_data="filter_class_11Г"),
        ],
        [
            InlineKeyboardButton(text="↩️ Назад", callback_data="admin_filter_reviews"),
        ],
    ]
    
    return InlineKeyboardMarkup(inline_keyboard=keyboard) 