from database import Database
from state_manager import StateManager
from states import *

import shared
import sys

if __name__ == "__main__":
    # allow database input
    if len(sys.argv) == 1:
        db_file = "db/database.db"
    else:
        db_file = sys.argv[1]

    shared.db = Database(db_file)

    # initialize state manager and insert all used states
    sm = StateManager()
    sm.add_state(LoginState(), "login")
    sm.add_state(PostState(), "post")
    sm.add_state(MenuState(), "menu")
    sm.add_state(QuestionState(), "question")
    sm.add_state(SearchState(), "search")
    sm.add_state(AnswerState(), "answer")
    sm.add_state(EditState(), "edit")

    sm.start("login")
