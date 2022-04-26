import datetime
import requests

from aiogram import Bot, types
from aiogram.dispatcher import Dispatcher
from aiogram.utils import executor

# from config import TOKEN, WEATHER_TOKEN, WEATHER_URL

bot = Bot(token=TOKEN)
dp = Dispatcher(bot)


@dp.message_handler(commands=["start"])
async def start_command(message: types.Message):
    await message.reply("Привет! Напиши название города и я пришлю сводку погоды!")


@dp.message_handler()
async def get_weather(message: types.Message):
    code_to_smile = {
        "Clear": "Ясно",
        "Clouds": "Облачно",
        "Rain": "Дождь",
        "Drizzle": "Дождь",
        "Thunderstorm": "Гроза",
        "Snow": "Снег",
        "Mist": "Туман"
    }

    try:
        r = requests.get(f"{WEATHER_URL}={message.text}&appid={WEATHER_TOKEN}&units=metric")
        data = r.json()

        city = data["name"]
        cur_weather = data["main"]["temp"]
        weather_description = data["weather"][0]["main"]

        if weather_description in code_to_smile:
            wd = code_to_smile[weather_description]
        else:
            wd = "Посмотри в окно, не пойму что там за погода!"

        humidity = data["main"]["humidity"]
        wind = data["wind"]["speed"]

        await message.reply(f"{datetime.datetime.now().strftime('%Y-%m-%d %H:%M')}\n"
                            f"Погода в городе: {city}\nТемпература: {cur_weather}C° {wd}\n"
                            f"Влажность: {humidity}%\nВетер: {wind} м/с\n"
                            )
    except:
        await message.reply("Проверьте название города")


if __name__ == '__main__':
    executor.start_polling(dp)
