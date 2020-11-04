from state_manager import State
from shared import term
import shared


def print_post(post):
    print("    Body: {}".format(post.body))
    print("    Score: {}; Author: {}; Tags: {}".format(post.score, post.poster.name, ", ".join(post.tags)))


def get_pages(posts):
    """
    returns pages of posts
    :param posts:
    :return:
    """
    for i in range(0, len(posts), 5):
        yield posts[i:i + 5]


class SearchState(State):
    def enter(self):
        self.page = 0
        print(term.home + term.clear + term.move_y(term.height // 2))
        print(term.black_on_darkkhaki(term.center("Search for a post")))
        keywords = input("Type in keywords to search for: ")
        self.results = list(get_pages(shared.db.search_post(keywords)))

    def loop(self):
        # todo: display search results: columns of posts table + num votes + num answers if question
        for i in range(len(self.results[self.page])):
            print("{}. Title: {}".format(i + 1, self.results[self.page][i].title))
            print_post(self.results[self.page][i])
        print("6. Show more")
        print("7. Back to menu")
        print("Select a post or action")

        with term.cbreak(), term.hidden_cursor():
            action = term.inkey()

        if action < "6":
            # go to that post
            shared.post = self.results[self.page][int(action) - 1]
            self.manager.change_state("post")
            pass
        elif action == "6":
            # show more
            if len(self.results) - 1 == self.page:
                print("No more results")
            else:
                self.page += 1
        elif action == "7":
            self.manager.change_state("menu")
        else:
            print(action + " is not a valid option, please try again...")
