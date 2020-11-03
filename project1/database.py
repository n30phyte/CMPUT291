import os
import sqlite3
from datetime import date
from typing import Tuple, List, Set

from post import Post
from user import User


def deduplicate_tag_list(tags: List[str], existing: Set[str] = None) -> List[str]:
    output = []

    if existing is None:
        tag_set = set()
    else:
        tag_set = existing

    # Add them all to the set
    for tag in tags:
        if tag.lower() not in tag_set:
            output.append(tag)
            tag_set.add(tag.lower())

    return output


def count_keywords(post: Post, keywords: str):
    search_rank = 0

    for keyword in keywords.split():
        result = [
            keyword.lower in post.title.lower().split(),  # In title
            keyword in post.body.lower().split(),  # In body
            keyword in [tag.lower() for tag in post.tags],  # In tags
        ]
        search_rank += sum(result)

    post.search_rank = search_rank


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
        existing_tags = set()

        # Add them all to the set
        for tag_entries in self.get_tags(post):
            existing_tags.add(tag_entries.lower())

        new_tags = deduplicate_tag_list(tags, existing_tags)

        # Go through the list and add the tags one by one, keeping casing
        for tag in new_tags:
            self.cursor.execute(
                "INSERT INTO tags (pid, tag) VALUES (?, ?);", (post.post_id, tag)
            )
            self.connection.commit()

        post.tags.extend(new_tags)

    def vote_post(self, post: Post, voter: User) -> bool:
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
            return True

        return False

    def search_post(self, keywords: str) -> List[Post]:
        search_query = (
            "SELECT * FROM posts "
            "LEFT JOIN tags ON posts.pid=tags.pid "
            "WHERE title LIKE :key OR body LIKE :key OR tags.tag LIKE :key "
            "GROUP BY posts.pid;"
        )

        results = []
        for keyword in keywords.split():
            self.cursor.execute(search_query, {"key": "%{}%".format(keyword)})
            search_result = self.cursor.fetchall()
            results.extend(search_result)

        output = []
        output_posts = set()

        for result in results:
            if result[0] not in output_posts:
                poster = self.get_user(result[4])

                current_result = Post(
                    result[0], result[1], result[2], result[3], poster
                )

                self.set_score(current_result)
                current_result.tags = self.get_tags(current_result)

                count_keywords(current_result, keywords)

                output.append(current_result)
                output_posts.add(result[0])

        return output

    def accept_answer(self, answer_post: Post):
        query = "UPDATE questions SET theaid = ? WHERE pid = ?;"

        self.cursor.execute(query, (answer_post.post_id, answer_post.question_id))
        self.connection.commit()
        answer_post.set_as_accepted()

    def give_badge(self, awardee: User, badge_name: str):
        query = "INSERT INTO ubadges(uid, bdate, bname) VALUES (?, ?, ?);"

        today = date.today().strftime("%Y-%m-%d")

        self.cursor.execute(query, (awardee.uid, today, badge_name))
        self.connection.commit()

    def edit_post(self, edited_post: Post):
        statement = "UPDATE posts SET title = ?, body = ? WHERE posts.pid = ?;"

        self.cursor.execute(
            statement, (edited_post.title, edited_post.body, edited_post.post_id)
        )
        self.connection.commit()

    def get_privileged(self, uid: str) -> bool:
        self.cursor.execute(
            "SELECT * FROM privileged WHERE privileged.uid = ?;", (uid,)
        )

        result = self.cursor.fetchall()

        if len(result) == 1:
            return True
        else:
            return False

    def get_user(self, uid: str) -> User:
        self.cursor.execute(
            "SELECT * FROM users WHERE (users.uid LIKE ?);",
            (uid,),
        )
        result = self.cursor.fetchone()
        return User(*result, privileged=self.get_privileged(uid))

    def get_tags(self, post: Post) -> List[str]:
        # Get all existing tags for the post
        self.cursor.execute("SELECT * FROM tags WHERE tags.pid = ?;", (post.post_id,))
        tags = []

        # Add them all to the set
        for tag_entries in self.cursor.fetchall():
            tags.append(tag_entries[1])

        return tags

    def set_score(self, post: Post):
        self.cursor.execute(
            "SELECT COUNT(votes.vno) FROM votes WHERE votes.pid = ?;", (post.post_id,)
        )

        score = self.cursor.fetchone()

        post.score = score
