# Author: Odin Bjerke #
# od.bjerke@gmail.com #

from sudoku_reader import Sudoku_reader
from sudoku_board import Sudoku_board
import time

def solve():
    # just solve sudokus with the algorithm, no pygame window launched
    START = time.time()
    BOARDS_TO_SOLVE = 10000  # select boards to solve
    one_piece_solved = 0
    backtrack_solved = 0
    READER = Sudoku_reader("./data/sudoku_boards/sudoku_easy_1M.csv")

    for _ in range(BOARDS_TO_SOLVE):
        BOARD = Sudoku_board(READER.get_next_board())
        if (BOARD.solve()) == 1:
            one_piece_solved += 1
        else:
            backtrack_solved += 1

        # uncomment if you want to triple check the solutions
        # if not (str(BOARD.verify_solution()) == 'Correct solution!'):
        #     print(BOARD.verify_solution)

    END = time.time()
    print("boards solved: " + str(BOARDS_TO_SOLVE) + ", time spent: " + str(round((END - START), 4)))
    print("Backtrack solved: " + str(backtrack_solved) + ", one piece solved: " + str(one_piece_solved))


if __name__ == "__main__":
    # main()
    solve()

# boards solved: 100000, time spent: 62.1865
# Backtrack solved: 41, one piece solved: 99959
