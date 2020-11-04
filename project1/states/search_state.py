from state_manager import State
from shared import term
import shared


def getpage(page, posts):

    return posts[page * 5, page * 5 + 5]


class SearchState(State):
    def enter(self):
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("Search for a post")))
        keywords = input(term.move_down() + "Type in keywords to search for")

    def loop(self):
        results = shared.db.search_post(keywords)
        # todo: display search results: columns of posts table + num votes + num answers if question
        for i in range(5):
            print("{}. {}".format(i + 1, results[i]))
        print("6. Show more")
        print("7. Back to menu")
        print("Select a post or action")

        with term.cbreak(), term.hidden_cursor():
            action = term.inkey()

        if action < "6":
            # go to that post
            self.manager.change_state("post")
            pass
        elif action == "6":
            # show more
            pass
        elif action == "7":
            self.manager.change_state("menu")
        else:
            print(action + " is not a valid option, please try again...")
