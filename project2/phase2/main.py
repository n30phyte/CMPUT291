import blessed

from database import Database

user_id = None
content_license = "CC BY-SA 2.5"
post_id = None

# todo: "after each action, the user should be able to return to the main menu for further operations


def prompt_login():
    uid = input("user id (press enter to proceed without report): ")
    # verify uid is all numeric
    if uid.isdecimal():
        # query for uid and present report
        user_report(uid)
    elif not uid:
        print("no user id entered, proceeding...")
    else:
        # todo: 3 uid attempts? if uid doesn't exist or if not all numbers
        print("error: uid must be all numeric, proceeding...")


def user_report(uid):
    print("user report for:", uid)
    print("...")
    user_id = uid
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
    tags = input("tags: ")
    # todo: record post in db: unique id, post type id = 1, post creation date = today, owner user id = user_id
    #  Score = 0, ViewCount = 0, AnswerCount = 0, CommentCount = 0, content license = content_license
    # question_id =


def search_questions():
    keywords = input("search keywords: ")
    # todo: search keywords in title body or tags (case intensitive)
    #  for each matching question, display title, creation date, score, answer count
    #  user can: select question to see all fields, view count of question += 1, perform action


def question():
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
    answer = input("answer: ")
    # todo: insert answer record into db w/ body field = answer
    #  assign unique id, post type id = 2, post creation date = today, owner user id = user_id, parent_id = question_id
    #  Score = 0,  CommentCount = 0, content license = content_license


def list_answers():
    # todo: query for answers to question
    #  - accepted answer is first + marked with a star.
    #  - display first 80 char of body text, creation date, score.
    #  - user can select answer to see all fields of answer + perform answer actions
    pass


def answer():
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


def vote():
    # todo: user can vote on question/answer if not already voted on if logged in
    #  - anon users can vote w/ no constraint
    #  - record votes w/ unique vote id, post id = post_id, vote type id = 2, creation date = today
    #  - if user id is set, score field in Posts increases by 1
    pass


if __name__ == '__main__':
    # set up db stuff
    db = Database(27017)
    db.new_question(-1, "uwu", "uwu cummies", [])
    db.search_question(["macos"])
    # start
    prompt_login()
