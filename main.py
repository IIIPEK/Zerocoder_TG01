import asyncio
import os
from random import random

from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery
from dotenv import load_dotenv
from openwether import get_weather, locations
from utils.design import generate_location_keyboard

locations = ['Москва', 'Санкт-Петербург', 'Владивосток', 'Новосибирск', 'Екатеринбург', 'Краснодар', 'Иркутск',
             'Тюмень']

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
async def get_city(message: Message):
    keyboard = generate_location_keyboard(locations)
    await message.answer("Выберите город:", reply_markup=keyboard)
    await message.delete()


@dp.callback_query(lambda c: c.data.startswith("city:"))
async def location_selected(callback: CallbackQuery):
    city = callback.data.split(":", 1)[1]
    weather = await get_weather(city)

    if not weather:
        await callback.message.edit_text(f"Не удалось получить данные о погоде для города {city}")
        return

    await callback.message.edit_text(f"📍 <b>{weather['city']}</b>\n"
                                     f"🌤 {weather['description'].capitalize()}\n"
                                     f"🌡 Температура: {round(weather['temp'])}°C (ощущается как {round(weather['feels_like'])}°C)\n"
                                     f"💧 Влажность: {weather['humidity']}%\n"
                                     f"🔽 Давление: {round(weather['pressure']*0.750062,1)} мм рт. ст.\n"
                                     f"💨 Ветер: {weather['wind']} м/с",
                                     parse_mode="HTML")

    await callback.answer()  # убираем "часики"

@dp.message(F.photo)
async def react_photo(message: Message):
    list = ['Ого, какая фотка!', 'Непонятно, что это такое', 'Не отправляй мне такое больше']
    rand_answ = random.choice(list)
    await message.answer(rand_answ)



async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
