from state_manager import State
from shared import term
import shared


class QuestionState(State):
    def enter(self):
        print(term.black_on_darkkhaki(term.center("New question")))
        print(term.move_down() + "1. Post a question" + "\n" + "2. Search posts")
        print("Select an action")
        with term.cbreak(), term.hidden_cursor():
            self.action = term.inkey()

    def process(self):
        if self.action == 1:
            self.manager.change_state("question")
        elif self.action == 2:
            self.manager.change_state("search")
