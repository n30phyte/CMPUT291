from user import User


class Post:

    def __init__(self, id: str, date: str, title: str, body: str, poster: User):
        self.id = id
        self.date = date
        self.title = title
        self.body = body
        self.poster = poster