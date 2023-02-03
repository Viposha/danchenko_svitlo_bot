from db_client import DBClient
from tests.conftest import TEST_DB_URL


def test_write_to_db_command(db_connection):
	command = """INSERT INTO Users(id, username, chat_id) VALUES(?, ?, ?);"""
	id = 1
	username = 'User'
	chat_id = 123456
	client = DBClient(TEST_DB_URL)
	client.create_conn()
	client.execute_command_params(command, (id, username, chat_id))
	cursor = db_connection.cursor()
	cursor.execute("""SELECT * FROM Users;""")
	users = cursor.fetchall()
	assert len(users) == 1
	user = users[0]
	assert user[0] == id
	assert user[1] == username
	assert user[2] == chat_id


def test_read_from_db_client(db_connection):
	id = 1
	username = 'User'
	chat_id = 123456
	db_connection.execute("""INSERT INTO Users(id, username,chat_id) VALUES(?, ?, ?);""", (id, username, chat_id))
	db_connection.commit()
	command = """SELECT * FROM Users;"""
	client = DBClient(TEST_DB_URL)
	client.create_conn()
	users = client.execute_select_command(command)
	assert len(users) == 1
	user = users[0]
	assert user[0] == id
	assert user[1] == username
	assert user[2] == chat_id

