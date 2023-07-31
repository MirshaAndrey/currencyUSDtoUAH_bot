import logging
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from aiogram.utils import executor
import requests

# Замените 'YOUR_TELEGRAM_BOT_TOKEN' на ваш собственный токен
TOKEN = ''

# Включаем логирование, чтобы видеть информацию о взаимодействии с ботом
logging.basicConfig(level=logging.INFO)

# Создаем объекты бота и диспетчера
bot = Bot(token=TOKEN)
dp = Dispatcher(bot)

# URL сервиса курсов валют NBU (Національного банку України)
NBU_API_URL = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange?json"

# Функция для получения курса валюты USD/UAH
def get_usd_to_uah_exchange_rate():
    try:
        response = requests.get(NBU_API_URL, params={"valcode": "USD"})
        if response.status_code == 200:
            data = response.json()
            exchange_rate = data[0]["rate"]
            return exchange_rate
    except Exception as e:
        logging.error(f"Error fetching exchange rate: {e}")
    return None

# Обработчик команды /start
@dp.message_handler(commands=['start'])
async def start_command(message: types.Message):
    await message.reply("Привет! Я бот, который отправляет курс валюты USD/UAH. Введите команду /KURS, чтобы получить текущий курс.")

# Обработчик команды /get_rate
@dp.message_handler(commands=['KURS'])
async def get_rate_command(message: types.Message):
    exchange_rate = get_usd_to_uah_exchange_rate()
    if exchange_rate:
        await message.reply(f"Курс USD/UAH: {exchange_rate:.2f} грн")
    else:
        await message.reply("Не удалось получить курс валюты USD/UAH. Попробуйте позже.")

# Обработчик всех остальных сообщений
@dp.message_handler()
async def echo_message(message: types.Message):
    await message.reply("Я не понимаю вашего запроса. Введите команду /KURS, чтобы получить текущий курс USD/UAH.")

if __name__ == '__main__':
    # Запускаем бота
    executor.start_polling(dp, skip_updates=True)
