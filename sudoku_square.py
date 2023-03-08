
class Square:
    """ A single square within the 9x9 sudoku board.\n
    Takes in row and col position as integers, and an integer value."""

    def __init__(self, value, p_row, p_col):
        self.p_row = p_row  # position on the y-axis, i.e. which row
        self.p_col = p_col  # position on the x-axis, i.e. which col
        self.value = value  # number within the square. 0 == empty square
        self.elements = []  # array of the elements that contain this square
        self.static = False
        self.relation_highlight = False

        if not (self.value == 0):
            self.static = True

    def get_valid_nums(self):
        """returns an array of all possible numbers for the square"""
        NUMS = []
        for x in range(1, 10):
            checks = 0
            for el in (self.elements):
                if not (el.has_num(x)):
                    checks += 1
                    if (checks == 3):
                        NUMS.append(x)
                        checks = 0
        return NUMS

    def unique_valid_num(self):
        """if only one valid number exists for the square, return it, otherwise return 0"""
        found = False
        number = 0
        for x in range(1, 10):
            checks = 0
            for el in (self.elements):
                if not (el.has_num(x)):
                    checks += 1
                    if (checks == 3):
                        if (found):
                            return 0
                        found = True
                        checks = 0
                        number = x
        return number

    def __str__(self):
        return str("square  @  [" + str(self.p_row) + "][" + str(self.p_col) + "]  ==  " + str(self.value))
