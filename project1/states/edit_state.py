from state_manager import State
from shared import term
import shared


class EditState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("Edit post")))

    def loop(self):
        print("Title: " + shared.post.title)
        print("Body: " + shared.post.body)
        print(term.move_down())

        title = input("New Title: ")
        body = input("New Body: ")
        shared.post.title = title
        shared.post.body = body
        shared.db.edit_post(shared.post)
        self.manager.change_state("post")

