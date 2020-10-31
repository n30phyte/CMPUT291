from user import User


class Post:
    post_id = ""
    date = ""
    title = ""
    body = ""
    poster = None

    is_answer = False
    question_id = ""

    def __init__(self, title: str, body: str, poster: User):
        self.title = title
        self.body = body
        self.poster = poster

    def set_post_id(self, post_id: str):
        self.post_id = post_id

    def set_post_date(self, date: str):
        self.date = date

    def set_as_answer(self, question_post: 'Post'):
        self.is_answer = True
        self.question_id = question_post.post_id
