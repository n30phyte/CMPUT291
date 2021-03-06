from typing import List

from user import User


class Post:
    post_id = ""
    date = ""
    title = ""
    body = ""
    poster = None

    is_answer = False
    question_id = ""
    tags = []

    is_accepted = False

    score = 0

    search_rank = 0

    def __init__(self, post_id: int, date: str, title: str, body: str, poster: User):
        self.post_id = post_id
        self.date = date
        self.title = title
        self.body = body
        self.poster = poster

    def set_as_answer(self, question_post: "Post"):
        self.is_answer = True
        self.question_id = question_post.get_post_id()

    def set_as_accepted(self):
        self.is_accepted = True

    def get_post_id(self):
        return str(self.post_id).zfill(4)
