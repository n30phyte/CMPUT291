from state_manager import State
from shared import term
import shared


class MenuState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("Login successful!")))
        print(term.move_down() + "1. Post a question" + "\n" + "2. Search posts")
        print("Select an action")

    def loop(self):
        with term.cbreak(), term.hidden_cursor():
            action = term.inkey()
        if action == "1":
            self.manager.change_state("question")
        elif action == "2":
            self.manager.change_state("search")
        else:
            print(action + " is not a valid option, please try again...")
