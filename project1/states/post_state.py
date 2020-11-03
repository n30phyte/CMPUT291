import shared
from state_manager import State
from shared import *


class PostState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("Post")))

    def loop(self):
        # todo: if question, show all answers below
        # todo: if answer, show question
        print("Title: {}".format(shared.post.title))
        print("Body: {}".format(shared.post.body))

        print(term.move_y(2))
        # print actions
        print("1. Answer")
        print("2. Vote")
        if user.is_privileged():
            print("3. Mark as accepted")
            print("4. Give a badge")
            print("5. Add a tag")
            print("6. Edit")
        print("7. Back to menu")

        action = input("Select an action: ")
        if action == "1":
            # answer
            pass
        elif action == "2":
            # vote
            voted = shared.db.vote_post(shared.post, shared.user)
            if voted:
                print("Post has been voted")
            else:
                print("You already voted this post")
        elif action == "3" and user.is_privileged():
            # mark as accepted
            pass
        elif action == "4" and user.is_privileged():
            # give a badge
            badge = input("What badge?: ")
            # shared.db.give_badge(badge, shared.post)
        elif action == "5" and user.is_privileged():
            # add a tag
            tags = input("Tags to add: ").split()
            shared.db.tag_post(shared.post, tags)
        elif action == "6" and user.is_privileged():
            # edit
            pass
        elif action == "7":
            self.manager.change_state("menu")
        else:
            print(action + " is not a valid option, please try again...")
