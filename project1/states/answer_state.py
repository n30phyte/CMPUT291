from state_manager import State
from shared import term
import shared


class AnswerState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("New answer")))

    def loop(self):
        title = input("Title: ")
        body = input("Body: ")
        shared.db.new_answer(title, body, shared.user, shared.post)
