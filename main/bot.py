import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.fsm.state import State, StatesGroup
from aiogram.types import Message
from aiogram.filters.command import Command
from aiogram.fsm.context import FSMContext
import models


class RegistrationState(StatesGroup):
    tg_id = State()
    waiting_for_password = State()
    waiting_for_password_confirmation = State()


bot = Bot(token="7922423364:AAHSa1aIL9DJgQ5UzgeLfSppV2mt29ub4sE")
dp = Dispatcher(bot)

@dp.message(Command("start"))
async def process_start_command(message: Message, state: FSMContext):
    await RegistrationState.tg_id.set()
    await state.update_data(tg_id=message.from_user.id)
    await message.reply("Привет! Я бот для регистрации в SkillSett. Пожалуйста, придумайте пароль:")
    await RegistrationState.waiting_for_password.set()


@dp.message(RegistrationState.waiting_for_password)
async def process_password_sent(message: Message, state: FSMContext):
    await state.update_data(password=message.text)
    await message.reply("Пароль принят! Пожалуйста, подтвердите его:")
    await RegistrationState.waiting_for_password_confirmation.set()


@dp.message(RegistrationState.waiting_for_password_confirmation)
async def process_password_confirmation(message: Message, state: FSMContext):
    await state.update_data(password_confirmation=message.text)
    data = await state.get_data()

    if message.text != data["password"]:
        await message.reply("Пароли не совпадают! Пожалуйста, попробуйте снова.")
        await state.clear()
    try:
        user = models.TelegramUser.objects.create(
            telegram_id=data["tg_id"],
            password=data["password"]
        )
        await message.reply("Регистрация завершена! Перейдите на сайт и авторизуйтесь.")
        await state.clear()
    except Exception as e:
        await message.reply(f"Произошла ошибка при регистрации: {e}")
        await state.clear()



def main():
    dp.start_polling(bot)

if __name__ == "__main__":
    main()