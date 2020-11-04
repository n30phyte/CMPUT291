from state_manager import State
from shared import term
import shared


class EditState(State):
    def enter(self):
        print(term.black_on_darkkhaki(term.center("Edit post")))

    def loop(self):
        print("Title: " + shared.post.title)
        print("Body: " + shared.post.body)
        print(term.move_down())

        print("Edit title/body (leave empty for no change)")
        title = input("New Title: ")
        body = input("New Body: ")
        if title != "":
            shared.post.title = title
        if body != "":
            shared.post.body = body
        shared.db.edit_post(shared.post)
        self.manager.change_state("post")