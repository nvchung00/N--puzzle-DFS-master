from state import State
from metric import Metric
import copy
import math


class Solver:

    """N-Puzzle Solver Class"""
    
    def __init__(self, init_list, goal_list):
        """Initialise Solver object. Raise ValueError if solution not possible."""

        self.initial_state = copy.deepcopy(self.list_to_grid(init_list))

        self.goal_state = copy.deepcopy(self.list_to_grid(goal_list))

        self.frontier = []
        self.explored = set()

        self.metrics = Metric(self.frontier)

    def dfs(self):
        """Explore search space using depth-first search"""

        self.metrics.start_timer()

        initial_state = State(self.initial_state)
        self.frontier.append(initial_state)
        
        # while stack is not empty..
        while self.frontier:

            state = self.frontier.pop()

            self.metrics.search_depth = len(state.path_history)
            self.metrics.update_max_depth()

            self.explored.add(state.hash)

            if self.goal_test(state):
                self.metrics.path_to_goal = state.path_history
                self.metrics.stop_timer()
                return self.metrics

            self.expand_nodes(state)

        # dead
        raise ValueError('Shouldn\'t have got to here')

    def expand_nodes(self, starting_state):
        """Take a grid state, add all possible 'next moves' to the frontier"""

        node_order = ['down', 'up', 'right', 'left']

        for node in node_order:   

            # the program is imagining the future!! (maybe change this name...)
            imagined_state = State(starting_state.state)

            # pass path history from previous grid to the next grid
            # using copy to avoid python's reference bindings
            imagined_state.path_history = copy.copy(starting_state.path_history)

            if imagined_state.move(node):  # returns false if move not possible

                imagined_state.path_history.append(copy.deepcopy(imagined_state.state))

                if imagined_state.hash not in self.explored:
                    self.frontier.append(imagined_state)
                    self.metrics.update_max_fringe()

            self.metrics.nodes_expanded += 1

    def goal_test(self, state):
        """Compare a given state to the goal state. Return Boolean"""

        if state.state == self.goal_state:
            return True
        else:
            return False

    def list_to_grid(self, tile_list):
        """Take a list of length n^2, return a nxn 2D list"""

        n = math.isqrt(len(tile_list))
        return [tile_list[i:i+n] for i in range(0, len(tile_list), n)]
