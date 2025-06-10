import os
import httpx
from dotenv import load_dotenv

load_dotenv()
locations = ['Москва', 'Санкт-Петербург', 'Владивосток', 'Новосибирск', 'Екатеринбург', 'Краснодар', 'Иркутск', 'Тюмень']


async def get_weather(location):
    API_URL = os.getenv('API_URL')
    API_KEY = os.getenv('API_KEY')
    try:
        async with httpx.AsyncClient() as client:
            url=f'{API_URL}?q={location}&lang=ru&units=metric&appid={API_KEY}'
            print(url)
            response = await client.get(url)
        data = response.json()
        result = {
            'city': data['name'],
            'temp': data['main']['temp'],
            'feels_like': data['main']['feels_like'],
            'description': data['weather'][0]['description'],
            'wind': data['wind']['speed'],
            'humidity': data['main']['humidity'],
            'pressure': data['main']['pressure'],
        }
        return result
    except httpx.RequestError as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return None
