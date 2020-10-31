from StateManager import State;
from post import *
from .shared import *

class LoginState(State):
    def enter(self):
        hasAccount = input("Do you have an existintg account? ")
        if hasAccount != "yes":
            self.manager.changeState("register");
        print("* PLEASE LOGIN *")

    def process(self):
        username = input("Username: ");
        password = input("Password: ");
