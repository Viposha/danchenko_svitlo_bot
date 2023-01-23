import telebot
import sqlite3
import os
from telebot import types
import schedule
import time
from apscheduler.schedulers.background import BlockingScheduler

hostname = '188.190.241.223'
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)
db = r"/danchenko_svitlo_bot/database/danchenko_svitlo_users.db"
sched = BlockingScheduler()



@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = types.KeyboardButton("Є інформація від Івана. Він пише:")
	btn2 = types.KeyboardButton("Додаткова інформація")
	markup.add(btn1, btn2)
	bot.send_message(message.chat.id,
					 text="Привіт, {0.first_name}!\nТут ти можеш дізнатися про наявність світла. "
						  "За орієнтир взято будинок по вул.Данченко 28.\n"
						  "Інформацію від енергетика Івана про планові дії\n"
						  "Та додаткову інформацію по освітленню".format(message.from_user), reply_markup=markup)
	write(message)


@bot.message_handler(content_types=['text'])
def get_usr_text(message):
	if (message.text == "Є інформація від Івана. Він пише:"):
		bot.register_next_step_handler(message, text_from_ivan) # Чекаю новий message і передаю в функцію text_from_ivan

	elif (message.text == "Додаткова інформація"):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		btn1 = types.KeyboardButton("Чи є світло зараз?")
		btn2 = types.KeyboardButton("Який графік по Данченко 28?")
		btn3 = types.KeyboardButton("Який графік по іншій адресі?")
		back = types.KeyboardButton("Повернутися назад")
		markup.add(btn1, btn2, btn3, back)
		bot.send_message(message.chat.id, text="Що Вас цікавить?", reply_markup=markup)

	elif (message.text == "Повернутися назад"):
		markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
		button1 = types.KeyboardButton("Є інформація від Івана. Він пише:")
		button2 = types.KeyboardButton("Додаткова інформація")
		markup.add(button1, button2)
		bot.send_message(message.chat.id, text="Ви повернулися в головне меню", reply_markup=markup)
	else:
		bot.send_message(message.chat.id, text="Ця команда недоступна")


def text_from_ivan(message):

	"""Відправляю повідомлення (Що сказав Іван) всім юзерам з бази даних"""

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

	""" Add user which push /start to db"""

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


def test():
	with sqlite3.connect(db) as conn:
		sql = """SELECT chat_id FROM Users"""
		data = conn.execute(sql)
		for chat_id in data:
			try:
				bot.send_message(chat_id[0], 'тестовий текст')
			except telebot.apihelper.ApiTelegramException as error:
				if "Forbidden: bot was blocked by the user" in error.description:
					print(error)
					sql = f"""DELETE FROM Users WHERE chat_id == {chat_id[0]}"""
					conn.execute(sql)


result = [0]
def job():

	"""функція пінгує другий роутер і при зміні result[0] на result[0,1] відправляє повідомлення всім з db"""

	response = os.system('ping -c 4 ' + hostname)
	result.append(response)
	if result[0] == 0 and result[1] == 256:
		with sqlite3.connect(db) as conn:
			sql = """SELECT chat_id FROM Users"""
			data = conn.execute(sql)
			for chat_id in data:
				try:
					bot.send_message(chat_id[0], 'Світло вимкнули')
				except telebot.apihelper.ApiTelegramException as error:
					if "Forbidden: bot was blocked by the user" in error.description:
						print(error)
						sql = f"""DELETE FROM Users WHERE chat_id == {chat_id[0]}"""
						conn.execute(sql)
	elif result[0] == 256 and result[1] == 0:
		with sqlite3.connect(db) as conn:
			sql = """SELECT chat_id FROM Users"""
			data = conn.execute(sql)
			for chat_id in data:
				try:
					bot.send_message(chat_id[0], 'Світло ввімкнули')
				except telebot.apihelper.ApiTelegramException as error:
					if "Forbidden: bot was blocked by the user" in error.description:
						print(error)
						sql = f"""DELETE FROM Users WHERE chat_id == {chat_id[0]}"""
						conn.execute(sql)
	else:
		pass
	result.pop(0)


sched.add_job(job, 'interval', seconds =10)

sched.start()
bot.polling(none_stop=True)

