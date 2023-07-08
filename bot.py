import os
import logging
from pprint import pprint

from dotenv import load_dotenv
from aiogram import executor, Bot, Dispatcher, types
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup, ReplyKeyboardMarkup
import requests
from aiogram.dispatcher import FSMContext
import asyncio

logging.basicConfig(level=logging.INFO)
load_dotenv()
bot = Bot(token=os.getenv("TOKEN"))
wea = os.getenv("weather_token")
dp = Dispatcher(bot, storage=MemoryStorage())

ADMINS =[1011382984]
inline_keyboard = types.ReplyKeyboardMarkup(resize_keyboard=True)

async def set_default_commands(dp):
    await bot.set_my_commands(
        [
            types.BotCommand('start', 'Запустити бота'),
            types.BotCommand('author', 'інформація про автора бота'),
        ]
    )

async def on_startup(dp):
    await set_default_commands(dp)

@dp.message_handler(commands='start')
async def cmd_start(message: types.Message):
    await message.reply("Привіт! Вітаю, ви запустили бота, Введіть місто(краще з дотаком своєї країни там Ua, UK, US)")

@dp.message_handler(commands='author')
async def cmd_author(message: types.Message):
    await message.answer("ім'я: Назар\n"
                         "прізвище: Гавриш\n"
                         "хоббі: програмування\n")

yes = types.InlineKeyboardButton(text='так', callback_data='yes')
no = types.InlineKeyboardButton(text='ні', callback_data = 'no')
inline_keyboard.add(yes, no)

chat_id = None

@dp.message_handler()
async def weather_at_the_moment(message: types.Message, state:FSMContext):
    code_to_smile = {
        "Clear": "Ясно \U00002600",
        "Clouds": "Хмарно \U00002601",
        "Rain": "Дощ \U00002614",
        "Drizzle": "Дощ \U00002614",
        "Thunderstorm": "Гроза \U000026A1",
        "Snow": "Сніг \U0001F328",
        "Mist": "Туман \U0001F32B"
    }
    if message.text == 'так':
        await message.answer("Перевірте назву міста")
    else:
        try:
            global city 
            
            city = message.text
            weather = requests.get( 
                f"http://api.openweathermap.org/data/2.5/weather?q={message.text}&appid={wea}&units=metric"
                    )
            data = weather.json()
            

            weather = data["weather"][0]["main"]
            if weather in code_to_smile:
                wd = code_to_smile[weather]
            else:
                wd = 'що в тебе з погодою'

            global temp, chat_id, wind

            humidity = data["main"]["humidity"]
            pressure = data["main"]["pressure"]
            wind = data["wind"]["speed"]
            clouds = data["clouds"]["all"]
            temp = data["main"]["temp"]

            await message.reply(f"<b>Вологість</b> -- {humidity}&#128166\n<b>Тиск</b> --{pressure} мм рт.ст.\n"
                    f"<b>Швидкість вітру</b> -- {wind} м/с\n<b>хмарність</b> -- {clouds}&#x2601\n"
                    f"<b>Температура</b> -- {temp} ℃&#x1F321;\n<b>Погода Загалом</b> -- {wd}", parse_mode='html')
            
            chat_id = message.chat.id
            await bot.send_message(chat_id=message.chat.id, text='Як щодо поради як вдягнутись??', reply_markup=inline_keyboard)
            await state.set_state('temp')
        except:
            await message.reply('перевірте назву міста')

@dp.message_handler(state='temp')
async def temp(message: types.Message, state:FSMContext):
    global temp
    clothing_recomendation ={
        "freeze": "Теплу куртку, штани з начосом, шарф, шапку та рукавички",
        "cold": "Худі та біні шапка",
        "warm": "Сорочка з довгим рукавом",
        "hot": "Шорти та футболка і не забуть про воду;)",
        # Додайте ще якісь температрні позначки, та змініть відповідно до того який одяг ви одягаєте
    }
    if message.text == 'так':
        if float(temp) >= 25:
            await message.answer(f"На вулиці досить спектоно, ось моя порада: {clothing_recomendation['hot']}")
        elif float(temp) >= 15:
            await message.answer(f"На вулиці не дуже тепло але {clothing_recomendation['warm']} буде достатньо")
        elif float(temp) >= 5:
            await message.answer(f"Доволі холодно тому одягнись тепліше: {clothing_recomendation['cold']}")
        else:
            await message.answer(f"На дворі морозно одягни: {clothing_recomendation['freeze']}")
        
        if wind > 15:
            print("Зверни увагу на швидкість вітру: можливо, знадобиться додатково захистити голову та обличчя.")
    
    else:
        await message.answer('сумно:_(')
    
    await bot.send_message(chat_id=message.chat.id, text='Погода на день вперед???', reply_markup=inline_keyboard)
    await state.set_state('forecast')

@dp.message_handler(state='forecast')
async def forecast(message: types.Message, state:FSMContext):
    global city, wea
    days = 8
    if message.text == 'так':
        url = f'http://api.openweathermap.org/data/2.5/forecast?q={city}&cnt=8&appid={wea}&units=metric'

    # Виконання HTTP-запиту і отримання відповіді
        response = requests.get(url)
        data = response.json()
    # Перевірка наявності даних та виведення результатів
        code_to_smile = {
        "Clear": "\U00002600",
        "Clouds": "\U00002601",
        "Rain": "\U00002614",
        "Drizzle": "\U00002614",
        "Thunderstorm": "\U000026A1",
        "Snow": "\U0001F328",
        "Mist": "\U0001F32B"
    }
        if response.status_code == 200:
            forecasts = data['list']
            
            table_data = []
            headers = ["Дата/час", "Опис", "Темп", "Вологість"]
            for forecast in forecasts:
                weather = forecast['weather'][0]["main"]
                if weather in code_to_smile:
                    wd = code_to_smile[weather]
                else:
                    wd = ''
                
                date_time = forecast['dt_txt']
                temperature = float(forecast['main']['temp'])
                humidity = forecast['main']['humidity']
                table_data.append([date_time, wd, round(temperature, 1), humidity])
                
                message_text = "*Прогноз погоди*\n\n"
                message_text += "|Дата/час  \u00A0 \u00A0  |Опис| 🌡  | 💧 |\n"
                for row in table_data:
                    message_text += "| {:<12} | {:<3} | {:<4} | {:<4} |\n".format(row[0][5:16], row[1], row[2], row[3])

   
            await message.answer(message_text, parse_mode='Markdown')
            await message.answer("Дякую за використання боту!")
        else:
        
            await message.answer('Помилка при отриманні прогнозу погоди')
        
        await state.finish()
    else:
        await message.answer("Дякую за використання боту!")
    
        await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, on_startup=on_startup)
    loop = asyncio.get_event_loop()
    