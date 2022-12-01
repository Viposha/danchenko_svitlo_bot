import telebot

bot = telebot.TeleBot('5924761149:AAErqGWIf0NJ2UboK7OJ4-wXfEwTq-UbAF0')


@bot.message_handler(commands=['start'])
def start(message):
	mess = f'Hello, {message.from_user.first_name}'
	bot.send_message(message.chat.id, mess)


bot.polling(none_stop=True)
