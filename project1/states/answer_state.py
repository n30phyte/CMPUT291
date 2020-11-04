from state_manager import State
from shared import term
import shared


class AnswerState(State):
    def enter(self):
        # print header
        print(term.black_on_darkkhaki(term.center("New answer")))

    def loop(self):
        # obtain title and body of answer and create new answer post in database, then go to post view of the answer
        title = input("Title: ")
        body = input("Body: ")
        shared.db.new_answer(title, body, shared.user, shared.post)
        self.manager.change_state("post")
