from util import clear


class State:
    """
    A generic State Class
    """

    stacks = True
    running = False
    manager = None

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

    states = {}
    state_stack = []

    PREV_STATE = "_PREV_STATE_"

    def add_state(self, state, name):
        self.states[name] = state
        state.manager = self

    def start(self, start_state):
        self.state_stack.insert(0, start_state)
        self.states[self.state_stack[0]]._enter()

    def change_state(self, next_state_name):
        if next_state_name == self.PREV_STATE:
            self.states[self.state_stack[0]]._exit()
            del self.state_stack[0]
        else:
            # TODO: error handling if a state node of that name doesnt exist
            if not next_state_name in self.states:
                print("no such state name: %s" % next_state_name)
                return
            nextState = self.states[next_state_name]
            # special case: state that uses the state stack, append to the stack
            if not nextState.stacks and next_state_name in self.state_stack:
                while self.state_stack[0] != next_state_name:
                    self.states[self.state_stack[0]]._exit()
                    del self.state_stack[0]
            else:
                self.state_stack.insert(0, next_state_name)
                nextState._enter()
