import sqlite3
import pytest

TEST_DB_URL = r'V:\python\project\danchenko_svitlo_bot\test_users.db'


@pytest.fixture(scope='session', autouse=True)
def create_tables(db_connection):
	sql_create_table = """ 
							CREATE TABLE IF NOT EXISTS Users 
							(
							id integer PRIMARY KEY,
							username text,
							chat_id integer UNIQUE
							); 
						"""
	sql_drop = """DROP TABLE Users;"""
	db_connection.execute(sql_create_table)
	db_connection.commit()
	yield
	db_connection.execute(sql_drop)
	db_connection.commit()


@pytest.fixture(scope='session')
def db_connection():
	return sqlite3.connect(TEST_DB_URL)


@pytest.fixture(scope='function', autouse=True)
def clean_database(db_connection):
	db_connection.execute("""DELETE FROM Users;""")
	db_connection.commit()


@pytest.fixture(scope='session')
def crete_user_in_database_func(db_connection):
	def create_user(id, username, chat_id):
		db_connection.execute("""INSERT INTO Users(id, username,chat_id) VALUES(?, ?, ?);""", (id, username, chat_id))
		db_connection.commit()
	return create_user


@pytest.fixture(scope='session')
def create_read_users_from_database_function(db_connection):
	def read_user():
		cursor = db_connection.cursor()
		cursor.execute("""SELECT * FROM Users;""")
		return cursor.fetchall()
	return read_user
