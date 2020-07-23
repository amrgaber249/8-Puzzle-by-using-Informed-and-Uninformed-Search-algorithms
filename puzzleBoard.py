from copy import deepcopy

# used for changing the text color
# https://bluesock.org/~willkg/dev/ansi.html
ANSI_RESET = "\u001B[0m"
ANSI_RED = "\u001B[31m"
ANSI_GREEN = "\u001B[32m"
ANSI_YELLOW = "\u001B[33m"
ANSI_BLUE = "\u001B[34m"


class puzzleBoard():
    """
    This is the 8 puzzle board class,
    which consists of a board holding an empty tile and 8 distinct or more movable tiles.

    ...

    Attributes
    ----------
    initialState : list
        the initial state of the board
    cost : int
        the cost required to reach this puzzleBoard obj
    parent : puzzleBoard class obj
        the parent of the current child state (default root is None)
    randomize : boolean
        used to generate random initial board state (default False)
    randomSize : int
        the dimension size of the board AxA (default 3)
    """

    def __init__(self, initialState=[], cost=0, parent=None, randomize=False, randomSize=3):
        """
        The constructor for puzzleBoard class.

        ...

        Parameters
        ----------
        initialState : list
            the initial state of the board
        cost : int
            the cost required to reach this puzzleBoard obj
        parent : puzzleBoard class obj
            the parent of the current child state (default root is None)
        randomize : boolean
            used to generate random initial board state (default False)
        randomSize : int
            the dimension size of the board AxA (default 3)
        """
        # To Generate a random initial board state
        if randomize or not initialState:
            print("Generating Random Initial State")
            initialState = self.randomize(randomSize)

        # To make sure you entered a Squared Number for the board size
        self.checkSize(len(initialState), int(len(initialState)**0.5))

        # Initialize the board tiles
        self.tiles = []
        for i in range(self.size):
            row = []
            for j in range(self.size):
                row.append(initialState[self.size*i + j])
                if row[-1] == 0:
                    self.emptyTile = [i, j]
            self.tiles.append(row)

        # initialize the rest of the parameters
        self.cost = cost
        self.parent = parent

    # Used in the heap sort for comparisons
    def __lt__(self, state):
        return state.cost > self.cost

    # Method to make sure you enterd a squared number for the board size
    def checkSize(self, length, size):
        # board too small to be playable
        # in case you want to play with this board size
        # remove this condition and change the (elif size**2 == length) condition
        # to (if size**2 == length or length == 2)
        if size < 2:
            raise Exception(
                f"{ANSI_RED}INPUT SIZE IS TOO SMALL, MINIMUM SIZE IS 4{ANSI_RESET}")
        elif size**2 == length:
            self.size = size
            self.direction = "Start"
        else:
            raise Exception(
                f"{ANSI_RED}INCORRECT INPUT SIZE, YOUR INPUT {length} : CLOSEST SQUARE NUMBERS {size**2} OR {(size+1)**2}!!!{ANSI_RESET}")

    # print (minimal) board tiles
    def displayBoard(self):
        for i in range(self.size):
            print([self.tiles[i][j] for j in range(self.size)])

    # print (colorful) board tiles
    def displayBoard2(self):
        print("." + f"{ANSI_YELLOW}____"*self.size)
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                if self.tiles[i][j] == 0:
                    row += f"{ANSI_YELLOW}| {ANSI_RED}{self.tiles[i][j]:02d}"
                else:
                    row += f"{ANSI_YELLOW}| {ANSI_BLUE}{self.tiles[i][j]:02d}"
            print(row+f"{ANSI_YELLOW}|")
            print(f"{ANSI_YELLOW}|___"*self.size +
                  f"{ANSI_YELLOW}|{ANSI_RESET}")

    # print (all green) board tiles
    def displayBoard3(self):
        print("." + f"{ANSI_GREEN}____"*self.size)
        for i in range(self.size):
            row = ""
            for j in range(self.size):
                row += f"{ANSI_GREEN}| {self.tiles[i][j]:02d}"
            print(row+f"{ANSI_GREEN}|")
            print(f"{ANSI_GREEN}|___"*self.size +
                  f"{ANSI_GREEN}|{ANSI_RESET}")

    # return a new board state where the empty tile and the tile above it are swapped
    def moveUp(self):
        if self.emptyTile[0] != 0:
            self.moveTile([-1, 0])
            self.direction = "Move Up"
            return self

    # return a new board state where the empty tile and the tile below it are swapped
    def moveDown(self):
        if self.emptyTile[0] != self.size - 1:
            self.moveTile([1, 0])
            self.direction = "Move Down"
            return self

    # return a new board state where the empty tile and the tile left to it are swapped
    def moveLeft(self):
        if self.emptyTile[1] != 0:
            self.moveTile([0, -1])
            self.direction = "Move Left"
            return self

    # return a new board state where the empty tile and the tile right to it are swapped
    def moveRight(self):
        if self.emptyTile[1] != self.size - 1:
            self.moveTile([0, 1])
            self.direction = "Move Right"
            return self

    # do the swapping process
    def moveTile(self, tile):
        row = self.emptyTile[0] + (1 * tile[0])
        col = self.emptyTile[1] + (1 * tile[1])
        self.tiles[row][col], self.tiles[self.emptyTile[0]][self.emptyTile[1]] \
            = self.tiles[self.emptyTile[0]][self.emptyTile[1]], self.tiles[row][col]
        self.emptyTile = [row, col]

    # create a new instance of the puzzleBoard
    # otherwise Python will just use the same pointer over the copies
    def copy(self):
        return deepcopy(puzzleBoard(self.tilesToList(), parent=self, cost=self.cost+1))
    __copy__ = copy

    # change the 2-D matrix into 1-D list for ease of processing
    def tilesToList(self):
        return [tile for row in self.tiles for tile in row]

    # get a list of all the children nodes states of the current parent state
    def children(self):
        states = [self.copy() for i in range(4)]
        states[0].moveUp()
        states[1].moveDown()
        states[2].moveLeft()
        states[3].moveRight()
        return [states[i] for i in range(4) if states[i].emptyTile != self.emptyTile]

    # check if the initialState of the board can be solved or not
    def canBeSolved(self):
        if self.isSolved():
            return
        # if self.size == 2:
        #     solution = [[1, 0, 2, 3], [1, 3, 2, 0], [1, 3, 0, 2], [0, 3, 1, 2], [3, 0, 1, 2],
        #                 [3, 2, 1, 0], [3, 2, 0, 1], [0, 2, 3, 1], [2, 0, 3, 1], [2, 1, 3, 0], [2, 1, 0, 3]]
        #     if self.tilesToList not in solution:
        #         raise Exception(
        #             f"{ANSI_RED}THIS PUZZLE CANNOT BE SOLVED, TRY ANOTHER INITIAL STATE !!!{ANSI_RESET}")
        inv_count = 0
        for i in range(self.size-1):
            j = i + 1
            while j < self.size:
                print(self.tiles[j][i], self.tiles[i][j])
                if self.tiles[j][i] > 0 and self.tiles[j][i] > self.tiles[i][j]:
                    inv_count += 1
                j += 1
        if inv_count % 2 != 0:
            raise Exception(
                f"{ANSI_RED}THIS PUZZLE CANNOT BE SOLVED, TRY ANOTHER INITIAL STATE !!!{ANSI_RESET}")

    # create a random board state
    def randomize(self, size=3):
        import random
        size = size ** 2
        return random.sample(range(size), size)

    def solution(self):
        return [i for i in range(self.size**2)]

    def isSolved(self):
        return self.tilesToList() == self.solution()

# initialState = [1, 2, 3, 4, 5, 6, 7, 8, 0]
# x = puzzleBoard(initialState)
# print(x.emptyTile)
# x.displayBoard2()
# y = x.children()
# print("hi")

# def startGame(initialState=[]):
#     game = puzzleBoard(initialState)
#     # TODO: -ADD BUTTON INPUT
#     #       -Display Board after each input
#     #       -Check if solved


# def takeInputs():
#     startGame(input("Enter your number list seprated by a \"\,\""))


# def exitGame():
#     print("                                                                                                                       _____ ")
#     print(" _____                           _____                    _           _      _   _       _                            |___  |")
#     print("|  _  |___ ___    _ _ ___ _ _   |   __|_ _ ___ ___    ___| |_ ___ _ _| |_   | |_| |_ ___| |_    ___             ___     |  _|")
#     print("|     |  _| -_|  | | | . | | |  |__   | | |  _| -_|  | .'| . | . | | |  _|  |  _|   | .'|  _|  | . |           | . |    |_|  ")
#     print("|__|__|_| |___|  |_  |___|___|  |_____|___|_| |___|  |__,|___|___|___|_|    |_| |_|_|__,|_|    |___|   _____   |___|    |_|  ")
#     print("                 |___|                                                                                |_____|                ")
#     print()
#     print("          ===> Y or N")
#     print()
#     check = input("            >> ")
#     if check.lower() == "n":
#         main()
#     exit()


# def main():
#     title()
#     print("Choose An Option:")
#     print("         (1) start with random board with default size 3x3")
#     print("         (2) Enter your own board, total length must be a square number")
#     print("         (3) To Exit")
#     print("")
#     choice = input(">> ")
#     if choice == 1:
#         startGame()
#     elif choice == 2:
#         takeInputs()
#     else:
#         exitGame()


# def title():
#     print()
#     print()
#     print(" ___    _____             _     ")
#     print("| . |  |  _  |_ _ ___ ___| |___ ")
#     print("| . |  |   __| | |- _|- _| | -_|")
#     print("|___|  |__|  |___|___|___|_|___|")
#     print()
#     print("_________________________________")
#     print("")


# if __name__ == "__main__":
#     main()
# z = puzzleBoard(randomize=True)
# print(z.solution())
# startGame()
