from state_manager import State
from shared import term
import shared


class AnswerState(State):
    def enter(self):
        print(term.black_on_darkkhaki(term.center("New answer")))

    def loop(self):
        title = input("Title: ")
        body = input("Body: ")
        shared.db.new_answer(title, body, shared.user, shared.post)
        self.manager.change_state("post")
