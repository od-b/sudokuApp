
class Board:
    """ root class of board """

    def __init__(self, NUMS):
        # Nums parameter is a 2D list, like what the sudoku_reader returns
        self.n_rows = len(NUMS[0])
        self.n_cols = len(NUMS)
        self.NUMS = [[None for _ in range(self.n_rows)] for _ in range(self.n_cols)]

    def __str__(self):
        return "Board with " + str(self.n_rows) + " rows and " + str(self.n_cols) + " columns:\n"
