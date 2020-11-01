from state_manager import State
import shared


class RegisterState(State):
    def enter(self):
        print("** Register **")

    def process(self):
        username = input("Username: ")
        password = input("Password: ")
        name = input("Name: ")
        city = input("City: ")
        result = shared.db.register(username, password, name, city)
        if result[0] == False:
            print(result[1])
            print("\nRegister failed, please try again ...")
            return
        self.manager.change_state("menu")
