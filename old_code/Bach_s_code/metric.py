import copy
import time


class Metric:

    """Take measurements of search performance."""

    def __init__(self, frontier):

        self.path_to_goal = []
        self.nodes_expanded = 0
        self.fringe = frontier
        self.max_fringe_size = 0
        self.search_depth = 0
        self.max_search_depth = 0
        self.start_time = 0
        self.end_time = 0
        self.search_time = 0

    def cost_of_path(self):
        """Return the number of steps taken to reach the goal"""
        return len(self.path_to_goal)

    def fringe_size(self):
        """Return the length of the fringe (frontier)"""
        return len(self.fringe)

    def update_max_fringe(self):
        """Update the value of max_fringe_size!"""
        fringe_length = self.fringe_size()
        if fringe_length > self.max_fringe_size:
            self.max_fringe_size = fringe_length

    def update_max_depth(self):
        """Update the maximum search depth reached"""
        if self.search_depth > self.max_search_depth:
            self.max_search_depth = copy.copy(self.search_depth)

    def start_timer(self):
        """Set start time"""
        self.start_time = time.time()

    def stop_timer(self):
        """Set stop time"""
        self.end_time = time.time()
        self.search_time = "{0:.2f}".format((self.end_time - self.start_time) * 1000)
