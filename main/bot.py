import os
import sys

# Добавляем корневую директорию проекта в PYTHONPATH
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

import django

# Настройка Django перед импортом моделей
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'skillsett.settings')
django.setup()

import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
from main.models import TelegramUser
from asgiref.sync import sync_to_async


class RegistrationState(StatesGroup):
    tg_id = State()
    waiting_for_password = State()
    waiting_for_password_confirmation = State()


bot = Bot(token="7785795639:AAEbTYYiOiODoxqHplWDf-jBXnZvC-OWbmk")
dp = Dispatcher()

@dp.message(Command("start"))
async def process_start_command(message: Message, state: FSMContext):
    await state.set_state(RegistrationState.tg_id)
    await state.update_data(tg_id=message.from_user.id)
    await message.reply("Привет! Я бот для регистрации в SkillSett. Пожалуйста, придумайте пароль:")
    await state.set_state(RegistrationState.waiting_for_password)


@dp.message(RegistrationState.waiting_for_password)
async def process_password_sent(message: Message, state: FSMContext):
    await state.update_data(waiting_for_password=message.text)
    await message.reply("Пароль принят! Пожалуйста, подтвердите его:")
    await state.set_state(RegistrationState.waiting_for_password_confirmation)


@dp.message(RegistrationState.waiting_for_password_confirmation)
async def process_password_confirmation(message: Message, state: FSMContext):
    await state.update_data(waiting_for_password_confirmation=message.text)
    data = await state.get_data()

    if message.text != data["waiting_for_password"]:
        await message.reply("Пароли не совпадают! Пожалуйста, попробуйте снова.")
        await state.clear()
        return

    try:
        # Оборачиваем создание пользователя в sync_to_async
        create_user = sync_to_async(TelegramUser.objects.create)
        await create_user(
            telegram_id=data["tg_id"],
            password=data["waiting_for_password"]
        )
        await message.reply("Регистрация завершена! Перейдите на сайт и авторизуйтесь. Ваш ID: " + str(data["tg_id"]))
        await state.clear()
    except Exception as e:
        await message.reply(f"Произошла ошибка при регистрации: {e}")
        await state.clear()


async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
