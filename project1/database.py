import os
import sqlite3


class Database:
    connection = None
    first_time = False
    cursor = None

    def __init__(self):
        # Check if exists
        if not os.path.exists("db/database.db"):
            self.first_time = True

        self.setup()

    def setup(self):
        try:
            self.connection = sqlite3.connect("db/database.db")
            if self.first_time:
                self.cursor = self.connection.cursor()
                self.init_sql()
        except sqlite3.Error as e:
            print("Error while connecting to database: %s" % e)

    def init_sql(self):
        with open("db/setup.sql") as command_file:
            setup_queries = command_file.read()
            self.cursor.executescript(setup_queries)
