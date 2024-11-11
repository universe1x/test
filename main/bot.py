import asyncio
import logging
import secrets
from datetime import timedelta
from django.utils import timezone
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from django.conf import settings
from . import models

# Настройка логирования
logging.basicConfig(level=logging.INFO)

# Инициализация бота
bot = Bot(token="7922423364:AAHSa1aIL9DJgQ5UzgeLfSppV2mt29ub4sE")
dp = Dispatcher()

# Создаем клавиатуру с кнопкой "Запустить"
def get_start_keyboard():
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [InlineKeyboardButton(text="Запустить", callback_data="generate_link")]
        ]
    )
    return keyboard

# Обработчик команды /start
@dp.message(Command("start"))
async def cmd_start(message: types.Message):
    await message.answer(
        "Добро пожаловать! Нажмите кнопку 'Запустить' для генерации ссылки регистрации.",
        reply_markup=get_start_keyboard()
    )

# Обработчик нажатия кнопки
@dp.callback_query(lambda c: c.data == "generate_link")
async def process_generate_link(callback_query: types.CallbackQuery):
    # Генерируем уникальный токен
    token = secrets.token_urlsafe(32)
    
    # Создаем запись в базе данных
    models.TelegramAuthToken.objects.create(
        token=token,
        telegram_id=callback_query.from_user.id,
        expires_at=timezone.now() + timedelta(minutes=30)  # Токен действителен 30 минут
    )
    
    # Формируем ссылку для возврата на сайт
    auth_url = f"{settings.SITE_URL}/telegram-auth/{token}/"
    
    await callback_query.message.answer(
        f"Ваша ссылка для регистрации:\n{auth_url}\n\n"
        "Перейдите по ней для завершения регистрации.\n"
        "Ссылка действительна в течение 30 минут."
    )
    await callback_query.answer()

# Функция запуска бота
async def start_bot():
    try:
        await dp.start_polling(bot)
    finally:
        await bot.session.close()

# Функция для запуска бота в отдельном потоке
def run_bot():
    asyncio.run(start_bot())

if __name__ == '__main__':
    run_bot()
