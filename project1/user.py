from datetime import date


class User:
    uid = ""
    name = ""
    password = ""
    city = ""
    create_date = ""
    privileged = False

    def __init__(self, uid: str, name: str, password: str, city: str, create_date: str, priviledged: bool):
        self.uid = uid
        self.name = name
        self.password = password
        self.city = city
        self.create_date = create_date
        self.privileged = priviledged
