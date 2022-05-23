import os
import logging
import psycopg2
from aiogram import Bot, Dispatcher, types, executor
from config import *
from flask import Flask, request

bot = Bot(token=BOT_TOKEN)
server = Flask(__name__)
logging.basicConfig(level=logging.INFO)
dp = Dispatcher(bot)

db_connection = psycopg2.connect(DB_URI, sslmode="require")
db_object = db_connection.cursor()


def update_messages_count(user_id):
    db_object.execute(f"UPDATE users SET messages = messages + 1 WHERE id = {user_id}")
    db_connection.commit()


@dp.message_handler(commands=["start"])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    await bot.send_message(message.from_user.id,'Привет {0.first_name}'.format(message.from_user))

    db_object.execute(f"SELECT id FROM users WHERE id = {user_id}")
    result = db_object.fetchone()

    if not result:
        db_object.execute("INSERT INTO users(id, username, messages) VALUES (%s, %s, %s)", (user_id, username, 0))
        db_connection.commit()

    update_messages_count(user_id)






if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)