from state_manager import State
from shared import term
import shared


class SearchState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("Search for a post")))
        print(term.move_down() + "Type in keywords to search for")

    def loop(self):
        keywords = input()
        results = shared.db.search_post(keywords)
        # todo: display search results: columns of posts table + num votes + num answers if question
        # for i in range(5):
        #   print("{}. {}".format(i+1, result[i]))
        # print("6. Show more")
        print("Select a post or action")
        action = input()

        if action < "6":
            # go to that post
            pass
        else:
            # show more
            pass
