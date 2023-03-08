
class Element:
    """subclass of Sudoku_board: group of squares within the sudokuboard\n
    Has a type matching the elements shape (col,row,box)\n
    Each Element contains an array of its squares."""

    def __init__(self, type, squares):
        self.type = type
        self.squares = squares
        self._set_up_square_link()

    def _set_up_square_link(self):
        """ links elements to their related squares upon element creation """
        for square in (self.squares):
            square.elements.append(self)

    def has_num(self, n):
        """ checks whether or not element contains a given number. Return True or False """
        for s in (self.squares):
            if (s.value == n):
                return True
        return False

    def __str__(self):
        str_r = "Element of type '" + str(self.type) + "' with squares: \n"
        for square in range(len(self.squares)):
            str_r += str(self.squares[square]) + "\n"
        return str_r
