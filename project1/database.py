import os
import sqlite3
from datetime import date
from typing import Tuple, List

from post import Post
from user import User


class Database:
    # Avoid injection by doing cursor.execute("(STATEMENT) ?", args)
    # https://stackoverflow.com/questions/13613037/
    connection = None
    first_time = False
    cursor = None
    filename = ""

    # Monotonically increasing counters.
    pid_max = 0
    vno_max = 0

    def __init__(self, db_filename: str = "db/database.db"):
        self.filename = db_filename
        # Check if exists
        if not os.path.exists(self.filename):
            self.first_time = True
        self.setup()

    def setup(self):
        try:
            self.connection = sqlite3.connect(self.filename)
            self.cursor = self.connection.cursor()

            if self.first_time:
                print("First time setup. Creating new file.")
                self.init_sql()
            else:
                # Get max pid and vno
                self.cursor.execute("SELECT MAX(pid) FROM posts;")
                result = self.cursor.fetchone()
                if result[0] is not None:
                    self.pid_max = int(result[0]) + 1

                self.cursor.execute("SELECT MAX(vno) FROM votes;")
                result = self.cursor.fetchone()
                if result[0] is not None:
                    self.vno_max = int(result[0]) + 1

        except sqlite3.Error as e:  # pragma: no cover
            print("Error while connecting to database: %s" % e)

    def init_sql(self):
        with open("db/setup.sql") as command_file:
            setup_queries = command_file.read()
            self.cursor.executescript(setup_queries)

    def login(self, uid: str, password: str) -> Tuple[bool, User]:
        """
        Attempts to log a user in.

        :param uid: User's ID
        :param password: User's password
        :return: A tuple with a boolean and a User object. If login was successful, bool will be true and User will
        exist. Otherwise, result is (false, None).
        """

        self.cursor.execute(
            "SELECT * FROM users WHERE (users.uid LIKE ?) AND (users.pwd = ?);",
            (uid, password),
        )

        result = self.cursor.fetchall()

        if len(result) == 1:
            return True, User(*result[0], privileged=self.get_privileged(uid))
        else:
            return False, "Incorrect Password or user does not exist"

    def register(
            self, uid: str, password: str, name: str = "", city: str = ""
    ) -> Tuple[bool, User]:
        """
        Attempts to register a user. Automatically returns a user as logged in afterwards.

        :param uid: User's ID
        :param password: User's password
        :param name: User's real name (Optional)
        :param city: User's city (Optional)
        :return: A tuple with a boolean and a User object. If register was successful, bool will be true and User will
        exist. Otherwise, result is (false, None).
        """
        if len(uid) > 4 or len(uid) <= 0:
            return False, "Username should be between 0 and 5 characters, exclusive"

        self.cursor.execute("SELECT uid FROM users WHERE users.uid LIKE ?;", (uid,))
        result = self.cursor.fetchall()

        statement = (
            "INSERT INTO users (uid, name, pwd, city, crdate) VALUES(?, ?, ?, ?, ?);"
        )

        if len(result) != 0:
            return False, "Username exists"
        else:
            today = date.today().strftime("%Y-%m-%d")
            self.cursor.execute(statement, (uid, name, password, city, today))

        self.connection.commit()
        return self.login(uid, password)

    def get_privileged(self, uid: str) -> bool:
        self.cursor.execute(
            "SELECT * FROM privileged WHERE privileged.uid = ?;", (uid,)
        )

        result = self.cursor.fetchall()

        if len(result) == 1:
            return True
        else:
            return False

    def new_question(self, title: str, body: str, poster: User) -> Post:
        post = self.new_post(title, body, poster)
        self.cursor.execute("INSERT INTO questions (pid) VALUES (?);", (post.post_id,))
        self.connection.commit()

        return post

    def new_answer(self, title: str, body: str, poster: User, question: Post) -> Post:
        post = self.new_post(title, body, poster)
        post.set_as_answer(question)
        self.cursor.execute(
            "INSERT INTO answers (pid, qid) VALUES (?, ?);",
            (post.post_id, post.question_id),
        )
        self.connection.commit()

        return post

    def new_post(self, title: str, body: str, poster: User) -> Post:
        statement = "INSERT INTO posts (pid, pdate, title, body, poster) VALUES (?, ?, ?, ?, ?);"

        today = date.today().strftime("%Y-%m-%d")
        post = Post(format(self.pid_max, "x"), today, title, body, poster)
        self.pid_max += 1

        self.cursor.execute(
            statement, (post.post_id, today, post.title, post.body, post.poster.uid)
        )

        return post

    def tag_post(self, post: Post, tags: List[str]):
        # Get all existing tags for the post
        self.cursor.execute("SELECT tag FROM tags WHERE pid = ?;", (post.post_id,))

        existing_tags = set()

        # Add them all to the set
        for tag_entries in self.cursor.fetchall():
            existing_tags.add(tag_entries[0].lower())

        # Go through the list and add the tags one by one, keeping casing
        for tag in tags:
            if tag.lower() not in existing_tags:
                self.cursor.execute(
                    "INSERT INTO tags (pid, tag) VALUES (?, ?);", (post.post_id, tag)
                )

        post.tags.extend(tags)

        self.connection.commit()

    def vote_post(self, post: Post, voter: User):
        self.cursor.execute(
            "SELECT uid FROM votes WHERE pid = ? AND uid = ?;",
            (post.post_id, voter.uid),
        )

        result = self.cursor.fetchall()

        if len(result) == 0:
            today = date.today().strftime("%Y-%m-%d")
            statement = "INSERT INTO votes (pid, vno, vdate, uid) VALUES (?, ?, ?, ?);"
            self.cursor.execute(
                statement, (post.post_id, format(self.vno_max, "x"), today, voter.uid)
            )
            self.vno_max += 1
            self.connection.commit()

    def search_post(self, keywords: str) -> List[Post]:
        search_query = "SELECT * FROM posts;"

        results = []
        for keyword in keywords.split():
            self.cursor.execute(search_query)
            test = self.cursor.fetchall()
            results.extend(test)