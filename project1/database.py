import os
import sqlite3


class Database:
    connection = None
    first_time = False
    cursor = None
    filename = ""

    def __init__(self, db_filename: str = "db/database.db"):
        self.filename = db_filename
        # Check if exists
        if not os.path.exists(self.filename):
            self.first_time = True
        self.setup()

    def setup(self):
        try:
            self.connection = sqlite3.connect(self.filename)

            if self.first_time:
                print("First time setup. Creating new file.")
                self.cursor = self.connection.cursor()
                self.init_sql()

        except sqlite3.Error as e:
            print("Error while connecting to database: %s" % e)

    def init_sql(self):
        with open("db/setup.sql") as command_file:
            setup_queries = command_file.read()
            self.cursor.executescript(setup_queries)
