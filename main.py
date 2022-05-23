
import telebot


bot = telebot.TeleBot('5307046869:AAFJATWhlKfT9OUYe2hoc-Yt_wuytxAibJo')


@bot.message_handler(commands=['start'])
def start(message):
    #username = message.from_user.username
    bot.send_message(message.chat.id, 'Hello')


bot.polling(none_stop=True)
# if __name__ == "__main__":
#   bot.remove_webhook()
#  bot.set_webhook(url=APP_URL)
# server.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
