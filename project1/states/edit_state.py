from state_manager import State
from shared import term
import shared


class EditState(State):
    def enter(self):
        # print header
        print(term.black_on_darkkhaki(term.center("Edit post")))

    def loop(self):
        # show current title and body of post
        print("Title: " + shared.post.title)
        print("Body: " + shared.post.body)
        print(term.move_down())

        # allow user to enter new title and/or body for post (leaving empty if no change desired) and update the database
        # afterwards, go to post view of the edited post.
        print("Edit title/body (leave empty for no change)")
        title = input("New Title: ")
        body = input("New Body: ")
        if title != "":
            shared.post.title = title
        if body != "":
            shared.post.body = body
        shared.db.edit_post(shared.post)
        self.manager.change_state("post")
