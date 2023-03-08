import random

class Sudoku_reader:
    """
    The class will allow you to read sudoku boards from
    on the format given in the csv-files.
    """

    def __init__(self, filename):
        self.filename = filename
        self.check_file()
        self.file_lines = self._init_get_file_numlines()
        self.file = open(self.filename, "r")
        self.current_line = 1
        print(f'\nSuccesfully loaded {self}')

    def check_file(self):
        '''verifies that the file exists'''
        try:
            tmp_file = open(self.filename, "r")
            tmp_file.close()
        except IOError:
            print("Sudoku_reader: error opening file. Aborting")
            quit(-1)

    def _init_get_file_numlines(self):
        '''opens a copy of the active file, reads number of lines, then closes it'''
        tmp_file = open(self.filename, "r")
        try:
            file_lines = len(tmp_file.readlines())
            tmp_file.close()
            if (file_lines < 1):
                print("Sudoku_reader: error -> file has no content. Aborting")
                quit(-1)
            return file_lines
        except IOError:
            print("Sudoku_reader: error opening file. Aborting")
            quit(-1)

    def reset_reader(self):
        '''reset the reader to line 1 of the active file. (Note: Closes and reopens the file.)'''
        if not (self.current_line == 1):
            self.file.close()
            self.file = open(self.filename, "r")
            self.current_line = 1

    def close_file(self):
        '''used externally if the reader is to be dumped'''
        self.file.close()

    def get_random_board(self):
        self.reset_reader()
        if (self.file_lines == 1):
            print("can't get random board: only one board in file. Aborting")
            quit(-1)

        board_txt = self.file.readline()
        TARGET = random.randint(2, self.file_lines)

        while (self.current_line < TARGET):
            board_txt = self.file.readline()
            self.current_line += 1

        BOARD = [[0 for _ in range(9)] for _ in range(9)]
        sym_num = 0     # letter within the read line (?)
        for i in range(9):
            for j in range(9):
                BOARD[i][j] = int(board_txt[sym_num])
                sym_num += 1
        return BOARD

    def get_next_board(self):
        """The method next_board() returns a 9*9 2D list of integers."""
        if (self.current_line == self.file_lines):
            self.reset_reader()

        line = self.file.readline()
        line = line.rstrip('\n')
        line = line.rstrip(',')

        BOARD = [[0 for _ in range(9)] for _ in range(9)]
        sym_num = 0
        for i in range(9):
            for j in range(9):
                BOARD[i][j] = int(line[sym_num])
                sym_num += 1

        return BOARD

    def __str__(self):
        return str(f'Sudoku_reader:\n\tFile:\t"{self.filename}"\n\tTotal sudokus in file:\t{self.file_lines}')
