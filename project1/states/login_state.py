from state_manager import State
from shared import term
import shared


def prompt_returning_user():
    uid = input("User ID: ")
    pw = input("Password: ")
    return uid, pw


def prompt_new_user():
    uid = input("User ID: ")
    pw = input("Password: ")
    name = input("Name: ")
    city = input("City: ")
    return [uid, pw, name, city]


class LoginState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center('New or returning user? (n/r)')))

    def loop(self):
        with term.cbreak(), term.hidden_cursor():
            user_type = term.inkey()

        if user_type == "r":
            print("Login:")
            tries = 0
            while tries < 3:
                uid, pw = prompt_returning_user()
                success, user = shared.db.login(uid, pw)
                if success:
                    break
                else:
                    print(user)
                tries += 1
        elif user_type == "n":
            print("Create a new account:")
            uid = input("User ID: ")
            pw = input("Password: ")
            name = input("Name: ")
            city = input("City: ")
            success, user = shared.db.register(uid, pw, name, city)
            while not success:
                print(user)
                data = prompt_new_user()
                success, user = shared.db.register(data[0], data[1], data[2], data[3])
        else:
            self.enter()
            print(user_type + " is not a valid opion, please try again...")
            return

        self.manager.change_state("menu")
