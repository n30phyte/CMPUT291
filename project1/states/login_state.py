from state_manager import State
from shared import term
import shared
import getpass


# prompt login and return inputted uid and password
def prompt_returning_user():
    uid = input("User ID: ")
    pw = getpass.getpass("Password: ")
    return uid, pw


# prompt register info and return the received info
def prompt_new_user():
    uid = input("User ID: ")
    pw = getpass.getpass("Password: ")
    name = input("Name: ")
    city = input("City: ")
    return uid, pw, name, city


class LoginState(State):
    # print header and options
    def enter(self):
        print(term.home + term.clear + term.move_y(0))
        print(term.black_on_darkkhaki(term.center("Welcome!")))
        print("\n1. Login")
        print("2. Register")
        print("3. Exit\n")

    def loop(self):
        # receive user action selection
        with term.cbreak(), term.hidden_cursor():
            action = term.inkey()

        if action == "1":
            # login, allow 3 tries max before returning to login options
            self.enter()
            print("Login:")
            tries = 0
            while tries < 3:
                uid, pw = prompt_returning_user()
                success, shared.user = shared.db.login(uid, pw)
                if success:
                    break
                else:
                    print(shared.user+"\n")
                    tries += 1
            if tries == 3:
                print("Login attempt failed 3 times")
                self.enter()
                return
        elif action == "2":
            # new account registration, allow infinite tries to create unique uid
            print("Create a new account:")
            uid, pw, name, city = prompt_new_user()
            success, shared.user = shared.db.register(uid, pw, name, city)
            while not success:
                print(shared.user)
                uid, pw, name, city = prompt_new_user()
                success, shared.user = shared.db.register(uid, pw, name, city)
        elif action == "3":
            # exit the program
            exit(0)
        else:
            self.enter()
            print(action + " is not a valid opion, please try again...")
            return

        # proceed to menu
        self.manager.change_state("menu")
