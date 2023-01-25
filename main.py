import telebot
import sqlite3
import os
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler

hostname = '188.190.241.223'
token = os.getenv('TOKEN')
bot = telebot.TeleBot(token)
db = r"/danchenko_svitlo_bot/database/danchenko_svitlo_users.db"
sched = BackgroundScheduler()
url = 'https://kyiv.yasno.com.ua/schedule-turn-off-electricity'
result = [5]


@bot.message_handler(commands=['start'])
def start(message):
	markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
	btn1 = types.KeyboardButton("\U0001F50EЗараз є світло?")
	btn2 = types.KeyboardButton("\U0001F3E0Графік Данченка 28")
	btn3 = types.KeyboardButton("\U0001F4CAГрафік інша адреса")
	markup.add(btn1, btn2, btn3)
	bot.send_message(message.chat.id,
					 text="Вітаю, {0.first_name}!\nТут ти зможеш дізнатися про наявність світла\n"
						  "За орієнтир взято будинок по вул. Данченка 28\n"
						  "Система автоматично за 5 хвилин повідомить про ввімкнення чи вимкнення світла\n"						  
						  "Інформацію від енергетика про планові дії\n"
						  "Та додаткову інформацію по освітленню".format(message.from_user), reply_markup=markup)
	write(message)


@bot.message_handler(content_types=['text'])
def get_usr_text(message):

	if(message.text == "\U0001F50EЗараз є світло?"):
		if result == [0]:
			bot.send_message(message.chat.id, 'Світло є \U0001F7E2')
		elif result == [256]:
			bot.send_message(message.chat.id, 'Світла нема \U0001F534')
		else:
			bot.send_message(message.chat.id, 'Наразі невідомо \U0001F7E0\nЗапитай через 5 хвилин')

	elif (message.text == "\U0001F3E0Графік Данченка 28"):
		bot.send_photo(message.chat.id, open("/danchenko_svitlo_bot/database/graph_28.jpg", 'rb'))

	elif (message.text == "\U0001F4CAГрафік інша адреса"):
		bot.send_message(message.chat.id, f'Перейди по посиланню\n{url}')

	else:
		if message.chat.id == 482085376:
			bot.register_next_step_handler(message, text_from_ivan) # Чекаю новий message і передаю в функцію text_from_ivan
		else:
			bot.send_message(message.chat.id, f'Ця команда недоступна\nПочни роботу з /start')


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

	"""Розпаковка інформації від юзера для подальшого запису в базу.
	   Відокремлення username та user_id"""

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


def switch():

	"""Пінгує другий роутер і при зміні result[0] на result[0,1] відправляє повідомлення всім з db"""
	global result
	response = os.system('ping -c 4 ' + hostname)
	result.append(response)
	if result[0] == 0 and result[1] == 256:
		with sqlite3.connect(db) as conn:
			sql = """SELECT chat_id FROM Users"""
			data = conn.execute(sql)
			for chat_id in data:
				try:
					bot.send_message(chat_id[0], 'Світло вимкнули \U0001F303')
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
					bot.send_message(chat_id[0], 'Світло ввімкнули \U0001F306')
				except telebot.apihelper.ApiTelegramException as error:
					if "Forbidden: bot was blocked by the user" in error.description:
						print(error)
						sql = f"""DELETE FROM Users WHERE chat_id == {chat_id[0]}"""
						conn.execute(sql)
	else:
		pass
	result.pop(0)


sched.add_job(switch, 'interval', minutes=3)

sched.start()
bot.polling(none_stop=True)
