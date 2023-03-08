
class Pygame_sudoku_square:
    def __init__(self, re, center, txt_color, board_square):
        self.re = re
        self.center = center
        self.txt_color = txt_color
        self.board_square = board_square
        self.elements = board_square.elements
        self.mouse_over = False
        self.static = False
        self.selected = False

    def highlight_related_squares(self):
        for el in (self.elements):
            for sq in el.squares:
                sq.relation_highlight = True
