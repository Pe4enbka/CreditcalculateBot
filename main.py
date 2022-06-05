import os
import logging
import psycopg2
from aiogram.contrib.fsm_storage.memory import MemoryStorage
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from aiogram.dispatcher.filters.state import StatesGroup, State
from aiogram.dispatcher import FSMContext
import markup as nav
from aiogram import Bot, Dispatcher, types, executor
from config import *
from flask import Flask, request

bot = Bot(token=BOT_TOKEN)
server = Flask(__name__)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot, storage=MemoryStorage())
dp.middleware.setup(LoggingMiddleware())

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()

#старт бота
@dp.message_handler(commands=["start"])
async def command_start(message: types.Message):
    await bot.send_message(message.from_user.id, 'Привет {0.username}!'.format(message.from_user), reply_markup=nav.startMenu)


################# главное окно ##################

#регистрация в боте
@dp.callback_query_handler(text='btn_reg')
async def register(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите вашу роль', reply_markup=nav.roleMenu)

#постотреть
@dp.callback_query_handler(text='btn_look')
async def look(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите вашу роль', reply_markup=nav.roleMenu)

####################################################

################# выбор роли ##################

# вернуться назад
@dp.callback_query_handler(text='btn_back')
async def back(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Привет {0.username}!', reply_markup=nav.startMenu)

# физическое лицо
@dp.callback_query_handler(text='btn_individual')
async def individual_role(message: types.Message):
    user_id = message.from_user.id
    db_object.execute(f"SELECT id FROM individual WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute(f"INSERT INTO individual(id) VALUES (%s)", [user_id])
        db_connection.commit()

    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.individualMenu)


########################## имя


@dp.callback_query_handler(text='btn_fullName')
async def full_name(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите данные', reply_markup=nav.fullNameMenu)

    # db_object.execute(f"UPDATE individual SET fullName = {fullName} WHERE id = {user_id}")


# db_connection.commit()


@dp.callback_query_handler(text='btn_name')
async def name(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите имя')
    user_id = message.from_user.id
    user_name = message.from_user.first_name
    db_object.execute(f"SELECT name FROM individual WHERE id = {user_id}")

    result = db_object.fetchone()

    if not result:
        db_object.execute(f"INSERT INTO individual(name) VALUES (%s)", [user_name])
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE individual SET name = (%s)", [user_name])
        db_connection.commit()

    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.fullNameMenu)


@dp.callback_query_handler(text='btn_lastName')
async def register(message: types.Message):
    await bot.send_message(message.from_user.id, 'Введите фамилию')
    user_id = message.from_user.id
    user_name = message.from_user.last_name
    db_object.execute(f"SELECT last_name FROM individual WHERE id = {user_id}")

    result = db_object.fetchone()

    if not result:
        db_object.execute(f"INSERT INTO individual(last_name) VALUES (%s)", [user_name])
        db_connection.commit()
    else:
        db_object.execute(f"UPDATE individual SET last_name = (%s)", [user_name])
        db_connection.commit()

    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите действие', reply_markup=nav.fullNameMenu)


@dp.callback_query_handler(text='btn_patronymic')
async def register(message: types.Message):
    await bot.delete_message(message.from_user.id, message.message.message_id)
    await bot.send_message(message.from_user.id, 'Выберите отчество', reply_markup=nav.fullNameMenu)


# user_id = call.from_user.id
# db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
# result = db_object.fetchone()

# if not result:
#     db_object.execute("INSERT INTO users(id) VALUES (%s)", user_id)
#       db_connection.commit()


if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)
