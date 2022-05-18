import sys
import copy
import hashlib


class Node:  # node class
    def __init__(self, tiles=[], parent=None):  # parent for reconstructing path
        self.tiles = copy.deepcopy(tiles)
        self.parent = parent
        self.hash = hashlib.sha256(str(tiles).encode()).digest()
        self.n = len(tiles)

    def findBlank(self):  # find the blank in a node's tiles
        for i in range(self.n):
            for j in range(self.n):
                if self.tiles[i][j] == '_':
                    return i, j

    def genChildren(self):  # generate all moves
        x0, y0 = self.findBlank()
        moves = ["up", "down", "right", "left"]
        children = []
        for move in moves:
            if move == "left":
                x, y = 0, 1
            elif move == "right":
                x, y = 0, -1
            elif move == "up":
                x, y = -1, 0
            elif move == "down":
                x, y = 1, 0
            if 0 <= x0 + x < self.n and 0 <= y0 + y < self.n:
                tmp = copy.deepcopy(self.tiles)
                tmp[x0][y0], tmp[x0 + x][y0 + y] = tmp[x0 + x][y0 + y], tmp[x0][y0]
                child = Node(tiles=tmp, parent=self)
                children.append(child)
        return children


def error(err):
    print(err)
    sys.exit()


class Solver:  # solver class
    def __init__(self):
        self.n = None
        self.start = None
        self.goal = None

    def checkTiles(self, tiles):  # check if tiles is valid
        return set(sum(tiles, [])) == set(list(map(str, range(1, self.n**2))) + ["_"])

    def load(self, inFile):  # load problem from file, define `start` and `goal`
        data = open(inFile, "r").read().strip().splitlines()
        n = int(data[0])
        self.n = n

        startTiles = [data[i + 1].strip().split() for i in range(n)]
        if not self.checkTiles(startTiles):
            error("Invalid start tiles!")
        self.start = Node(startTiles)

        goalTiles = [data[i + 1 + n].strip().split() for i in range(n)]
        if not self.checkTiles(goalTiles):
            error("Invalid goal tiles!")
        self.goal = Node(goalTiles)

    def save(self, outFile):  # save solution to output file
        res = ""
        for it in self.solution_path:
            for row in it:
                for x in row:
                    res += str(x).rjust(5)
                res += "\n"
            res += "-" * 20
            res += "\n"
        open(outFile, "w").write(res)

    def dfs(self):  # dfs algorithm
        stack = []
        stack.append(self.start)
        visited = set()
        while stack:  # while stack not empty
            u = stack.pop()
            if u.tiles == self.goal.tiles:  # we reached goal
                return u
            if u.hash not in visited:
                visited.add(u.hash)
                for w in u.genChildren():
                    if w.hash not in visited:
                        stack.append(w)
        return None

    def solve(self):  # main solve function
        if not self.start:
            error("Undefined start state.")
        if not self.goal:
            error("Undefined goal state.")

        sol = self.dfs()

        if sol is None:
            error("No solution.")

        path = [sol.tiles]
        while True:  # reconstruct path from parent
            sol = sol.parent
            path.append(sol.tiles)
            if sol.parent is None:
                break
        self.solution_path = path[::-1]
        del path
        return len(self.solution_path)


def main():
    inFile, outFile = sys.argv[1], sys.argv[2]
    
    s = Solver()
    s.load(inFile)
    n_step = s.solve()
    s.save(outFile)

    print("SUCCESS!")
    print("Number of steps:", n_step)


if __name__ == "__main__":
    main()
