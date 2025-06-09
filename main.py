import asyncio
import os

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from openwether import get_weather, locations
from utils.design import generate_location_keyboard

locations = ['Москва', 'Санкт-Петербург', 'Владивосток', 'Новосибирск', 'Екатеринбург', 'Краснодар', 'Иркутск', 'Тюмень']

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()

@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот для обучения Aiogram')

@dp.message(Command('help'))
async def help(message: Message):
    await message.answer('Я могу выполнять следующие команды:\n'
                         '/start - начать диалог\n'
                         '/weather - узнать погоду в указанном городе\n'
                         '/help - вывести справку')

@dp.message(Command('weather'))
async def get_weather(message: Message):
    keyboard = generate_location_keyboard(locations)
    await message.answer("Выберите город:", reply_markup=keyboard)

@dp.callback_query(lambda c: c.data.startswith("city:"))
async def location_selected(callback: CallbackQuery):
    city = callback.data.split(":", 1)[1]
    await callback.message.edit_text(f"Вы выбрали город: {city}")
    await callback.answer()  # убираем "часики"


async def main():
    await dp.start_polling(bot)



if __name__ == '__main__':
    asyncio.run(main())
