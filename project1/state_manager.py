from util import clear
from shared import term


class State:
    """
    A generic State Class
    """

    stacks = False
    running = False
    manager = None

    def _enter(self):
        self.running = True
        clear()
        print(term.home + term.clear + term.move_y(0))
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
    current = None

    def add_state(self, state, name):
        self.states[name] = state
        state.manager = self

    def start(self, start_state):
        """
        Start the state machine at the given state name

        :param start_state: name of state to start at
        """

        self.current = self.states[start_state]
        self.current._enter()

    def change_state(self, next_state_name):
        """
        leaves the current state and
        enters the state object with the given state name

        :param next_state_name: name of state to enter
        """

        if not next_state_name in self.states:
            print("no such state name: %s" % next_state_name)
            return
        # case: non stacking state
        self.current._leave()
        self.current = self.states[next_state_name]
        self.current._enter()
