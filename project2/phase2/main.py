from database import Database

user_id = ""
content_license = "CC BY-SA 2.5"
question_post = {}
answer_post = {}
db = None


# todo: "after each action, the user should be able to return to the main menu for further operations


def prompt_login():
    uid = input("user id (press enter to proceed without report): ")
    # verify uid is all numeric
    if uid.isdecimal():
        user_report(uid)
    elif not uid:
        print("no user id entered, proceeding to menu...")
    else:
        print("error: uid must be all numeric, proceeding to menu...")
    prompt_menu()


def user_report(uid):
    global user_id
    result = db.get_report(user_id)
    print("user report for:", uid)
    print(
        "number of questions owned (avg score): {} ({})".format(
            result["num_questions"], result["avg_q_votes"]
        )
    )
    print(
        "number of answers   owned (avg score): {} ({})".format(
            result["num_answers"], result["avg_a_votes"]
        )
    )
    prompt_menu()


def prompt_menu():
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
    title = input("title: ")
    body = input("body: ")
    tags = input("tags: ").split()
    # create post and go to post
    global question_post
    question_post = db.new_question(user_id, title, body, tags)
    print("post created!")
    question()


# todo: cynthia
#  display accepted answer first
#  check if number of results are 0
def search_questions():
    keywords = input("search keywords: ").split()
    results = db.search_question(keywords)

    # todo: remove min 5 range later
    for i in range(min(len(results), 5)):
        post = results[i]
        print("{}. title: {}".format(i + 1, post["Title"]))
        print(
            "    creation date: {}; score: {}; answer count: {}".format(
                post["CreationDate"], post["Score"], post["AnswerCount"]
            )
        )

    print("select a post by it's number or enter 0 to return to menu")
    action = input()

    if action == "0":
        prompt_menu()
    elif int(action) <= len(results):
        global question_post
        question_post = results[int(action)]
        db.visit_question(question_post["Id"])
        question()
    else:
        print("error: please choose one of the actions")


def question():
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
        vote()
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


# todo: michael
def list_answers():
    # todo: query for answers to question
    #  - accepted answer is first + marked with a star.
    #  - display first 80 char of body text, creation date, score.
    #  - user can select answer to see all fields of answer + perform answer actions
    answers = db.get_answers(question_post["Id"])


def answer():
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
        vote()
    elif action == "2":
        prompt_menu()
    else:
        print("error: please choose one of the actions")


# todo: michael
def vote():
    # todo: user can vote on question/answer if not already voted on if logged in
    #  - anon users can vote w/ no constraint
    #  - record votes w/ unique vote id, post id = post_id, vote type id = 2, creation date = today
    #  - if user id is set, score field in Posts increases by 1
    pass


if __name__ == "__main__":
    # set up db stuff
    db = Database(27017)
    # start
    prompt_login()
