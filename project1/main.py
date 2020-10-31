from database import Database
from StateManager import StateManager
from states import LoginState, PostState

if __name__ == "__main__":
    db :Database = Database()

    sm = StateManager()
    sm.addState(LoginState(), "login")
    sm.addState(PostState(), "postEditor")\

    sm.start("login")
