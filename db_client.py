import sqlite3


class DBClient:

	"""Initialisation db with its pathname. If it doesn`t exist - create db """

	def __init__(self, pathname: str):
		self.conn = None
		self.pathname = pathname

	""" Create connection to db"""

	def create_conn(self):
		self.conn = sqlite3.connect(self.pathname, check_same_thread=False)

	""" Close connection to db"""

	def close_conn(self):
		self.conn.close()

	"""Create Table in db with query"""

	def execute_command(self, query: str):
		self.conn.execute(query)
		self.conn.commit()

	"""Execute any query to db"""

	def execute_command_params(self, query: str, params: tuple):
		self.conn.execute(query, params)
		self.conn.commit()

	"""Execute SELECT query and return data"""

	def execute_select_command(self, query: str):
		cur = self.conn.cursor()
		cur.execute(query)
		return cur.fetchall()