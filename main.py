import asyncio
import os
import random
import tempfile


from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command, CommandStart
from aiogram.types import Message, CallbackQuery, FSInputFile
from dotenv import load_dotenv
from gtts import gTTS
from googletrans import Translator

from openwether import get_weather, locations
from utils.design import generate_location_keyboard

load_dotenv()
TOKEN = os.getenv('TOKEN')

bot = Bot(token=TOKEN)
dp = Dispatcher()


@dp.message(CommandStart())
async def start(message: Message):
    await message.answer('Привет! Я бот для обучения Aiogram')


@dp.message(Command('help'))
async def help_command(message: Message):
    await message.answer('Я могу выполнять следующие команды:\n'
                         '/start - начать диалог\n'
                         '/weather - узнать погоду в указанном городе\n'
                         '/help - вывести справку\n'
                         'Если просто ввести текст, я его переведу на английский')


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
    text = (
        f"📍 <b>{weather['city']}</b>\n"
        f"🌤 {weather['description'].capitalize()}\n"
        f"🌡 Температура: {round(weather['temp'])}°C (ощущается как {round(weather['feels_like'])}°C)\n"
        f"💧 Влажность: {weather['humidity']}%\n"
        f"🔽 Давление: {round(weather['pressure'] * 0.750062, 1)} мм рт. ст.\n"
        f"💨 Ветер: {weather['wind']} м/с"
    )

    tts_text = (
        f"Погода в городе {weather['city']}. "
        f"{weather['description'].capitalize()}. "
        f"Температура {round(weather['temp'])} градусов, ощущается как {round(weather['feels_like'])}. "
        f"Влажность {weather['humidity']} процентов. "
        f"Давление {round(weather['pressure'] * 0.750062)} миллиметров ртутного столба. "
        f"Скорость ветра {weather['wind']} метров в секунду."
    )
    await callback.message.edit_text(text, parse_mode = "HTML")

    tts = gTTS(text=tts_text, lang="ru")
    with tempfile.NamedTemporaryFile(delete=False, suffix=".ogg") as fp:
        voice_path = fp.name
        tts.save(voice_path)

    voice = FSInputFile(voice_path)
    await callback.message.answer_voice(voice)

    await callback.answer()  # убираем "часики"


@dp.message(F.photo)
async def save_photo(message: Message):
    os.makedirs("img", exist_ok=True)  # создаём папку при необходимости
    photo = message.photo[-1]  # берём максимальное качество
    file_path = f"img/{photo.file_id}.jpg"
    file = await bot.get_file(file_id=photo.file_id)
    await bot.download_file(file_path=file.file_path, destination=file_path)
    await message.answer("Фото сохранено ✅")


@dp.message(F.text)
async def translate_text(message: Message):

    async with Translator() as translator:
        result = await translator.translate(message.text, dest='en')
        await message.answer(f"🔤 Перевод:\n{result.text}")


async def main():
    await dp.start_polling(bot)


if __name__ == '__main__':
    asyncio.run(main())
