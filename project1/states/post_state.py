import shared
from state_manager import State
from shared import term
import shared


def print_answers(post):
    answers = shared.db.get_answers(post)
    if len(answers) > 0:
        print("Answers:")
    for answer in answers:
        print(
            shared.term.move_down()
            + "    Title: {}; Body: {}".format(answer.title, answer.body)
        )
        print("    Author: {}; Score: {}".format(answer.poster.name, answer.score))


def print_question(post):
    question = shared.db.get_post(post.question_id)
    print("Question:")
    print("    Title: {}; Body: {}".format(question.title, question.body))
    print("    Author: {}; Score: {}".format(question.poster.name, question.score))


def reprint_post():
    print(term.home + term.clear)
    print(term.black_on_darkkhaki(term.center("Post")) + term.move_down())
    print("Title: {}".format(shared.post.title))
    print("Body: {}".format(shared.post.body))
    print("Score: {}".format(shared.post.score))
    print("Author: {}".format(shared.post.poster.name))
    print("Tags: {}".format(", ".join(shared.post.tags)))

    if shared.post.is_answer:
        print_question(shared.post)
    else:
        print_answers(shared.post)

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
        if action == "1" and not shared.post.is_answer:
            # answer
            self.manager.change_state("answer")
        elif action == "2":
            # vote
            voted = shared.db.vote_post(shared.post, shared.user)
            if voted:
                print("Post has been voted")
                with term.location(y=5, x=0):
                    print("Score: {}".format(shared.post.score) + term.clear_eol)
            else:
                print("You already voted this post")
        elif action == "3" and shared.user.privileged and shared.post.is_answer:
            # mark as accepted
            shared.db.accept_answer(shared.post)
            print("Answer Accepted!")
        elif action == "4" and shared.user.privileged:
            # give a badge
            badge = input("What badge?: ")
            success = shared.db.give_badge(shared.post.poster, badge)
            if success:
                print("Badge given!")
            else:
                print("You already gave that badge today")
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
