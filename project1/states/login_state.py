from state_manager import State
import shared


class LoginState(State):
    def enter(self):
        print("** LOGIN **")
        yes = ["yes", "y"]
        no = ["no", "n"]
        response = None
        while not (response in yes + no):
            response = input("Do you have an existing account? [yes/no/y/n]: ")
            if response in no:
                self.manager.change_state("register")
        print("\n* PLEASE LOGIN *")

    def process(self):
        username = input("Username: ")
        password = input("Password: ")
        result = shared.db.login(username, password)
        if result[0] == False:
            print(result[1])
            print("\nLogin failed, please try again ...")
            return
        self.manager.change_state("menu")
