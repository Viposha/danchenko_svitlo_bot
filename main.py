import telebot
import sqlite3
from sqlite3 import Error

with open('tok.txt') as f:
	token = f.readline()

bot = telebot.TeleBot(token)
db = r"danchenko_svitlo_users.db"


@bot.message_handler(commands=['start'])
def start(message):
	mess = f'''Привіт, {message.from_user.first_name}. 
Щоб надати інформацію по освітленню напиши фразу Іван сказав: сюди встав повідомлення від Івана\n
Наприклад:\nІван сказав: Від ранку я на вихідних до понеділка, тому данні по відключенням можуть бути рідше '''
	bot.send_message(message.chat.id, mess)
	write(message)


# @bot.message_handler(commands=['info'])
# def info(message):
# 	mess = 'Напишіть інформацію про освітлення'
# 	bot.send_message(message.chat.id, mess)


@bot.message_handler(content_types=['text'])
def get_user_text(message):
	if 'іван сказав:' in message.text:
		try:
			with sqlite3.connect(db) as conn:
				sql = """SELECT chat_id FROM Users"""
				data = conn.execute(sql)
				for id in data:
					bot.send_message(id[0], message.text)
		except telebot.apihelper.ApiTelegramException as error:
			print(error)


def extract(message):
	username = message.from_user.username
	user_id = message.from_user.id
	return [username, user_id]


with sqlite3.connect(db) as conn:
	sql_create_table = """ 
						CREATE TABLE IF NOT EXISTS Users (
						id integer PRIMARY KEY,
						username text,
						chat_id integer UNIQUE
						); """
	c = conn.cursor()
	c.execute(sql_create_table)


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
