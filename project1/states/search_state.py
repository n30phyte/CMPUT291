from state_manager import State
from shared import term
import shared


# print an individual post given the post object, along with its detail and number of answers if it is a question
def print_post(post):
    print("    Body: {}".format(post.body))
    print(
        "    Score: {}; Author: {}; Tags: {}".format(
            post.score, post.poster.name, ", ".join(post.tags)
        )
    )
    if not post.is_answer:
        print("    Answers: {}".format(len(shared.db.get_answers(post))))


# returns the search result in chunks of 5 to present as pages
def get_pages(posts):
    for i in range(0, len(posts), 5):
        yield posts[i : i + 5]


class SearchState(State):
    # initialize search result page to 0 and print header, then prompt for search keyword and obtain search results
    def enter(self):
        self.page = 0
        print(term.black_on_darkkhaki(term.center("Search for a post")))
        keywords = input("Type in keywords to search for: ")
        self.results = list(get_pages(shared.db.search_post(keywords)))

    def loop(self):
        for i in range(len(self.results[self.page])):
            print("{}. Title: {}".format(i + 1, self.results[self.page][i].title))
            print_post(self.results[self.page][i])
        print("6. Show more")
        print("7. Back to menu")
        print("Select a post or action")

        # get user action selection
        with term.cbreak(), term.hidden_cursor():
            action = term.inkey()

        if action < "6":
            # open selected post in post view
            shared.post = self.results[self.page][int(action) - 1]
            self.manager.change_state("post")
            pass
        elif action == "6":
            # show more results
            if len(self.results) - 1 == self.page:
                print("No more results")
            else:
                self.page += 1
        elif action == "7":
            self.manager.change_state("menu")
        else:
            print(action + " is not a valid option, please try again...")
