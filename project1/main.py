from database import Database
from state_manager import StateManager
from states import LoginState, PostState, MenuState
import shared

def post_question(db, user):
    """
    User can post a question by providing title and body text

    :return:
    """
    print("Create a new post")
    title = input("Title: ")
    body = input("Body: ")
    db.new_question(title, body, user)


def homepage(db, user):
    while True:
        action_enums = 0
        print("1. Post a question")
        print("2. Search for posts")
        print("3. Post - Answer")
        print("4. Post - Vote")
        if user.is_privileged():
            print("5. Post - Mark as the accepted")
            print("6. Post - Give a badge")
            print("7. Post - Add a tag")
            print("8. Post - Edit")
        action = input("Choose an action from above")
        if action == 1:
            post_question(db, user)
        elif action == 2:
            search_post()


if __name__ == "__main__":
    shared.db = Database()

    sm = StateManager()
    sm.add_state(LoginState(), "login")
    sm.add_state(PostState(), "postEditor")
    sm.add_state(MenuState(), "menu")

    sm.start("login")

    # term = Terminal()
    # user = login(db)
    # homepage(db, user)
