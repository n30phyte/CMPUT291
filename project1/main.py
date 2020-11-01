from database import Database
from state_manager import StateManager
from states import LoginState, PostState
from shared import *
from ui import UserInterface
from blessed import Terminal


def prompt_returning_user():
    uid = input("User ID: ")
    pw = input("Password: ")
    return uid, pw


def prompt_new_user():
    uid = input("User ID: ")
    name = input("Name: ")
    city = input("City: ")
    pw = input("Password: ")
    return [uid, name, city, pw]


def login(db, user_type):
    user = None
    if user_type == "r":
        print("Login:")
        tries = 0
        while tries < 3:
            uid, pw = prompt_returning_user()
            success, user = db.login(uid, pw)
            if success:
                break
            else:
                print(user)
            tries += 1
    elif user_type == "n":
        print("Create a new account:")
        uid = input("User ID: ")
        name = input("Name: ")
        city = input("City: ")
        pw = input("Password: ")
        success, user = db.register(uid, pw, name, city)
        while ~success:
            print(user)
            data = prompt_new_user()
            success, user = db.register(data[0], data[1], data[2], data[3])
    return user


if __name__ == "__main__":
    db = Database()

    sm = StateManager()
    sm.addState(LoginState(), "login")
    sm.addState(PostState(), "postEditor")
    
    term = Terminal()
    print(term.home + term.clear + term.move_y(term.height // 2))
    print(term.black_on_darkkhaki(term.center('New or returning user? (n/r)')))

    with term.cbreak(), term.hidden_cursor():
        user_type = term.inkey()

    user = login(db, user_type)
