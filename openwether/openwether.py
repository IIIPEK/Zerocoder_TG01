import os
import requests
from dotenv import load_dotenv

locations = ['Москва', 'Санкт-Петербург', 'Владивосток', 'Новосибирск', 'Екатеринбург', 'Краснодар', 'Иркутск', 'Тюмень']
API_URL = os.getenv('API_URL')
API_KEY = os.getenv('API_KEY')

def get_weather(location):
    try:
        response = requests.get(f'{API_URL}?q={location}&lang=ru&lang=ru&units=metric&appid=f3086e5e46acaa901b7820c6911993ca')
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
    except requests.exceptions.RequestException as e:
        print(f"Произошла ошибка при выполнении запроса: {e}")
        return None
