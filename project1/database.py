import os
import sqlite3
from datetime import date
from typing import Tuple, List, Set

from post import Post
from user import User


DATE_FORMAT = "%Y-%m-%d"


def deduplicate_tag_list(tags: List[str], existing: Set[str] = None) -> List[str]:
    """
    Ensure a list of tags doesn't have duplicates, and optionally compare to another list, while keeping case
    :param tags: List of strings with the tags to be added
    :param existing: List of existing tags
    :return: List of tags that should get added
    """

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
    """
    For a given post, calculate keyword score

    :param post: The post to rate
    :param keywords: Space-seperated keywords
    """
    search_rank = 0

    for keyword in keywords.split():
        if (
            (keyword.lower() in post.title.lower())
            or (keyword in post.body.lower())
            or (keyword in [tag.lower() for tag in post.tags])
        ):
            search_rank += 1

    post.search_rank = search_rank


class Database:
    """
    Main class for most operations, such as user information gathering and post creation.

    Very little validation is done on this side, and the UI/State Machine should handle that.
    """

    # Avoid injection by doing cursor.execute("(STATEMENT) ?", args)
    # https://stackoverflow.com/questions/13613037/
    connection = None
    first_time = False
    cursor = None
    filename = ""

    # Monotonically increasing counters.
    pid_max = 0
    vno_max = 0

    def __init__(self, db_filename: str):
        """
        Constructor for database mega class
        :param db_filename: Location of db file, may not exist.
        """
        self.filename = db_filename

        # Check if exists
        if not os.path.exists(self.filename):
            self.first_time = True

        self.setup()

    def setup(self):
        """
        More initialization code, along with checking if the setup sql script needs to be run
        """
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
                    self.pid_max = int(result[0][1:]) + 1

                self.cursor.execute("SELECT MAX(vno) FROM votes;")
                result = self.cursor.fetchone()
                if result[0] is not None:
                    self.vno_max = int(result[0]) + 1

        except sqlite3.Error as e:  # pragma: no cover
            print("Error while connecting to database: %s" % e)

    def init_sql(self):
        """
        Run setup sql script provided to define database schema
        """
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
            return False, "Username should be between 1 and 4 characters"

        self.cursor.execute("SELECT uid FROM users WHERE users.uid LIKE ?;", (uid,))
        result = self.cursor.fetchall()

        statement = (
            "INSERT INTO users (uid, name, pwd, city, crdate) VALUES(?, ?, ?, ?, ?);"
        )

        if len(result) != 0:
            return False, "Username exists"
        else:
            today = date.today().strftime(DATE_FORMAT)
            self.cursor.execute(statement, (uid, name, password, city, today))

        self.connection.commit()
        return self.login(uid, password)

    def new_question(self, title: str, body: str, poster: User) -> Post:
        """
        Post a new question as the provided user with the provided title and body

        :param title: Title of the question
        :param body: Body of the question
        :param poster: The user that posted
        :return: The post created
        """

        post = self.new_post(title, body, poster)
        self.cursor.execute(
            "INSERT INTO questions (pid) VALUES (?);", (post.get_post_id(),)
        )
        self.connection.commit()

        return post

    def new_answer(self, title: str, body: str, poster: User, question: Post) -> Post:
        """
        Reply to a question as an answer

        :param title: Title of answer
        :param body: Body of answer
        :param poster: Answering user
        :param question: Question to answer
        :return: The new post made by answering
        """

        post = self.new_post(title, body, poster)
        post.set_as_answer(question)
        self.cursor.execute(
            "INSERT INTO answers (pid, qid) VALUES (?, ?);",
            (post.get_post_id(), post.question_id),
        )
        self.connection.commit()

        return post

    def new_post(self, title: str, body: str, poster: User) -> Post:
        statement = "INSERT INTO posts (pid, pdate, title, body, poster) VALUES (?, ?, ?, ?, ?);"

        today = date.today().strftime()
        post = Post(self.pid_max, today, title, body, poster)
        self.pid_max += 1

        self.cursor.execute(
            statement,
            (post.get_post_id(), today, post.title, post.body, post.poster.uid),
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
                "INSERT INTO tags (pid, tag) VALUES (?, ?);", (post.get_post_id(), tag)
            )
            self.connection.commit()

        post.tags.extend(new_tags)

    def vote_post(self, post: Post, voter: User) -> bool:
        self.cursor.execute(
            "SELECT uid FROM votes WHERE pid = ? AND uid = ?;",
            (post.get_post_id(), voter.uid),
        )

        result = self.cursor.fetchall()

        if len(result) == 0:
            today = date.today().strftime(DATE_FORMAT)
            statement = "INSERT INTO votes (pid, vno, vdate, uid) VALUES (?, ?, ?, ?);"
            self.cursor.execute(
                statement, (post.get_post_id(), self.vno_max, today, voter.uid)
            )
            self.vno_max += 1
            self.connection.commit()
            self.set_score(post)
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
        output_ids = set()

        for result in results:
            if result[0] not in output_ids:
                output_ids.add(result[0])

                current_result = self.get_post(result[0])

                count_keywords(current_result, keywords)

                output.append(current_result)

        output.sort(key=lambda post: post.search_rank, reverse=True)

        return output

    def accept_answer(self, answer_post: Post):
        query = "UPDATE questions SET theaid = ? WHERE pid = ?;"

        self.cursor.execute(query, (answer_post.get_post_id(), answer_post.question_id))
        self.connection.commit()
        answer_post.set_as_accepted()

    def give_badge(self, awardee: User, badge_name: str):
        query = "INSERT INTO ubadges(uid, bdate, bname) VALUES (?, ?, ?);"

        today = date.today().strftime(DATE_FORMAT)

        try:
            self.cursor.execute(query, (awardee.uid, today, badge_name))
            self.connection.commit()
        except sqlite3.IntegrityError as Err:
            return False

        return True

    def edit_post(self, edited_post: Post):
        statement = "UPDATE posts SET title = ?, body = ? WHERE posts.pid = ?;"

        self.cursor.execute(
            statement, (edited_post.title, edited_post.body, edited_post.get_post_id())
        )
        self.connection.commit()

    def get_privileged(self, uid: str) -> bool:
        """
        Check if specific user is privileged

        :param uid: uid of user
        :return: True if privileged, false otherwise
        """

        self.cursor.execute(
            "SELECT * FROM privileged WHERE privileged.uid = ?;", (uid,)
        )

        result = self.cursor.fetchall()

        if len(result) == 1:
            return True
        else:
            return False

    def get_user(self, uid: str) -> User:
        """
        Get a user based on their uid
        :param uid: User's ID
        :return: User object
        """

        self.cursor.execute(
            "SELECT * FROM users WHERE (users.uid LIKE ?);",
            (uid,),
        )
        result = self.cursor.fetchone()
        return User(*result, privileged=self.get_privileged(uid))

    def get_tags(self, post: Post) -> List[str]:
        """
        Get existing tags for a post
        :param post: Target post
        :return: List of tags
        """

        self.cursor.execute(
            "SELECT * FROM tags WHERE tags.pid = ?;", (post.get_post_id(),)
        )
        tags = []

        # Add them all to the list
        for tag_entries in self.cursor.fetchall():
            tags.append(tag_entries[1])

        return tags

    def set_score(self, post: Post):
        """
        Calculates and sets the score for specified post where score is the total votes

        :param post: Post to be scored
        """

        self.cursor.execute(
            "SELECT COUNT(votes.vno) FROM votes WHERE votes.pid = ?;",
            (post.get_post_id(),),
        )

        score = self.cursor.fetchone()

        post.score = score[0]

    def get_answers(self, post: Post) -> List[Post]:
        """
        Gets the answers to specified post, assumed to be question but not checked

        :param post: Post to be queried
        :return: List of posts, first post will be the accepted answer
        """

        all_answers_query = "SELECT answers.pid FROM answers WHERE answers.qid = ?;"
        accepted_answer_query = (
            "SELECT theaid FROM questions WHERE pid = ? AND theaid NOT NULL;"
        )

        output = []
        output_ids = set()

        self.cursor.execute(accepted_answer_query, (post.get_post_id(),))
        accepted_res = self.cursor.fetchall()
        if len(accepted_res) == 1:
            accepted_res = accepted_res[0]
            output_ids.add(accepted_res[0])

            accepted_answer = self.get_post(accepted_res[0])
            accepted_answer.set_as_accepted()
            output.append(accepted_answer)

        self.cursor.execute(all_answers_query, (post.get_post_id(),))
        all_res = self.cursor.fetchall()

        for result in all_res:
            if result[0] not in output_ids:
                output_ids.add(result[0])

                current_result = self.get_post(result[0])
                output.append(current_result)

        return output

    def is_post_answer(self, post_id) -> bool:
        query = "SELECT * FROM answers WHERE answers.pid = ?;"

        self.cursor.execute(query, (post_id,))
        result = self.cursor.fetchall()

        return len(result) > 0

    def get_post(self, post_id: str) -> Post:
        query = "SELECT * FROM posts WHERE posts.pid = ?;"

        self.cursor.execute(query, (post_id,))
        result = self.cursor.fetchone()

        poster = self.get_user(result[4])

        post = Post(result[0], result[1], result[2], result[3], poster)

        self.set_score(post)

        post.tags = self.get_tags(post)
        post.is_answer = self.is_post_answer(post_id)

        if post.is_answer:
            # Get the question it's answering
            query = "SELECT qid FROM answers WHERE answers.pid = ?;"
            self.cursor.execute(query, (post_id,))
            result = self.cursor.fetchone()

            post.question_id = result[0]

        return post
