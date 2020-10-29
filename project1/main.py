import sqlite3

database = None


def setup():
    try:
        database = sqlite3.connect('./db/database.db')
        print(sqlite3.sqlite_version)

        cursor = database.cursor()
        sql_file = open("./db/setup.sql")

        sql_as_string = sql_file.read()
        cursor.executescript(sql_as_string)

    except sqlite3.Error as e:
        print(e)
    finally:
        if database:
            database.close()


if __name__ == '__main__':
    setup()
    print('Hello World!')
