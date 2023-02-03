import sqlite3
import pytest

TEST_DB_URL = r'V:\python\project\danchenko_svitlo_bot\test_users.db'
SQL_CREATE_TABLE = """ 
						CREATE TABLE IF NOT EXISTS Users 
						(
						id integer PRIMARY KEY,
						username text,
						chat_id integer UNIQUE
						); 
					"""
SQL_DROP_TABLE = """DROP TABLE Users;"""


@pytest.fixture(scope='session', autouse=True)
def create_tables(db_connection):
	db_connection.execute(SQL_CREATE_TABLE)
	db_connection.commit()
	yield
	db_connection.execute(SQL_DROP_TABLE)
	db_connection.commit()


@pytest.fixture(scope='session')
def db_connection():
	return sqlite3.connect(TEST_DB_URL)


@pytest.fixture(scope='function', autouse=True)
def clean_database(db_connection):
	db_connection.execute("""DELETE FROM Users;""")
	db_connection.commit()
