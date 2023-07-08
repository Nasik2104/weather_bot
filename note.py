import requests

# Ваш ключ API від OpenWeatherMap'

# Місце, для якого потрібен прогноз погоди (наприклад, Київ, Україна)
location = 'Пороги'

# Кількість днів для прогнозу
days = 10

# URL запиту до OpenWeatherMap API для прогнозу погоди
url = f'http://api.openweathermap.org/data/2.5/forecast?q={location}&cnt={days}&appid={api_key}'

# Виконання HTTP-запиту і отримання відповіді
response = requests.get(url)
data = response.json()

# Перевірка наявності даних та виведення результатів
if response.status_code == 200:
    # Отримання прогнозу погоди для кожного дня
    forecasts = data['list']
    table_html = "<table>"
    table_html += "<tr><th>Дата/час</th><th>Опис</th><th>Температура (К)</th><th>Вологість (%)</th></tr>"
    # Виведення результатів для кожного дня
    for forecast in forecasts:
        date_time = forecast['dt_txt']
        weather_description = forecast['weather'][0]['description']
        temperature = forecast['main']['temp']
        humidity = forecast['main']['humidity']
        table_html += f"<tr><td>{date_time}</td><td>{weather_description}</td><td>{temperature} К</td><td>{humidity}%</td></tr>"

    table_html += "</table>"

    print(table_html, )

else:
    print('Помилка при отриманні прогнозу погоди')
