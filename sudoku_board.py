from sudoku_element import Element
from sudoku_square import Square

class Board:
    """ root class of boards """

    def __init__(self, NUMS):
        # Nums parameter is a 2D list, like what the sudoku_reader returns
        self.n_rows = len(NUMS[0])
        self.n_cols = len(NUMS)
        self.NUMS = [[None for _ in range(self.n_rows)] for _ in range(self.n_cols)]

    def __str__(self):
        return "Board with " + str(self.n_rows) + " rows and " + str(self.n_cols) + " columns:\n"


class Sudoku_board(Board):
    ''' Subclass of Board. Implementation of a 9x9 sudoku board '''

    def __init__(self, NUMS):
        super().__init__(NUMS)
        self.NUMS = NUMS
        '''array describing starting setup of the board. this array will not be mutated by the program'''
        self.unsolved_squares = []
        '''contains unsolved squares of the board'''
        self.squares = self._set_up_squares()
        '''array of the squares contained within the board'''
        self.elements = self._set_up_elems(self.squares)
        '''array of elements contained within the board'''
        self.solved = False

    def _set_up_squares(self):
        '''Set up the squares on the board (ints into Square objects)'''
        SQUARES = []
        for row in range(9):
            NEW_ROW = []
            for col in range(9):
                VAL = self.NUMS[row][col]
                NEW_SQUARE = Square(VAL, row, col)
                NEW_ROW.append(NEW_SQUARE)
                if (VAL == 0):
                    self.unsolved_squares.append(NEW_SQUARE)
            SQUARES.append(NEW_ROW)
        return SQUARES

    def _set_up_elems(self, squares):
        '''Set up elements for checking rows, coloumns, boxes'''
        ELEMS = []

        # add rows to elements
        for i in range(9):
            ELEMS.extend([
                Element("row", self.squares[i]),
                Element("col", [row[i] for row in self.squares])])

        # add boxes to elements; not very pretty but it does the job
        # adds 3 and 3 parts of each row, concatinated together, in order to form the boxes
        for i in [0, 3, 6]:
            ELEMS.extend([
                Element("box", squares[i][0:3] + squares[i+1][0:3] + squares[i+2][0:3]),
                Element("box", squares[i][3:6] + squares[i+1][3:6] + squares[i+2][3:6]),
                Element("box", squares[i][6:9] + squares[i+1][6:9] + squares[i+2][6:9])])

        return ELEMS

    # not in use
    def move_was_mistake(self):
        for row in (self.squares):
            for s in (row):
                if not (s.value == 0):
                    s.possible_values = s.get_valid_nums()
                    if (len(s.possible_values) == 0):
                        # not occupied and has no legal values. a mistake has been made
                        return True
        return False

    def one_piece_solve(self):
        '''attempt to solve the sudoku board'''

        # this method looks for a piece that has only one possible valid number, sets it,
        # and then repeats until the whole board is solved.
        # this will only work if there is an unique solution to the sudoku, which there usually is.
        # For context, the first non-unique-solution sudoku in sudoku_1M is sudoku#3610
        # Bit ugly as a consequence of some optimizations attempts

        while (True):
            solving = False
            for row in self.squares:
                for s in row:
                    if (s.value == 0):
                        x = s.unique_valid_num()  # val == 0 if there exists more than one option
                        if (x > 0):
                            s.value = x
                            self.unsolved_squares.remove(s)
                            solving = True
            if not (solving):
                if (len(self.unsolved_squares) == 0):
                    return True
                else:
                    return False

    def _find_empty_index(self):
        '''find index of empty square within self.unsolved_squares'''

        for i in range(len(self.unsolved_squares)):
            if (self.unsolved_squares[i].value == 0):
                return i
        return -1

    def backtrack_solve(self):
        '''solves by trial and error through recursion.
        My implementation here is not optimized by any means
        Does not continuously update the squares within unsolved squares'''

        i = self._find_empty_index()
        if (i == -1):   # no more unsolved squares, sudoku is done
            return True

        for num in range(1, 10):
            options = self.unsolved_squares[i].get_valid_nums()
            if num in options:
                self.unsolved_squares[i].value = num
                if self.backtrack_solve():
                    return True
                self.unsolved_squares[i].value = 0
        return False

    def solve(self):
        self.solved = True
        if (self.one_piece_solve()):
            return 1
        else:
            self.backtrack_solve()
            self.unsolved_squares = []
            return 0

    # used in pygame // testing
    def verify_solution(self):
        '''check if current board solution is valid. Returns a string with info '''

        checks = 0
        for e in (self.elements):
            sum = 0
            has_nums = 0
            for i in range(1, 10):  # wtf python, why not just (int i = 1; i < 10; i++)
                if (e.has_num(0)):
                    self.solved = False
                    return "_Oops! Solution does not solve for all squares!"
                if (e.has_num(i)):
                    has_nums += 1
                    sum += i
            if not (has_nums == 9):
                self.solved = False
                return "_Oops! Solution has element with duplicate number!"
            elif (sum == 45):
                # double verification with sum of [1, 9] == 45
                checks += 1

        if (checks == len(self.elements)):
            self.solved = True
            return "Correct solution!"

    # edited the original to read from "squares" instead of "nums"
    def __str__(self):
        str_r = "Board with " + str(self.n_rows) + " rows and " + str(self.n_cols) + " columns:\n"
        str_r += "\n[["
        for row in self.squares:
            for i in row:
                str_r += str(i.value) + ", "
            str_r = str_r[:-2] + "]" + "\n ["
        str_r = str_r[:-3] + "]"
        return str_r
