import requests
import datetime
from config import API_TOKEN, BASE_URL, TG_BOT_TOKEN
from aiogram import Bot, types 
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

bot = Bot(token=TG_BOT_TOKEN)
dispatcher = Dispatcher(bot)

@dispatcher.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши название города!")

@dispatcher.message_handler()
async def get_weather(message: types.Message):
    
    code_emoji = {
        'Clear': 'Ясно \U00002600',
        'Clouds': 'Облачно \U00002601',
        'Rain': 'Дождь \U00002614',
        'Thunderstorm': 'Гроза \U000026A1',
        'Drizzle': 'Дождь \U00002614',
        'Snow': 'Снег \U0001F328',
        'Mist': 'Туман \U0001F32B',
    }

    try:
        #Город берем из ообщения
        response = requests.get(f'{BASE_URL}?q={message.text}&appid={API_TOKEN}&units=metric')
        data = response.json()
   
        city = data['name']
        temp = data['main']['temp']

        weather_descr = data['weather'][0]['main']
        if weather_descr in code_emoji:
            weather_icon = code_emoji[weather_descr]
        else:
            weather_icon = 'Хрен пойми что твориться...) Выгляни в окно!'

        humidity = data['main']['humidity']
        pressure = data['main']['pressure']
        wind_speed = data['wind']['speed']
        # Преобразуем в читаемы формат
        sunrise = datetime.datetime.fromtimestamp(data['sys']['sunrise'])
        sunset = datetime.datetime.fromtimestamp(data['sys']['sunset'])
        day_duration = sunset - sunrise

        await message.reply(f'***{datetime.datetime.now().strftime("%Y-%m-%d %H:%M")}***\n'
            f'Погода в городе: {city}\nТемпература: {temp}C° {weather_icon}\n'
            f'Влажность: {humidity}%\nДавление: {pressure}мм.рт.ст\nСкорость ветра: {wind_speed}м/с\n'
            f'Восход солнца: {sunrise}\nЗакат: {sunset}\n'
            f'Продолжительность дня: {day_duration}\n'
            f'***Have a nice day!!!***')


    except:
        await message.reply('\U00002620 Проверьте название города! \U00002620')
 

if __name__ == '__main__':
    executor.start_polling(dispatcher)    