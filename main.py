from aiogram.utils import executor

from aiogram.types import Message, ShippingOption, ShippingQuery, LabeledPrice, PreCheckoutQuery

from key_list import get_user_keys

import datetime


from create_connection import create_connection

import asyncio
import aiogram.utils.markdown as md
from aiogram import Bot, Dispatcher, types
from aiogram.types import ParseMode
from add_keys import add_keys

from logger import logger


# создаем бота и диспетчер
bot = Bot(token='6003949568:AAHwtuGz1Y8N0EAdW-ttNFE6LPQWoP-JYzk')

paytoken = "381764678:TEST:59190"

dp = Dispatcher(bot)


mydb = create_connection()

def generate_key(server_id, message, days):
    username = message.from_user.first_name
    telegram_id = message.from_user.id
    start_date = datetime.datetime.now()
    stop_date = start_date + datetime.timedelta(days=days)
    answer = add_keys(server_id,telegram_id, username, start_date, stop_date)
    return answer


subscription_periods = {
    'Amsterdam 1 месяц - 200 рублей': 31,
    'Amsterdam 2 месяца - 350 рублей': 62,
    "Amsterdam 3 месяца - 500 рублей": 92,
    "Amsterdam 6 месяцев - 900 рублей": 182,
    "Germany 1 месяц - 200 рублей": 31,
    "Germany 2 месяца - 350 рублей": 62,
    "Germany 3 месяца - 500 рублей": 92,
    "Germany 6 месяцев - 900 рублей'": 182
}


# обрабатываем команду /start
@dp.message_handler(commands=['start'])
async def process_start_command(message: types.Message):
    mycursor = mydb.cursor()

    # создаем клавиатуру с четырьмя кнопками
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Получить ключ')
    button2 = types.KeyboardButton('Мои ключи')
    button4 = types.KeyboardButton('Заработать')
    keyboard.add(button1, button2, button4)

    username = message.from_user.first_name
    telegram_id = message.from_user.id

    # chat_id = message.chat.id

    # проверем, есть ли данный юзер в таблице users
    mycursor.execute("SELECT * FROM users WHERE telegram_id = %s", (telegram_id,))
    result = mycursor.fetchone()

    if result is None:
        mycursor.execute(
            "INSERT INTO users (username, telegram_id) VALUES (%s, %s)",
            (username, telegram_id)
        )
        # отправляем приветственное сообщение и клавиатуру пользователю
    await message.reply("Добрый день, уважаемый пользователь!", reply_markup=keyboard)
    logger.debug('Обработка команды /start')


@dp.message_handler(lambda message: message.text == 'Мои ключи')
async def process_get_key_command(message: types.Message):
    # создаем клавиатуру с кнопкой "Назад"
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    telegram_id = message.from_user.id
    answer = get_user_keys(telegram_id)
    await message.reply(answer, reply_markup=keyboard)


# обрабатываем нажатие кнопки "Получить ключ"
@dp.message_handler(lambda message: message.text == 'Получить ключ')
async def process_get_key_command(message: types.Message):
    # создаем клавиатуру с кнопкой "Назад"
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    button_Amsterdam = types.KeyboardButton('Amsterdam')
    button_Germany = types.KeyboardButton('Germany')

    keyboard.add(button_Germany)
    keyboard.add(button_Amsterdam)
    keyboard.add(button)

    answer = "Выберите страну:"

    await message.reply(answer, reply_markup=keyboard)

# обрабатываем нажатие кнопки "Amsterdam"
@dp.message_handler(lambda message: message.text == 'Amsterdam')
async def process_back_command(message: types.Message):
    # создаем клавиатуру с кнопкой "Назад"
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    # создаем клавиатуру для выбора колличества месяцев подписки
    button1 = types.KeyboardButton('Amsterdam 1 месяц - 200 рублей')
    button2 = types.KeyboardButton('Amsterdam 2 месяца - 350 рублей')
    button3 = types.KeyboardButton('Amsterdam 3 месяца - 500 рублей')
    button6 = types.KeyboardButton('Amsterdam 6 месяцев - 900 рублей')

    keyboard.add(button1, button2, button3, button6)

    # отправляем сообщение с текстом "Главное меню" и клавиатурой с четырьмя кнопками
    await message.reply("Выберите, на сколько месяцев оформить подписку", reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Amsterdam 1 месяц - 200 рублей')
async def process_back_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    server_id = 1
    answer = generate_key(server_id, message, 1)
    await message.reply(answer, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Amsterdam 2 месяца - 350 рублей')
async def process_back_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    server_id = 1
    answer = generate_key(server_id, message, 2)
    await message.reply(answer, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Amsterdam 3 месяца - 500 рублей")
async def process_back_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    server_id = 1
    answer = generate_key(server_id, message, 3)
    await message.reply(answer, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Amsterdam 6 месяцев - 900 рублей")
async def process_back_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    server_id = 1
    answer = generate_key(server_id, message, 4)
    await message.reply(answer, reply_markup=keyboard)


# обрабатываем нажатие кнопки "Germany"
@dp.message_handler(lambda message: message.text == 'Germany')
async def process_back_command(message: types.Message):
    # создаем клавиатуру с кнопкой "Назад"
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    # создаем клавиатуру для выбора колличества месяцев подписки
    button1 = types.KeyboardButton('Germany 1 месяц - 200 рублей')
    button2 = types.KeyboardButton('Germany 2 месяца - 350 рублей')
    button3 = types.KeyboardButton('Germany 3 месяца - 500 рублей')
    button6 = types.KeyboardButton('Germany 6 месяцев - 900 рублей')

    keyboard.add(button1, button2, button3, button6)

    # отправляем сообщение с текстом "Главное меню" и клавиатурой с четырьмя кнопками
    await message.reply("Выберите, на сколько месяцев оформить подписку", reply_markup=keyboard)



@dp.message_handler(lambda message: message.text == 'Germany 1 месяц - 200 рублей')
async def process_back_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    server_id = 2
    answer = generate_key(server_id, message, 1)
    await message.reply(answer, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == 'Germany 2 месяца - 350 рублей')
async def process_back_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    server_id = 2
    answer = generate_key(server_id, message, 2)
    await message.reply(answer, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Germany 3 месяца - 500 рублей")
async def process_back_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    server_id = 2
    answer = generate_key(server_id, message, 3)
    await message.reply(answer, reply_markup=keyboard)


@dp.message_handler(lambda message: message.text == "Germany 6 месяцев - 900 рублей")
async def process_back_command(message: types.Message):
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)
    server_id = 2
    answer = generate_key(server_id, message, 0)
    await message.reply(answer, reply_markup=keyboard)

# обрабатываем нажатие кнопки "Заработать"
@dp.message_handler(lambda message: message.text == 'Заработать')
async def process_back_command(message: types.Message):
    # создаем клавиатуру с кнопкой "Назад"
    keyboard = types.ReplyKeyboardMarkup(row_width=1)
    button = types.KeyboardButton('Назад')
    keyboard.add(button)

    answer2 = "Здесь будет введена система промокодов"

    # отправляем сообщение с текстом "Главное меню" и клавиатурой с четырьмя кнопками
    await message.reply(answer2, reply_markup=keyboard)

# обрабатываем нажатие кнопки "Назад"
@dp.message_handler(lambda message: message.text == 'Назад')
async def process_back_command(message: types.Message):
    # создаем клавиатуру с четырьмя кнопками
    keyboard = types.ReplyKeyboardMarkup(row_width=2)
    button1 = types.KeyboardButton('Получить ключ')
    button2 = types.KeyboardButton('Мои ключи')
    button4 = types.KeyboardButton('Заработать')
    keyboard.add(button1, button2, button4)

    # отправляем сообщение с текстом "Главное меню" и клавиатурой с четырьмя кнопками
    await message.reply("Главное меню", reply_markup=keyboard)


if __name__ == '__main__':
    # запускаем бота
    loop = asyncio.get_event_loop()
    executor.start_polling(dp, skip_updates=False)
    logger.info('Бот запущен')
