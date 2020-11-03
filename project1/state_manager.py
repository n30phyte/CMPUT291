from util import clear


class State:
    """
    A generic State Class
    """
    stacks = True
    running = False
    manager = None

    def _enter(self):
        self.running = True
        clear()
        self.enter()
        while self.running:
            self.loop()

    def enter(self):
        pass

    def loop(self):
        pass

    def _leave(self):
        self.running = False
        self.leave()

    def leave(self):
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
        """
        Start the state machine at the given state name

        :param start_state: name of state to start at
        """

        self.state_stack.insert(0, start_state)
        self.states[self.state_stack[0]]._enter()

    def change_state(self, next_state_name):
        """
        enters the state object with the given state name
        in the special case that the name is PREV_STATE, it will pop the current state and conitue the previous state
        otherwise if the next state stacks it will append it to the stack
        if it is neither PREV_STATE or a stacking state, it will replace the current state

        :param next_state_name: name of state to enter
        """

        # special case: previous state
        if next_state_name == self.PREV_STATE:
            self.states[self.state_stack[0]]._leave()
            del self.state_stack[0]
        else:
            if not next_state_name in self.states:
                print("no such state name: %s" % next_state_name)
                return
            nextState = self.states[next_state_name]
            # case: non stacking state
            if not nextState.stacks and next_state_name in self.state_stack:
                while self.state_stack[0] != next_state_name:
                    self.states[self.state_stack[0]]._leave()
                    del self.state_stack[0]
            # case: stacking state
            else:
                self.state_stack.insert(0, next_state_name)
                nextState._enter()
