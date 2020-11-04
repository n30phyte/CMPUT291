import shared
from state_manager import State
from shared import term
import shared


def reprint_post():
    print(term.black_on_darkkhaki(term.center("Post")) + term.move_down())
    # todo: if question, show all answers below
    # todo: if answer, show question
    print("Title: {}".format(shared.post.title))
    print("Body: {}".format(shared.post.body))
    print("Score: {}".format(shared.post.score))
    print("Author: {}".format(shared.post.poster.name))
    print("Tags: {}".format(", ".join(shared.post.tags)))

    print(term.move_down(2))
    # print actions
    if not shared.post.is_answer:
        print("1. Answer")
    print("2. Vote")
    if shared.user.privileged:
        if shared.post.is_answer:
            print("3. Mark as accepted")
        print("4. Give a badge")
        print("5. Add a tag")
        print("6. Edit")
    print("7. Back to menu")
    print("Select an action: ")


class PostState(State):
    def enter(self):
        reprint_post()

    def loop(self):
        with term.cbreak(), term.hidden_cursor():
            action = term.inkey()
        if action == "1" and !shared.post.is_answer:
            # answer
            self.manager.change_state("answer")
        elif action == "2":
            # vote
            voted = shared.db.vote_post(shared.post, shared.user)
            if voted:
                print("Post has been voted")
                print(term.move_y(term.height // 2 + 5) + "Score: {}".format(shared.post.score))
            else:
                print("You already voted this post")
        elif action == "3" and shared.user.privileged and shared.post.is_answer:
            # mark as accepted
            shared.db.accept_answer(shared.post)
            print("Answer Accepted!")
        elif action == "4" and shared.user.privileged:
            # give a badge
            badge = input("What badge?: ")
            shared.db.give_badge(shared.post.poster, badge)
            print("Badge given!")
        elif action == "5" and shared.user.privileged:
            # add a tag
            tags = input("Tags to add: ").split()
            shared.db.tag_post(shared.post, tags)
            reprint_post()
        elif action == "6" and shared.user.privileged:
            # edit
            self.manager.change_state("edit")
        elif action == "7":
            self.manager.change_state("menu")
        else:
            print(action + " is not a valid option, please try again...")
