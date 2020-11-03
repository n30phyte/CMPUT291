from database import Database
from state_manager import StateManager
from states import *
import shared

if __name__ == "__main__":
    shared.db = Database()

    sm = StateManager()
    sm.add_state(LoginState(), "login")
    sm.add_state(PostState(), "post")
    sm.add_state(MenuState(), "menu")
    sm.add_state(QuestionState(), "question")
    sm.add_state(SearchState(), "search")
    sm.add_state(AnswerState(), "answer")

    sm.start("login")

    # term = Terminal()
    # user = login(db)
    # homepage(db, user)
