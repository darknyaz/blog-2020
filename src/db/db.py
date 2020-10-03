import sqlite3


class DbConnection:
    def __init__(self):
        self.connection = sqlite3.connect('blog-2020.db',
                                          check_same_thread=False)
        self.select_cursor = self.connection.cursor()

    def execute_select_query(self, query):
        return self.select_cursor.execute(query).fetchall()


DB = DbConnection()
