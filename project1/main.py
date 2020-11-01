from database import Database
from state_manager import StateManager
from states import LoginState, PostState, MenuState
import shared
from ui import UserInterface

if __name__ == "__main__":
    shared.db = Database()

    sm = StateManager()
    sm.add_state(LoginState(), "login")
    sm.add_state(PostState(), "postEditor")
    sm.add_state(MenuState(), "menu")

    sm.start("login")
