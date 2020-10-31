from util import clear

class State:
    """
    A generic State Class
    """
    stacks :bool = True
    running :bool  = False
    manager = None

    def _enter(self):
        running = True
        clear()
        self.enter()
        while (running):
            self.process();

    def enter(self): pass

    def process(self): pass

    def _exit(self):
        running = False
        exit()

    def exit(self): pass

class StateManager:
    """
    A generic state machine class that will manage and transition between states
    """
    states : dict = {}
    stateStack : list = []

    PREV_STATE : str = "_PREV_STATE_"

    def addState(self, state: "State", name :str):
        self.states[name] = state
        state.manager = self

    def start(self, startState : str):
        self.stateStack.insert(0, startState)
        self.states[self.stateStack[0]]._enter()

    def changeState(self, nextStateName : str):
        if nextStateName == self.PREV_STATE:
            self.states[self.stateStack[0]]._exit()
            del self.stateStack[0]
        else:
            # TODO: error handling if a state node of that name doesnt exist
            if not nextStateName in self.states:
                print("no such state name: %s" % nextStateName)
                return
            nextState = self.states[nextStateName]
            # special case: state that uses the state stack, append to the stack
            if not nextState.stacks and nextStateName in self.stateStack:
                while(self.stateStack[0] != nextStateName):
                    self.states[self.stateStack[0]]._exit()
                    del self.stateStack[0]
            else:
                self.stateStack.insert(0, nextStateName)
                nextState._enter()
