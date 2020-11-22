import sys

from database import Database
from prettytable import PrettyTable
from blessed import Terminal

current_state = "LOGIN"

user_id = ""
question_post = {}
answer_post = {}
current_post = {}
db = None
term = Terminal()

# todo: "after each action, the user should be able to return to the main menu for further operations


def clear_term(state: str):
    print(term.home + term.clear + term.move_y(0))
    print(term.black_on_darkkhaki(term.center(state)))


def login():
    clear_term("login")
    uid = input("user id (press enter to proceed without report): ")
    # verify uid is all numeric
    if uid.isdecimal():
        global user_id
        user_id = uid
        user_report()
    elif not uid:
        print("no user id entered, proceeding to menu...")
    else:
        print("error: uid must be all numeric, proceeding to menu...")
    prompt_menu()


def user_report():
    clear_term("user report")
    global user_id
    result = db.get_report(user_id)
    print("user report for:", user_id)
    print("number of questions owned (avg score): {} ({})".format(
        result["num_questions"], result["avg_q_votes"]))
    print("number of answers   owned (avg score): {} ({})".format(
        result["num_answers"], result["avg_a_votes"]))
    action = input("press any key to continue...")
    prompt_menu()


def prompt_menu():
    clear_term("menu")
    print("select an action:")
    print("1. post a question")
    print("2. search for questions")
    print("3. exit program")
    action = input()
    if action == "1":
        post_question()
    elif action == "2":
        search_questions()
    elif action == "3":
        print("exiting program... cya!")
        exit(0)
    else:
        print("error: please choose one of the actions")


def post_question():
    clear_term("post a question")
    title = input("title: ")
    body = input("body: ")
    tags = input("tags: ").split()
    # create post and go to post
    global question_post
    question_post = db.new_question(user_id, title, body, tags)
    question()


def get_search_pages(questions):
    for i in range(0, len(questions), 5):
        yield questions[i:i + 5]


def print_search_questions(page, results):
    for i in range(len(results[page])):
        post = results[page][i]
        print("{}. title: {}".format(i + 1, post["Title"]))
        print("    creation date: {}; score: {}; answer count: {}".format(
            post["CreationDate"], post["Score"], post["AnswerCount"]))


def search_questions():
    clear_term("search question")
    keywords = input("search keywords: ").split()
    results = list(get_search_pages(db.search_question(keywords)))
    page = 0
    if len(results) == 0:
        print("No results found.")
        prompt_menu()
    else:
        while True:
            print_search_questions(page, results)

            print("6. show more")
            print("select a post by it's number or enter 0 to return to menu")
            action = input()

            if action == "0":
                prompt_menu()
                break
            elif int(action) <= len(results):
                global question_post
                question_post = results[page][int(action) - 1]
                db.visit_question(question_post["Id"])
                question()
                break
            elif action == "6":
                # show more results
                if len(results) - 1 == page:
                    print("no more results")
                else:
                    page += 1
            else:
                print("error: please choose one of the actions")


def question():
    clear_term("question")
    print("question: ")
    print("title: {}".format(question_post["Title"]))
    print("body: {}".format(question_post["Body"]))
    print("tags: {}".format(question_post["Tags"]))

    print("select an action:")
    print("1. answer")
    print("2. list answers")
    print("3. vote")
    print("4. go back to menu")
    action = input()
    if action == "1":
        answer_question()
    elif action == "2":
        list_answers()
    elif action == "3":
        db.vote(question_post["Id"], user_id)
        question()
    elif action == "4":
        prompt_menu()
    else:
        print("error: please choose one of the actions")


def answer_question():
    answer_text = input("answer: ")
    global answer_post
    global user_id
    # change focus post to answer
    answer_post = db.answer_question(user_id, question_post["Id"], answer_text)
    answer()


def list_answers():
    (accepted_answer, answers) = db.get_answers(question_post["Id"])

    ans_count = 1

    all_answers = []
    if accepted_answer is not None:
        print("\nAccepted Answer:\n")

        print("* {}. {}{}".format(
            ans_count, accepted_answer["Body"][:80],
            "..." if len(accepted_answer["Body"]) > 80 else ""))

        print("Post Date: {}".format(accepted_answer["CreationDate"][:10]))
        print("Score: {}".format(accepted_answer["Score"]))

        ans_count += 1

        all_answers.append(accepted_answer)

    if len(answers) != 0:
        print("\nAnswers:\n")

        for ans in answers:
            print("{}. {}{}".format(ans_count, ans["Body"][:80],
                                    "..." if len(ans["Body"]) > 80 else ""))

            print("Post Date: {}".format(ans["CreationDate"][:10]))
            print("Score: {}".format(ans["Score"]))
            print()
            ans_count += 1

        all_answers.extend(answers)

    if len(all_answers) == 0:
        print("No Answers. Going back to Question view.")
        question()
    else:
        selected = False

        while not selected:
            selection = int(
                input(
                    "\nPlease select an answer to read (or 0 to return to menu): "
                )) - 1

            if selection == 0:
                prompt_menu()
            elif selection < len(all_answers):
                global answer_post
                answer_post = all_answers[selection]
                selected = True
                answer()
            else:
                print("Incorrect number. Please try again.")


def answer():
    clear_term("answer")
    print("answer: ")
    global question_post
    global answer_post
    print("body: {}".format(answer_post["Body"]))

    print("in response to question:")
    print("    title: {}".format(question_post["Title"]))
    print("    body: {}".format(question_post["Body"]))
    print("    tags: {}".format(question_post["Tags"]))

    print("select an action:")
    print("1. vote")
    print("2. go back to menu")
    action = input()
    if action == "1":
        db.vote(answer_post["Id"], user_id)
        answer()
    elif action == "2":
        prompt_menu()
    else:
        print("error: please choose one of the actions")


def run_state():
    states = {
        "LOGIN": login,
        "POST": post,
        "SEARCH": search,
        "QUESTION": question,
    }

    if current_state == "EXIT":
        exit(0)
    else:
        states[current_state]()


if __name__ == "__main__":
    # set up db stuff
    if len(sys.argv) == 1:
        port = 27017
    else:
        port = int(sys.argv[1])
    db = Database(port)
    # start
    login()
