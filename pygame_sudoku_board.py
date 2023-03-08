import pygame
from pygame_sudoku_square import Pygame_sudoku_square

class Pygame_sudoku_board:
    '''aka pg_board'''
    def __init__(self, cf, BOARD, SURFACE, MENU, pos_x, pos_y, size):
        if not (int(size) % 9 == 0):
            print(f'{int(size)} % 9 == {int(size) % 9}')
            print("Pygame_sudoku_board requires board size divisable by 9. Aborting")
            quit(-2)

        self.cf = cf
        self.BOARD = BOARD
        self.CX = SURFACE
        self.MENU = MENU
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.size = int(size)   # board length & width
        self.block_size = int(size / 9)    # block size

        self.re = pygame.Rect(self.pos_x, self.pos_y, self.size, self.size)
        self.PG_SQUARES = self._set_up_squares()
        self.selected_square = self.PG_SQUARES[0][0]  # dummy value
        self.assisted_solve = False

    def _set_up_squares(self):
        '''set up pygame board squares. the squares contain a link to the relevant sudoku_square,
            and do not hold their value themself. The purpose is mainly to not have to create pygame rects for
            every loop, as that makes the app a lot slower.'''
        pg_squares = []
        row = 0
        for x in range(self.pos_x, self.size, self.block_size):
            pg_squares_row = []
            col = 0
            for y in range(self.pos_y, self.size, self.block_size):
                # create a rect to assign the square
                rect = pygame.Rect(int(x), int(y), int(self.block_size), int(self.block_size))

                # value of of the corresponding square within the board array
                board_square = self.BOARD.squares[row][col]

                # pygame rects have a .center property, alternatively;
                # square_center = (x+(self.block_size/2), y+(self.block_size/2))
                square_center = rect.center

                # determine if square value is static (preset) or not, and adjust the text accordingly
                if (board_square.static):
                    txt_color = self.cf.theme['SQUARE_TEXT_HARD']
                else:
                    txt_color = self.cf.theme['SQUARE_TEXT_MEDI']

                # create the pygame square and push to pygame board
                new_pg_square = Pygame_sudoku_square(rect, square_center, txt_color, board_square)
                pg_squares_row.append(new_pg_square)
                col += 1
            pg_squares.append(pg_squares_row)
            row += 1
        return pg_squares

    def update_selected_square(self, x, y):
        # uncheck last board piece selection
        self.selected_square.selected = False
        # update selected square in pg_board
        self.selected_square = self.PG_SQUARES[x][y]
        self.PG_SQUARES[x][y].selected = True

    def update_selected_square_value(self, n):
        if not (self.selected_square.board_square.static):
            self.selected_square.board_square.value = n

    def reset(self):
        ''' resets the board square array. Sets self.solved = False '''
        self.BOARD.unsolved_squares = []
        self.BOARD.solved = False
        for row in self.BOARD.squares:
            for square in row:
                if not square.static:
                    square.value = 0
                    self.BOARD.unsolved_squares.append(square)

    def clear_highlighted_squares(self):
        for row in self.PG_SQUARES:
            for sq in row:
                sq.board_square.relation_highlight = False

    def draw(self):
        '''draw the board and numbers'''
        # draw the board background
        # pygame.draw.rect(self.CX.display, self.cf.theme['BOARD_BACKGROUND'], self.re)

        for row in range(9):
            for col in range(9):
                PS = self.PG_SQUARES[row][col]  # Pygame Square

                # selection // highlighting
                if (PS.selected):
                    bg_color = self.cf.theme['SELECTED_SQUARE_BACKGROUND']
                    border_color = self.cf.theme['SELECTED_SQUARE_BORDER']
                elif (PS.board_square.relation_highlight):
                    bg_color = self.cf.theme['SELECTED_SQUARE_RELATION_BACKGROUND']
                    border_color = self.cf.theme['SELECTED_SQUARE_RELATION_BORDER']
                else:
                    bg_color = self.cf.theme['SQUARE_BACKGROUND']
                    border_color = self.cf.theme['SQUARE_BORDER']

                # debug setting
                if self.cf.misc['debug_draw_containers']:
                    txt_bgcolor = self.cf.theme['DEBUG']
                else:
                    txt_bgcolor = bg_color

                # draw the squares borders and background
                pygame.draw.rect(self.CX.display, bg_color, PS.re)
                pygame.draw.rect(self.CX.display, border_color, PS.re, 1)

                # if square has a number, render and draw the text
                if not (PS.board_square.value == 0):
                    text = self.CX.FONTS['SQUARE_NUM'].render(
                        str(PS.board_square.value),
                        True,   # antialiasing
                        PS.txt_color,
                        txt_bgcolor
                    )
                    text_rect = text.get_rect()
                    text_rect.center = PS.center  # translate the rect to the center of the square
                    # blit square num onto its square
                    self.CX.display.blit(text, text_rect)

    def draw_box_grid_lines(self):
        '''draw 4 horizontal & vertical lines, visualizing the nine 3x3 boxes'''
        SPACING = int(self.block_size * 3)   # 9 boxes total -> spacing = blocksize * 3
        LINE_W = self.cf.misc['box_grid_linewidth']

        for i in range(SPACING, self.size, SPACING):
            # without adjustment similar to LINE_W, the lines are visibly slightly longer than the edge of the board
            X = int(i + self.pos_x - LINE_W)+1
            Y = int(i + self.pos_y - LINE_W)+1
            # draw vertical line
            pygame.draw.line(
                self.CX.display, self.cf.theme['BOX_GRID'],
                (X, (self.pos_y + 1)),
                (X, (self.size + self.pos_x - LINE_W)),
                LINE_W)
            # draw horizontal line
            pygame.draw.line(
                self.CX.display, self.cf.theme['BOX_GRID'],
                ((self.pos_x + 1), Y),
                ((self.size + self.pos_x - LINE_W), Y),
                LINE_W)

        # draw the board outlier border
        pygame.draw.rect(
            self.CX.display,
            self.cf.theme['BOARD_BORDER'],
            self.re,
            int(self.cf.misc['box_grid_linewidth']))
