from state_manager import State
from shared import *


class PostState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("Post")))

    def loop(self):
        # todo: bold and upsize title?
        # todo: obtain post data somehow
        print("Title: ")
        print("Body: ")

        print(term.move_y(2))
        # print actions
        action_num = 0
        print("{}. Answer".format(action_num))
        action_num += 1
        print("{}. Vote".format(action_num))
        action_num += 1
        if user.is_privileged():
            print("{}. Mark as accepted".format(action_num))
            action_num += 1
            print("{}. Give a badge".format(action_num))
            action_num += 1
            print("{}. Add a tag".format(action_num))
            action_num += 1
            print("{}. Edit".format(action_num))
            action_num += 1
        print("{}. Exit".format(action_num))

        action = input("Select an action")
        if action == 0:
            # answer
            pass
        elif action == 1:
            # vote
            pass
        # todo: which way is best to split into priv and non priv user paths

