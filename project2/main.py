import sys

from blessed import Terminal

import prettytable
from prettytable import PrettyTable

from database import Database

CURRENT_STATE = "LOGIN"

user_id = ""
question_post = {}
answer_post = {}
current_post = {}
db = None
term = Terminal()


def clear_term(title: str):
    print(term.home + term.clear + term.move_y(0))
    print(term.black_on_darkkhaki(term.center(title)))


def login():
    clear_term("Login")

    uid = input("User ID: ")

    # verify uid is all numeric
    if uid.isdecimal():
        global user_id
        user_id = uid
        user_report()
    elif not uid:
        print("No user ID entered. Proceeding to Main Menu")
        input("Press enter key to go to main menu")
    else:
        print("Error: User ID must be numeric. Assuming null")
        input("Press enter key to go to main menu")

    global CURRENT_STATE
    CURRENT_STATE = "PROMPT"


def user_report():
    global user_id
    clear_term("User Report for " + user_id)

    result = db.get_report(user_id)

    print(term.ljust("Number of questions owned (avg score): ", 40))
    print(term.ljust("{} ({})".format(result["num_questions"], result["avg_q_votes"])))

    print(term.ljust("Number of answers owned (avg score): ", 40))
    print(term.ljust("{} ({})".format(result["num_answers"], result["avg_a_votes"])))

    print(term.ljust("Number of votes by user: ", 40))
    print(term.ljust(result["total_votes"]))

    print(term.move_down())
    input("Press enter key to go to main menu")

    global CURRENT_STATE
    CURRENT_STATE = "PROMPT"


def prompt_menu():
    clear_term("Main Menu")

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
        input("Press enter key to continue")


def post():
    clear_term("Post a new question")

    title = input("Title: ")
    print(term.move_down)
    body = input("body: ")
    print(term.move_down)
    tags = input("tags: ").lower().split()

    # create post and go to post
    global question_post, CURRENT_STATE
    question_post = db.new_question(user_id, title, body, tags)

    CURRENT_STATE = "QUESTION"


def search():
    global CURRENT_STATE, question_post

    clear_term("Search for Question")

    keywords = input("search keywords: ")

    results = list(db.search_question(keywords))
    page = 0

    results_table = PrettyTable()
    results_table.field_names = [
        "no.",
        "Id",
        "Title",
        "Creation Date",
        "Score",
        "Answers",
    ]
    results_table._max_width = {"Title": 80}
    results_table._max_table_width = term.width
    results_table.hrules = prettytable.ALL

    count = 0
    for post_result in results:
        results_table.add_row(
            [
                (count % 5) + 1,
                post_result["Id"],
                post_result["Title"],
                post_result["CreationDate"],
                post_result["Score"],
                post_result["AnswerCount"],
            ]
        )
        count += 1

    if len(results) == 0:
        print("No results found.")
        input("Press enter key to go to main menu")
        CURRENT_STATE = "PROMPT"
    else:
        while True:
            print(results_table.get_string(start=page * 5, end=(page + 1) * 5))
            print(term.move_down())

            print("6. show more")
            print(
                "Select a post by it's order in the table or enter 0 to return to menu"
            )
            action = input()

            if action == "0":
                CURRENT_STATE = "PROMPT"
                break
            elif action == "":
                pass
            elif int(action) <= min(len(results), 5):
                question_post = results[(int(action) - 1) + (5 * page)]
                db.visit_question(question_post["Id"])
                question_post["ViewCount"] += 1

                CURRENT_STATE = "QUESTION"
                break
            elif action == "6":
                # show more results
                if len(results) - 1 == page:
                    print("no more results")
                    input("Press enter key to continue")
                else:
                    page += 1
            else:
                print("error: please choose one of the actions")
                input("Press enter key to continue")


def question():
    clear_term("Question")

    question_table = PrettyTable()

    for key in question_post:
        question_table.add_row([key, question_post[key]])

    question_table.field_names = ["field", "data"]
    question_table.header = False
    question_table._max_table_width = term.width
    question_table._max_width = {"data": 80}

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
        result = db.vote(question_post["Id"], user_id)
        if result:
            question_post["Score"] += 1
            print("Vote successful!")
            input("Press enter key to continue")
        else:
            print("You already voted on this!")
            input("Press enter key to continue")
    elif action == "4":
        global CURRENT_STATE
        CURRENT_STATE = "PROMPT"
    else:
        print("error: please choose one of the actions")
        input("Press enter key to continue")


def answer_question():
    global answer_post, user_id, CURRENT_STATE

    answer_text = input("answer: ")

    # Change answer_post to current answer
    answer_post = db.answer_question(user_id, question_post["Id"], answer_text)

    CURRENT_STATE = "ANSWER"


def list_answers():
    clear_term("Answers")
    (accepted_answer, answers) = db.get_answers(question_post["Id"])

    all_answers = []

    global CURRENT_STATE

    answers_table = PrettyTable()
    answers_table.field_names = ["# ", "Accepted", "Id", "Answer", "Post Date", "Score"]
    answers_table._max_width = {"Answer": 80}
    answers_table._max_table_width = term.width - 10
    answers_table.hrules = prettytable.ALL

    count = 0

    if accepted_answer is not None:
        answers_table.add_row(
            [
                (count % 5) + 1,
                "*",
                accepted_answer["Id"],
                accepted_answer["Body"].replace("\n", "")[:80],
                accepted_answer["CreationDate"],
                accepted_answer["Score"],
            ]
        )

        all_answers.append(accepted_answer)
        count += 1

    if len(answers) != 0:
        for ans in answers:
            answers_table.add_row(
                [
                    (count % 5) + 1,
                    "",
                    ans["Id"],
                    ans["Body"].replace("\n", "")[:80],
                    ans["CreationDate"],
                    ans["Score"],
                ]
            )

            count += 1

        all_answers.extend(answers)

    if len(all_answers) == 0:
        print("No Answers. Going back to Question view.")
        input("Press enter key to continue")
        CURRENT_STATE = "QUESTION"
    else:
        print(answers_table)

        while True:
            selection = int(
                input("\nPlease select an answer to read (or 0 to return to menu): ")
            )

            if selection == 0:
                CURRENT_STATE = "PROMPT"
                break
            elif selection <= len(all_answers):
                global answer_post
                answer_post = all_answers[selection - 1]
                CURRENT_STATE = "ANSWER"
                break
            else:
                print("Incorrect number. Please try again.")
                input("Press enter key to continue")


def answer():
    global question_post, answer_post, CURRENT_STATE

    clear_term("Answer")

    print("Original question:")
    question_table = PrettyTable()

    for key in question_post:
        question_table.add_row([key, question_post[key]])

    question_table.field_names = ["field", "data"]
    question_table.header = False
    question_table._max_table_width = term.width
    question_table._max_width = {"data": 80}

    print(term.center(str(question_table)))

    print("\nAnswer: ")

    answers_table = PrettyTable()
    for key in answer_post:
        answers_table.add_row([key, answer_post[key]])

    answers_table.field_names = ["field", "data"]
    answers_table.header = False
    answers_table._max_table_width = term.width
    answers_table._max_width = {"data": 80}

    print(term.center(str(answers_table)))

    print("Select an action:")
    print("1. Vote")
    print("2. Go back to menu")
    action = input()
    if action == "1":
        result = db.vote(answer_post["Id"], user_id)
        if result:
            answer_post["Score"] += 1
            print("Vote successful!")
            input("Press enter key to continue")
        else:
            print("You already voted on this!")
            input("Press enter key to continue")
    elif action == "2":
        CURRENT_STATE = "PROMPT"
    else:
        print("error: please choose one of the actions")
        input("Press enter key to continue")


def run_state():
    states = {
        "LOGIN": login,  # Login screen
        "POST": post,  # Making a new post
        "SEARCH": search,  # Search for posts
        "QUESTION": question,  # Question view
        "ANSWER": answer,  # Answer view
        "PROMPT": prompt_menu,
    }

    if CURRENT_STATE == "EXIT":
        print("Exiting program")
        print(term.clear)
        exit(0)
    else:
        states[CURRENT_STATE]()


if __name__ == "__main__":
    # set up db stuff
    port = 27017
    if len(sys.argv) == 2:
        port = int(sys.argv[1])

    db = Database(port)
    # Run

    while True:
        run_state()
