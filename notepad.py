import requests
from aiogram import Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
import asyncio
from tabulate import tabulate
import os
import pprint
# Ваш ключ API від OpenWeatherMap

# Місце, для якого потрібен прогноз погоди (наприклад, Київ, Україна)
location = 'Kyiv'

# Кількість днів для прогнозу
days = 10

# URL запиту до OpenWeatherMap API для прогнозу погоди
url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&cnt={days}&appid={api_key}'

# Ініціалізація бота, диспетчера та зберігання
bot_token = "6281790793:AAHRD4P5uPWzXhzNMCwJcvUKFomzRO6tpSQ"
bot = Bot(token=bot_token)
storage = MemoryStorage()
dp = Dispatcher(bot, storage=storage)


@dp.message_handler(commands=['weather'])
async def get_weather(message: types.Message):
    # ... отримання даних погоди ...
    response = requests.get(url)
    data = response.json()
    print(data)
    # Перевірка наявності даних та виведення результатів
    if response.status_code == 200:
        # Отримання прогнозу погоди для кожного дня
        forecasts = data['list']
        code_to_smile = {
        "Clear": "\U00002600",
        "Clouds": "\U00002601",
        "Rain": "\U00002614",
        "Drizzle": "\U00002614",
        "Thunderstorm": "\U000026A1",
        "Snow": "\U0001F328",
        "Mist": "\U0001F32B"
    }
    # Підготовка даних для таблиці
    table_data = []
    headers = ["Дата/час", "Опис", "Температура", "Вологість"]

    for forecast in forecasts:
        date_time = forecast['dt_txt']
        weather_description = forecast['weather'][0]['main']
        temperature = forecast['main']['temp']
        humidity = forecast['main']['humidity']

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = 'що в тебе з погодою'
        # Додавання рядка до даних таблиці
        table_data.append([date_time, wd, temperature, humidity])

    # Форматування повідомлення з використанням Markdown
    message_text = "*Прогноз погоди*\n\n"
    message_text += "| Дата/час | Опис | Температура | Вологість |\n"
   

    for row in table_data:
        message_text += "| {:<20} | {:<4} | {:<14} | {:<15} |\n".format(row[0], row[1], row[2], row[3])

    # Відправлення повідомлення з прогнозом погоди
    await message.answer(message_text, parse_mode='Markdown')

async def main():
    # Запуск бота
    await dp.start_polling()


if __name__ == '__main__':
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main())

