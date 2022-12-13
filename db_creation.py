import sqlite3

db = 'users.db'


def db_create(db):
	with sqlite3.connect(db) as conn:
		sql_create_table = """ 
							CREATE TABLE IF NOT EXISTS Users (
							id integer PRIMARY KEY,
							username text,
							chat_id integer UNIQUE
							); """
		c = conn.cursor()
		c.execute(sql_create_table)

if __name__ == "__main__":
	db_create(db)