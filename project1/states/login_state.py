from state_manager import State
from shared import term
import shared

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

class LoginState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center('New or returning user? (n/r)')))

        with term.cbreak(), term.hidden_cursor():
            self.user_type = term.inkey()

    def process(self):
        user = None
        if self.user_type == "r":
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
        elif self.user_type == "n":
            print("Create a new account:")
            uid = input("User ID: ")
            name = input("Name: ")
            city = input("City: ")
            pw = input("Password: ")
            success, user = shared.db.register(uid, pw, name, city)
            while ~success:
                print(user)
                data = prompt_new_user()
                success, user = shared.db.register(data[0], data[1], data[2], data[3])

        self.manager.change_state("menu")
