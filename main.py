import telebot
import sqlite3
import os
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
from db_client import DBClient
from datetime import date

hostname = os.getenv('HOSTNAME')
#token = os.getenv('TOKEN')
token = '5924761149:AAErqGWIf0NJ2UboK7OJ4-wXfEwTq-UbAF0'
bot = telebot.TeleBot(token)
pathname = r"database/danchenko_svitlo_users.db"
sched = BackgroundScheduler()
url = 'https://kyiv.yasno.com.ua/schedule-turn-off-electricity'
db = DBClient(pathname)
result = [5]

sql_create_table = """ 
						CREATE TABLE IF NOT EXISTS Users 
						(
						id integer PRIMARY KEY,
						username text,
						chat_id integer UNIQUE
						); 
					"""
sql_insert_into_db = """ 
					INSERT INTO Users(username,chat_id)
					VALUES(?,?) 
					"""
sql_select_chat_id = """SELECT chat_id FROM Users"""

db.create_conn()
db.execute_command(sql_create_table)  # Create table to db
db.close_conn()


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = types.KeyboardButton("\U0001F50E Зараз є світло?")
	btn2 = types.KeyboardButton("\U0001F3E0 Графік Данченка 28")
	btn3 = types.KeyboardButton("\U0001F4CA Графік інша адреса")
	markup.add(btn1, btn2, btn3)
	bot.send_message(
					message.chat.id, text="Вітаю, {0.first_name}!\nТут ти зможеш дізнатися про наявність світла\n"
					"За орієнтир взято будинок по вул. Данченка 28\n"
					"Система автоматично за 5 хвилин повідомить про ввімкнення чи вимкнення світла\n"
					"Інформацію від енергетика про планові дії\n"
					"Та додаткову інформацію по освітленню".format(message.from_user), reply_markup=markup)
	try:
		db.create_conn()
		db.execute_command_params(sql_insert_into_db, extract(message))
		db.close_conn()
	except sqlite3.IntegrityError as error:
		print(error)


@bot.message_handler(content_types=['text'])
def get_usr_text(message):

	if message.text == "\U0001F50E Зараз є світло?":
		if result == [0]:
			bot.send_message(message.chat.id, '\U0001F7E2 Світло є')
		elif result == [256]:
			bot.send_message(message.chat.id, '\U0001F534 Світла нема')
		else:
			bot.send_message(message.chat.id, '\U0001F7E0 Наразі невідомо\nЗапитай через 5 хвилин')

	elif message.text == "\U0001F3E0 Графік Данченка 28":
		current_date = date.weekday(date.today())
		bot.send_photo(message.chat.id, open(f"/danchenko_svitlo_bot/database/graph/{current_date}.jpg", 'rb'))

	elif message.text == "\U0001F4CA Графік інша адреса":
		bot.send_message(message.chat.id, f'Перейди по посиланню\n{url}')

	else:
		if message.chat.id == 482085376:
			bot.register_next_step_handler(message, text_from_ivan)  # Чекаю новий message і передаю в функцію text_from_ivan
		else:
			bot.send_message(message.chat.id, f'Ця команда недоступна\nПочни роботу з /start')


def text_from_ivan(message):

	"""Відправляю повідомлення (Що сказав Іван) всім юзерам з бази даних"""

	db.create_conn()
	data = db.execute_select_command(sql_select_chat_id)
	for chat_id in data:
		try:
			bot.send_message(chat_id[0], message.text)
		except telebot.apihelper.ApiTelegramException as error:
			if "Forbidden: bot was blocked by the user" in error.description:
				sql = f"""DELETE FROM Users WHERE chat_id == {chat_id[0]}"""
				db.execute_command(sql)
	db.close_conn()


def extract(message):

	""" Розпаковка інформації від юзера для подальшого запису в базу. Відокремлення username та user_id"""

	username = message.from_user.username
	if username is None:
		username = 'name:{0.first_name}'.format(message.from_user)
	user_id = message.from_user.id
	return username, user_id


def switch():

	"""Пінгує другий роутер і при зміні result[0] на result[0,1] відправляє повідомлення всім з db"""

	global result
	response = os.system('ping -c 4 ' + hostname)
	result.append(response)
	db.create_conn()
	data = db.execute_select_command(sql_select_chat_id)
	for chat_id in data:
		try:
			if result[0] == 0 and result[1] == 256:
				bot.send_message(chat_id[0], '\U0001F303 Світло вимкнули')
			elif result[0] == 256 and result[1] == 0:
				bot.send_message(chat_id[0], '\U0001F306 Світло ввімкнули')
			else:
				pass
		except telebot.apihelper.ApiTelegramException as error:
			if "Forbidden: bot was blocked by the user" in error.description:
				sql = f"""DELETE FROM Users WHERE chat_id == {chat_id[0]}"""
				db.execute_command(sql)
	db.close_conn()
	result.pop(0)



sched.add_job(switch, 'interval', minutes=2)
sched.start()
bot.polling(none_stop=True)

