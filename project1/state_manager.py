from util import clear


class State:
    """
    A generic State Class
    """

    stacks = True
    running = False

    def _enter(self):
        running = True
        clear()
        self.enter()
        while running:
            self.process()

    def enter(self):
        pass

    def process(self):
        pass

    def _exit(self):
        running = False
        exit()

    def exit(self):
        pass


class StateManager:
    """
    A generic state machine class that will manage and transition between states
    """

    # keep track of the current state and state history
    # MAKE SURE TO SET THE START_STATE
    states = {}
    stateStack = []

    PREV_STATE = "_PREV_STATE_"

    def add_state(self, state: State, name: str):
        self.states[name] = state
        state.manager = self

    def start(self, start_state: str):
        self.stateStack.insert(0, start_state)
        self.states[self.stateStack[0]].enter()

    def change_state(self, next_state_name: str):
        if next_state_name == self.PREV_STATE:
            self.states[self.stateStack[0]]._exit()
            del self.stateStack[0]
        else:
            # TODO: error handling if a state node of that name doesnt exist
            if not next_state_name in self.states:
                print("no such state name: %s" % next_state_name)
                return
            next_state = self.states[next_state_name]
            # special case: state that uses the state stack, append to the stack
            if not next_state.stacks and next_state_name in self.stateStack:
                while self.stateStack[0] != next_state_name:
                    self.states[self.stateStack[0]]._exit()
                    del self.stateStack[0]
            else:
                self.stateStack.insert(0, next_state_name)
                next_state.enter()
