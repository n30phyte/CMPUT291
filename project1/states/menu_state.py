from state_manager import State
from shared import term
import shared


class MenuState(State):
    # print header and actions
    def enter(self):
        print(term.home + term.clear + term.move_y(0))
        print(term.black_on_darkkhaki(term.center("Menu")))
        print("\n1. Post a question")
        print("2. Search posts")
        print("3. Logout")
        print("\nSelect an action")

    def loop(self):
        # receive user action selection and proceed to corresponding states
        with term.cbreak(), term.hidden_cursor():
            action = term.inkey()
        if action == "1":
            self.manager.change_state("question")
        elif action == "2":
            self.manager.change_state("search")
        elif action == "3":
            self.manager.change_state("login")
        else:
            print(action + " is not a valid option, please try again...")
