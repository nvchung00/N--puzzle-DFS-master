import copy
import hashlib
import sys


class Node:
    def __init__(self, tiles = [] , parent = None ):
        self.tiles = copy.deepcopy(tiles)
        self.parent = parent
        self.hash = hashlib.sha256(str(tiles).encode()).digest()
        self.n = len(tiles)

    def isGoal(self):
        return self.tiles == goal.tiles

    def findBlank(self): #find the blank in a node's tiles
        tiles = self.tiles
        for i in range(self.n):
            for j in range(self.n):
                if tiles[i][j] == '_':
                    return i, j

    def genChildren(self):
        tiles = self.tiles
        x, y = self.findBlank()
        newTiles = []
        if x + 1 < self.n: #moving blank down / moving a tile up
            new = copy.deepcopy(tiles)
            new[x][y] = new[x+1][y]
            new[x+1][y] = '_'
            newTiles.append(new)
        if x - 1 > -1: #moving blank up / moving a tile down
            new = copy.deepcopy(tiles)
            new[x][y] = new[x-1][y]
            new[x-1][y] = '_'
            newTiles.append(new)
        if y + 1 < self.n:  # moving blank right / moving a tile left
            new = copy.deepcopy(tiles)
            new[x][y]=new[x][y+1]
            new[x][y+1]='_'
            newTiles.append(new)
        if y - 1 > -1: # moving blank left / moving a tile right
            new = copy.deepcopy(tiles)
            new[x][y] = new[x][y - 1]
            new[x][y-1] = '_'
            newTiles.append(new)
        ret = []
        for i in newTiles: #create children nodes
            child = Node(tiles=i, parent=self)
            ret.append(child)
        return ret

    
def dfs(start , goal):
    lst = [] 
    lst.append(start)
    vst = set()
    while lst:
        u = lst.pop()
        if u.isGoal():
            return u
        if u.hash not in vst:
            vst.add(u.hash)
            for w in u.genChildren():
                if w.hash not in vst:
                    lst.append(w)
    return None


def getInput(fileName):
    with open(fileName, "r") as f:
        data = f.read().strip().splitlines()
    n = int(data[0])
    tiles = []
    startTiles = [data[i + 1].strip().split() for i in range(n)]
    start = Node(startTiles)
    goalTiles = [data[i + 1 + n].strip().split() for i in range(n)]
    goal = Node(goalTiles)
    return start, goal


def output(fileName, path):
    res = ""
    n = len(path[0])
    for i in path:
        for row in i:
            for x in row:
                res += str(x).rjust(5)
            res += "\n"
        res += "=" * 20
        res += "\n"
    open(fileName, "w").write(res)


if __name__ == '__main__':
    inFile, outFile = sys.argv[1], sys.argv[2]
    start, goal = getInput(inFile)

    res = dfs(start, goal)

    if res is None:
        print("No solution.")
        sys.exit()

    path = [res.tiles]
    while True:
        res = res.parent
        path.append(res.tiles)
        if res.parent is None:
            break

    output(outFile, path[::-1])
    print("SUCCESS !")
    print("Number of steps:", len(path))
