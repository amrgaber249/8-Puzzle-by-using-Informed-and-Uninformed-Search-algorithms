
from puzzleBoard import *
import heapq


def bfsSearch(initialState):
    '''
    The main idea here is that we will use the None value to
    indicate the end of each level hence the depth of our solution.

    After finishing a level, the next state will be equal to None,
    in which case we are able to easily identify the end of the current level.

    We will use a list as a queue for holding our states.
    '''
    # initializing our root (depth=0)
    frontier = [initialState, None]
    explored = []
    depth = 0
    # to find when to add None (end of level) to our queue
    flag = 0

    while len(frontier) > 0:
        # .pop(0) -> remove the first element of the list
        state = frontier.pop(0)

        # if None then we reached the end of our current level and raise flag
        if not state:
            depth += 1
            flag = 1
            continue

        # add None to our queue and reset the flag value
        if flag:
            frontier.append(None)
            flag = 0

        # add the current state to our explored list
        explored.append(state.tilesToList())

        # check if the current state is the solution to our puzzle
        if goalTest(state):
            return success(state, len(explored), depth)

        # add the neighbours to our current node
        # only if they are not in (explored U frontier)
        for neighbour in state.children():
            if not checkExp(neighbour, explored):
                if not checkFront(neighbour, frontier):
                    frontier.append(neighbour)

    # in case we couldn't solve the puzzle
    return False


def dfsSearch(initialState):
    '''
    The main idea here is that we will use the None value to
    calculate our current depth.

    if the current state has a neighbour not in (explored U frontier),
    we will add None, otherwise we will not add None, because the current state 
    has no children and we will have to pop another state from the stack.

    We will use a list as a stack for holding our states.
    '''
    # initializing our root (depth=0)
    frontier = [initialState]
    explored = []
    # not used
    maxDepth = 0
    depth = 0
    # to find when to add None (node expanded) to our stack
    flag = 0

    while len(frontier) > 0:
        # .pop() -> remove the last element of the list
        state = frontier.pop()

        # if None then we are going to the parent
        if not state:
            continue

        # the number of None in our list will be our depth
        depth = frontier.count(None)

        # not used but can calculate our max Depth
        maxDepth = max(maxDepth, depth)

        # add the current state to our explored list
        explored.append(state.tilesToList())

        # check if the current state is the solution to our puzzle
        if goalTest(state):
            return success(state, len(explored), depth)

        # limit our search to a specific depth to not have the states expand to reach our max Depth,
        # which can cause Memory &/or deepcopy errors
        depthLimit = 50
        if depth < depthLimit:
            # find where is the start of our expansion nodes
            # to add our None before them
            row = len(frontier)
            # add the neighbours to our current node
            # only if they are not in (explored U frontier)
            for neighbour in state.children():
                if not checkExp(neighbour, explored):
                    if not checkFront(neighbour, frontier):
                        # raise the flag if we found a neighbour
                        flag = 1
                        frontier.append(neighbour)

            # if we didn't expand, we will not add None
            if flag == 1:
                # insert None before the added neighbours
                frontier.insert(row, None)
                # reset flag
                flag = 0
    # in case we couldn't solve the puzzle
    return False


def astarSearch(initialState, type):
    frontier = []
    explored = []
    # calculate the cost depending on the type of Heuristics
    cost = manhattanDistance(
        initialState) if type == "manhattan" else euclideanDistance(initialState)
    # create a tuple for the node to hold the cost which will be used to by the heapsort,
    # and its state
    node = (cost, initialState)
    heapq.heappush(frontier, node)
    while len(frontier) > 0:
        state = heapq.heappop(frontier)[1]

        # add the current state to our explored list
        explored.append(state.tilesToList())

        #  check if the current state is the solution to our puzzle
        if goalTest(state):
            # find the depth by tracing back the root parent of the state
            depth = 0
            temp = state
            while temp:
                # print(temp)
                depth += 1
                temp = temp.parent
            return success(state, len(explored), depth)

        # add the neighbours to our current node
        # only if they are not in (explored U frontier)
        for neighbour in state.children():
            if not checkExp(neighbour, explored):
                if not checkFront(neighbour, [state for cost, state in frontier]):
                    # calculate the cost depending on the type of Heuristics
                    cost = manhattanDistance(
                        neighbour) if type == "manhattan" else euclideanDistance(neighbour)
                    node = (cost, neighbour)
                    heapq.heappush(frontier, node)
    # in case we couldn't solve the puzzle
    return False


# calculate the Manhattan Distance
# h=𝑎𝑏𝑠(𝑐𝑢𝑟𝑟𝑒𝑛𝑡𝑐𝑒𝑙𝑙.𝑥−𝑔𝑜𝑎𝑙.𝑥)+𝑎𝑏𝑠(𝑐𝑢𝑟𝑟𝑒𝑛𝑡𝑐𝑒𝑙𝑙.𝑦−𝑔𝑜𝑎𝑙.𝑦)
def manhattanDistance(state):
    tiles = state.tilesToList()
    h = state.cost
    for i in range(len(tiles)):
        if tiles[i] != 0:
            currentCellX, currentCellY, goalCellX, goalCellY = getXY(
                i, tiles[i], state.size)
            h += (abs(currentCellX - goalCellX) +
                  abs(currentCellY - goalCellY))
    return h


# calculate the Euclidean Distance
# h=𝑠𝑞𝑟𝑡((𝑐𝑢𝑟𝑟𝑒𝑛𝑡𝑐𝑒𝑙𝑙.𝑥−𝑔𝑜𝑎𝑙.𝑥)2+𝑠𝑞𝑟𝑡((𝑐𝑢𝑟𝑟𝑒𝑛𝑡𝑐𝑒𝑙𝑙.𝑦−𝑔𝑜𝑎𝑙.𝑦)2)
def euclideanDistance(state):
    tiles = state.tilesToList()
    h = state.cost
    for i in range(len(tiles)):
        if tiles[i] != 0:
            currentCellX, currentCellY, goalCellX, goalCellY = getXY(
                i, tiles[i], state.size)
            h += ((currentCellX - goalCellX)**2 +
                  (currentCellY - goalCellY)**2)**0.5
    return h


# get x, y values for the currentCell and the goalCell
def getXY(i, tile, size):
    return i // size, i % size, tile // size, tile % size


# check if the neighbour state is explored or not
def checkExp(neighbour, explored):
    return neighbour.tilesToList() in explored


# check if the neighbour state is in the frontier or not
def checkFront(neighbour, frontier):
    for state in frontier:
        if not state:
            continue
        if state.tilesToList() == neighbour.tilesToList():
            return True
    return False


# get the solution to our puzzle
def goalTest(state):
    return state.isSolved()


# print our the full path taken to solve the puzzle from start to finish
def success(state, lenExplored, depth):
    fullStates = []
    fullPath = []
    fullCost = state.cost
    size = state.size
    while state:
        fullStates.append(state)
        fullPath.append(state.direction)
        state = state.parent
    pathTaken = ""
    fullStats = fullStates[::-1]
    fullPath = fullPath[::-1]
    for i, state in enumerate(fullStats[:-1]):
        state.displayBoard2()
        print("DIRECTION: ", fullPath[i])
        pathTaken += " -> " + fullPath[i]
    fullStats[-1].displayBoard3()
    print("DIRECTION: ", fullPath[-1])
    print("*"*size, "DONE", "*"*size)
    print()
    pathTaken += " -> " + fullPath[-1]

    print("Path Taken: ", pathTaken)
    print("Cost of that path: ", fullCost)
    print("Nodes Expanded: ", lenExplored)
    print("Search Depth: ", depth)
    return True


def main():
    import sys
    import time
    initialState = [int(num) for num in sys.argv[1].split(",")]
    searchType = sys.argv[2].lower()
    # start the clock
    tick = time.time()
    # initalize the puzzle with the input state
    puzzle = puzzleBoard(initialState)
    # check if the puzzle can be solved before applying the search algorithm
    # puzzle.canBeSolved()
    if searchType == "bfs":
        if not bfsSearch(puzzle):
            raise Exception(
                f"{ANSI_RED}THIS PUZZLE CANNOT BE SOLVED, TRY ANOTHER INITIAL STATE !!!{ANSI_RESET}")
    elif searchType == "dfs":
        if not dfsSearch(puzzle):
            raise Exception(
                f"{ANSI_RED}THIS PUZZLE CANNOT BE SOLVED, TRY ANOTHER INITIAL STATE !!!{ANSI_RESET}")
    else:
        type = searchType.split(",")[1]
        if not astarSearch(puzzle, type):
            raise Exception(
                f"{ANSI_RED}THIS PUZZLE CANNOT BE SOLVED, TRY ANOTHER INITIAL STATE !!!{ANSI_RESET}")
    # end the clock
    tock = time.time()
    print(f"Running Time: {tock-tick:.4f} sec")


if __name__ == '__main__':
    main()
