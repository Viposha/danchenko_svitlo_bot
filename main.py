import telebot
import sqlite3
from sqlite3 import Error
from db_creation import db_create
import os

token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)
db = "danchenko_svitlo_users.db"


@bot.message_handler(commands=['start'])
def start(message):
	db_create(db)
	mess = f'''Привіт, {message.from_user.first_name}. 
Щоб надати інформацію по освітленню напиши фразу Іван сказав: сюди встав повідомлення від Івана\n
Наприклад:\nІван сказав: перевірка 2 '''
	bot.send_message(message.chat.id, mess)
	write(message)


# @bot.message_handler(commands=['info'])
# def info(message):
# 	mess = 'Напишіть інформацію про освітлення'
# 	bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
	if 'Іван сказав:' in message.text:
		with sqlite3.connect(db) as conn:
			sql = """SELECT chat_id FROM Users"""
			data = conn.execute(sql)
			for chat_id in data:
				try:
					bot.send_message(chat_id[0], message.text)
				except telebot.apihelper.ApiTelegramException as error:
					if "Forbidden: bot was blocked by the user" in error.description:
						print(error)
						sql = f"""DELETE FROM Users WHERE chat_id == {chat_id[0]}"""
						conn.execute(sql)


def extract(message):
	username = message.from_user.username
	user_id = message.from_user.id
	return [username, user_id]


def write(message):
	try:
		with sqlite3.connect(db) as conn:
			data = extract(message)
			base = (data[0], data[1])
			sql = """ 
					INSERT INTO Users(username,chat_id)
					VALUES(?,?) """
			cur = conn.cursor()
			cur.execute(sql, base)
			conn.commit()
			return cur.lastrowid
	except sqlite3.IntegrityError as error:
		print(error)


bot.polling(none_stop=True)

