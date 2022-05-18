import copy
import hashlib


class State:
    """Represent the state of a grid: state, path_history, and heuristic score."""

    def __init__(self, input_state):
        
        # don't just bind to input state. we want the object to have its OWN state
        # https://docs.python.org/2/library/copy.html
        self.state = copy.deepcopy(input_state)

        self.path_history = [copy.deepcopy(self.state)]

        self.n = len(input_state[0])

        self.hash = hashlib.sha256(str(self.state).encode()).digest()

    def move(self, direction):
        """Slide a tile in one of 4 directions.
        Return True if successful (with side-effect of changing the state).
        Return False if movement in that direction not possible. 
        """

        y0, x0 = self.locate_tile(0, self.state)

        # find the offset of the moving tile relative to the '0' tile
        # when we say 'move left' we mean the tile, not the space (0)
        if direction == 'up':
            y, x = 1, 0
        elif direction == 'down':
            y, x = -1, 0
        elif direction == 'left':
            y, x = 0, 1
        elif direction == 'right':
            y, x = 0, -1
        else:
            return False

        # return false if move not possible
        if not 0 <= y0 + y < self.n:
            return False
        if not 0 <= x0 + x < self.n:
            return False

        # swap tiles
        tile_to_move = self.state[y0 + y][x0 + x]
        self.state[y0][x0] = tile_to_move
        self.state[y0 + y][x0 + x] = 0

        # update hash
        self.hash = hashlib.sha256(str(self.state).encode()).digest()

        return True

    def locate_tile(self, tile, grid_state):
        """Return the co-ordinates of a given tile, given as a tuple.
        Assumes one unique tile in grid."""

        for (y, row) in enumerate(grid_state):
            for (x, value) in enumerate(row):
                if value == tile:
                    return (y, x)
