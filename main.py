import asyncio
import logging

from bot import dp, bot
from database import Base, engine
from handlers import menu, registration, reviews, admin

# Инициализация хендлеров
# Импорты выше уже инициализируют обработчики

# Запуск бота
async def main():
    """Запуск бота"""
    logging.info("Запуск бота")
    # Создаем таблицы в базе данных, если их нет
    Base.metadata.create_all(engine)
    # Запускаем бота
    await dp.start_polling(bot)

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        logging.info("Бот остановлен!") 