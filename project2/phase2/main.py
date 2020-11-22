import sys

from database import Database
from prettytable import PrettyTable
from blessed import Terminal

CURRENT_STATE = "LOGIN"

user_id = ""
question_post = {}
answer_post = {}
current_post = {}
db = None
term = Terminal()


# todo: "after each action, the user should be able to return to the main menu for further operations


def clear_term(title: str):
    print(term.home + term.clear + term.move_y(0))
    print(term.black_on_darkkhaki(term.center(title)))


def login():
    clear_term("Login")

    print(term.move_y(int(term.height / 2)))
    uid = input("User ID: ")

    # verify uid is all numeric
    if uid.isdecimal():

        global user_id
        user_id = uid
        user_report()

    elif not uid:
        print("No user ID entered. Proceeding to Main Menu")
    else:
        print("Error: User ID must be numeric. Assuming null")

    global CURRENT_STATE
    CURRENT_STATE = "PROMPT"


def user_report():
    global user_id
    clear_term("User Report for " + user_id)

    result = db.get_report(user_id)

    print(term.ljust("Number of questions owned (avg score): ", 40))
    print(term.ljust("{} ({})".format(result["num_questions"], result["avg_q_votes"])))

    print(term.move_down())

    print(term.ljust("Number of answers owned (avg score): ", 40))
    print(term.ljust("{} ({})".format(result["num_answers"], result["avg_a_votes"])))

    print(term.move_down())
    print(term.ljust("Number of votes by user: ", 40))
    print(term.ljust(result["total_votes"]))

    print(term.move_down(4))
    input("Press any key to go to main menu")

    global CURRENT_STATE
    CURRENT_STATE = "PROMPT"


def prompt_menu():
    clear_term("Main Menu")

    print(term.move_y(int(term.height / 2) - 2))
    print("Select an action:")
    print("1. Post a question")
    print("2. Search for questions")
    print("3. Exit program")

    global CURRENT_STATE
    action = input()

    if action == "1":
        CURRENT_STATE = "POST"
    elif action == "2":
        CURRENT_STATE = "SEARCH"
    elif action == "3":
        CURRENT_STATE = "EXIT"
    else:
        print("error: please choose one of the actions")


def post():
    clear_term("Post a new question")

    print(term.move_y(int(term.height / 2) - 2))

    title = input("Title: ")
    print(term.move_down)
    body = input("body: ")
    print(term.move_down)
    tags = input("tags: ").split()

    # create post and go to post
    global question_post, CURRENT_STATE
    question_post = db.new_question(user_id, title, body, tags)

    CURRENT_STATE = "QUESTION"


def search():
    global CURRENT_STATE, question_post

    clear_term("Search for Question")

    keywords = input("search keywords: ").split()

    results = list(db.search_question(keywords))
    page = 0

    results_table = PrettyTable()
    results_table.field_names = ["Id", "Title", "Creation Date", "Score", "Answers"]

    for post in results:
        results_table.add_row([post["Id"], post["Title"], post["CreationDate"], post["Score"], post["AnswerCount"]])

    if len(results) == 0:
        print("No results found.")
        CURRENT_STATE = "PROMPT"
    else:
        while True:
            print(results_table.get_string(start = page * 5, end = (page + 1) * 5))

            print("6. show more")
            print("Select a post by it's order in the table or enter 0 to return to menu")
            action = input()

            if action == "0":
                CURRENT_STATE = "PROMPT"
                break

            elif int(action) <= min(len(results), 5):

                question_post = results[(int(action) - 1) + (5 * page)]
                db.visit_question(question_post["Id"])

                CURRENT_STATE = "QUESTION"
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
    clear_term("Question")

    question_table = PrettyTable()

    question_table.add_row(["Title", question_post["Title"]])
    question_table.add_row(["Body", question_post["Body"]])
    question_table.add_row(["Tags", question_post["Tags"]])

    question_table.header = False

    print(term.center(str(question_table)))

    print("Select an action:")
    print("1. Answer")
    print("2. List Answers")
    print("3. Vote")
    print("4. Go back to menu")
    action = input()
    if action == "1":
        answer_question()
    elif action == "2":
        list_answers()
    elif action == "3":
        db.vote(question_post["Id"], user_id)
    elif action == "4":
        global CURRENT_STATE
        CURRENT_STATE = "PROMPT"
    else:
        print("error: please choose one of the actions")


def answer_question():
    global answer_post, user_id, CURRENT_STATE

    answer_text = input("answer: ")

    # Change answer_post to current answer
    answer_post = db.answer_question(user_id, question_post["Id"], answer_text)

    CURRENT_STATE = "ANSWER"


def list_answers():
    (accepted_answer, answers) = db.get_answers(question_post["Id"])

    ans_count = 1

    all_answers = []

    global CURRENT_STATE

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

        CURRENT_STATE = "QUESTION"
    else:
        selected = False

        while not selected:
            selection = int(
                input(
                    "\nPlease select an answer to read (or 0 to return to menu): "
                )) - 1

            if selection == 0:
                CURRENT_STATE = "PROMPT"
            elif selection < len(all_answers):
                global answer_post
                answer_post = all_answers[selection]
                selected = True
                CURRENT_STATE = "ANSWER"
            else:
                print("Incorrect number. Please try again.")


def answer():
    global question_post, answer_post, CURRENT_STATE

    clear_term("Answer")

    print("Answer: ")

    answer_table = PrettyTable()
    answer_table.add_row(["Body", answer_post["Body"]])

    print(term.center(str(answer_table)))

    print("Original question:")
    question_table = PrettyTable()

    question_table.add_row(["Title", question_post["Title"]])
    question_table.add_row(["Body", question_post["Body"]])
    question_table.add_row(["Tags", question_post["Tags"]])

    question_table.header = False

    print(term.center(str(question_table)))

    print("Select an action:")
    print("1. Vote")
    print("2. Go back to menu")
    action = input()
    if action == "1":
        db.vote(answer_post["Id"], user_id)
    elif action == "2":
        CURRENT_STATE = "PROMPT"
    else:
        print("error: please choose one of the actions")


def run_state():
    states = {
        "LOGIN": login,  # Login screen
        "POST": post,  # Making a new post
        "SEARCH": search,  # Search for posts
        "QUESTION": question,  # Question view
        "ANSWER": answer,  # Answer view
        "PROMPT": prompt_menu
    }

    if CURRENT_STATE == "EXIT":
        print("Exiting program")
        print(term.clear)
        exit(0)
    else:
        states[CURRENT_STATE]()


if __name__ == "__main__":
    # set up db stuff
    if len(sys.argv) == 1:
        port = 27017
    else:
        port = int(sys.argv[1])
    db = Database(port)
    # Run

    while True:
        run_state()
