import blessed

from database import Database

user_id = ""
content_license = "CC BY-SA 2.5"
focus_post = {}
db = None


# todo: "after each action, the user should be able to return to the main menu for further operations

# complete
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


# completed
def user_report(uid):
    global user_id
    result = db.get_report(user_id)
    print("user report for:", uid)
    print("number of questions owned (avg score): {} ({})".format(result['num_questions'], result['avg_q_votes']))
    print("number of answers   owned (avg score): {} ({})".format(result['num_answers'], result['avg_a_votes']))
    prompt_menu()


# complete
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


# complete
def post_question():
    title = input("title: ")
    body = input("body: ")
    tags = input("tags: ").split()
    # create post and go to post
    global focus_post
    focus_post = db.new_question(user_id, title, body, tags)
    print("post created!")
    question()


# todo: cynthia
#  display accepted answer first
def search_questions():
    keywords = input("search keywords: ").split()
    results = db.search_question(keywords)
    num = 1
    for result in results:
        print("{}. title: {}".format(num, result['Title']))
        print("    creation date: {}; score: {}; answer count: {}".format(result['CreationDate'], result['Score'], result['AnswerCount']))
        num += 1

    action = input("select a post by it's number or enter 0 to return to menu")
    if action == "0":
        prompt_menu()
    elif int(action) <= len(results):
        global focus_post
        focus_post = results[int(action)]
        db.visit_question(focus_post['Id'])
        question()
    else:
        print("error: please choose one of the actions")


# complete
def question():
    print("question: ")
    print("title: {}".format(focus_post['title']))
    print("body: {}".format(focus_post['body']))
    print("tags: {}".format(focus_post['tags']))

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


# complete
def answer_question():
    answer_text = input("answer: ")
    # todo: insert
    global focus_post
    global user_id
    # change focus post to answer
    focus_post = db.answer_question(user_id, focus_post['Id'], answer_text)
    answer()


# todo: michael
def list_answers():
    # todo: query for answers to question
    #  - accepted answer is first + marked with a star.
    #  - display first 80 char of body text, creation date, score.
    #  - user can select answer to see all fields of answer + perform answer actions
    answers = db.get_answers(focus_post['Id'])


# complete
def answer():
    print("answer: ")
    global focus_post
    print("title: {}".format(focus_post['title']))
    print("body: {}".format(focus_post['body']))
    print("tags: {}".format(focus_post['tags']))

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


if __name__ == '__main__':
    # set up db stuff
    db = Database(27017)
    # start
    prompt_login()
