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
        results = shared.db.search_post(keywords.split())
        # todo: display search results
