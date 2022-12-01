import telebot
import sqlite3
from sqlite3 import Error

with open('tok.txt') as f:
	token = f.readline()

bot = telebot.TeleBot(token)
db = r"danchenko_svitlo_users.db"


@bot.message_handler(commands=['start'])
def start(message):
	mess = f'Hello, {message.from_user.first_name}'
	bot.send_message(message.chat.id, mess)
	write(message)


@bot.message_handler(commands=['ivan'])
def ivan(message):
	mess = 'Вставте повідомлення від Івана'
	bot.send_message(message.chat.id, mess)



def extract(message):
	username = message.from_user.username
	user_id = message.from_user.id
	return [username, user_id]


with sqlite3.connect(db) as conn:
	sql_create_table = """ 
						CREATE TABLE IF NOT EXISTS Users (
						id integer PRIMARY KEY,
						username text NOT NULL,
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
