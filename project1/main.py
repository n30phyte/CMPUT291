from database import Database
from state_manager import StateManager
from states import LoginState, PostState
from .shared import *

if __name__ == "__main__":
    db = Database()

    sm = StateManager()
    sm.addState(LoginState(), "login")
    sm.addState(PostState(), "postEditor")\

    sm.start("login")
