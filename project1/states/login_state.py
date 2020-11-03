from state_manager import State
from shared import term
import shared
import getpass


def prompt_returning_user():
    uid = input("User ID: ")
    pw = getpass.getpass("Password: ")
    return uid, pw


def prompt_new_user():
    uid = input("User ID: ")
    pw = getpass.getpass("Password: ")
    name = input("Name: ")
    city = input("City: ")
    return uid, pw, name, city


class LoginState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center('Welcome!')))
        print("1. Login")
        print("2. Register")
        print("3. Exit")

    def loop(self):
        with term.cbreak(), term.hidden_cursor():
            action = term.inkey()

        if action == "1":
            print("Login:")
            tries = 0
            while tries < 3:
                uid, pw = prompt_returning_user()
                success, shared.user = shared.db.login(uid, pw)
                if success:
                    break
                else:
                    print(shared.user)
                tries += 1
        elif action == "2":
            print("Create a new account:")
            uid, pw, name, city = prompt_new_user()
            success, user = shared.db.register(uid, pw, name, city)
            while not success:
                print(user)
                uid, pw, name, city = prompt_new_user()
                success, shared.user = shared.db.register(uid, pw, name, city)
        elif action == "3":
            exit(0)
        else:
            self.enter()
            print(action + " is not a valid opion, please try again...")
            return

        # shared.user = user
        self.manager.change_state("menu")
