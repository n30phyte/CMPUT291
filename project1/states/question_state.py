from state_manager import State
from shared import term
import shared


class QuestionState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("New question")))

    def loop(self):
        title = input("Title: ")
        body = input("Body: ")
        shared.post = shared.db.new_question(title, body, shared.user)
        print("testing shared post")
        self.manager.change_state("post")
