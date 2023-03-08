# Author: Odin Bjerke #
# od.bjerke@gmail.com #

import pygame
from sudoku_reader import Sudoku_reader
from sudoku_board import Sudoku_board
from pygame_window import Pygame_window
from pygame_sudoku_board import Pygame_sudoku_board
from pygame_main_menu import Pygame_main_menu
from pygame_right_menu import Pygame_right_menu
from pygame_popup_info import Pygame_popup_info
from pygame_popup_options import Pygame_popup_options
from settings import settings as _settings_


''' TODO:
* Finish refactoring in timers.py to wrap in timer variables
* Hint function for uncovering just one correct square
'''


class Pygame_sudoku_wrapper:
    '''
        Single use class, which might be bad practice.
        wrapper for initializing objects, gameloop, changing boards, changing settings, etc.
        Takes in a settings object and applies the settings to the relevant elements.
    '''

    def __init__(self, SETTINGS):
        # init settings / config / cf
        self.cf = SETTINGS

        # pygame clock module
        self.clock = pygame.time.Clock()

        # file reader
        self.difficulty = self.cf.misc['reader_default_difficulty']
        self.READER = Sudoku_reader(self.cf.misc['reader_path'][self.difficulty])

        window_height = int(
            self.cf.misc['board_size']\
            + self.cf.misc['board_margin_top']\
            + self.cf.misc['board_margin_bottom']\
            + self.cf.misc['menu_height']
        )

        window_width = int(
            self.cf.misc['board_size']\
            + self.cf.misc['board_margin_right']\
            + self.cf.misc['board_margin_left']
        )

        if (self.cf.misc['show_right_menu']):
            window_width += int(self.cf.misc['right_menu_width'])

        # surface window
        self.CX = Pygame_window(
            self.cf,
            self.cf.misc['caption'],
            window_width,
            window_height
        )

        main_menu_width = self.cf.misc['board_size'] + 2
        # board is actually 2 pixels wider than 'board_size' due to its borders
        if (self.cf.misc['show_right_menu']):
            main_menu_width += int(self.cf.misc['right_menu_width']) + 2
            # account for right menu and its border too

        # main menu wrapper
        self.MENU = Pygame_main_menu(
            self.cf,
            self.CX,
            (self.cf.misc['board_margin_left']),                      # pos x
            (self.cf.misc['board_size'] + self.cf.misc['board_margin_top']),  # pos y
            self.cf.misc['menu_height'],                       # height
            main_menu_width,
            self.cf.misc['menu_btn_margin'],
            len(self.cf.buttons['main_menu']),
            None
        )

        right_menu_width = int(
            self.CX.WIDTH - (
                self.cf.misc['board_margin_left']\
                + self.cf.misc['board_margin_right']\
                + self.cf.misc['board_size']\
                + int(2 * self.cf.misc['menu_border_width'])\
            )
        )
        # right menu wrapper
        self.MENU_RIGHT = Pygame_right_menu(
            self.cf,
            self.CX,
            (self.cf.misc['board_margin_left']\
                + self.cf.misc['board_size']\
                + self.cf.misc['menu_btn_margin']),  # pos_x
            self.cf.misc['board_margin_top'],        # pos_y
            self.cf.misc['board_size'],              # height
            right_menu_width,
            self.cf.misc['menu_btn_margin'],
            0,
            None
        )

        # misc
        self.running = True
        self.first_run = True
        self.popup_window = []  # list with max one element, to avoid member of 'None' errors
        self.popup_active = False
        #   note: square selection is here as opposed to under board to allow smooth board swapping
        self.selected_x = 0
        self.selected_y = 0
        self.outline_selected = True

        # board variables // init first board
        self.board_num = 0
        self.boards_completed = 0
        self.pg_board = self._get_new_board(True)

        # time variables
        self.total_time = 0
        self.current_board_time = None
        self.current_board_start = 0
        self.time_segments = []
        self.fastest_time = None

        self.debug_draw_containers = self.cf.misc['debug_draw_containers']

    def _get_new_board(self, next):
        '''
        *   next=false will return a random board, next=true returns next board in csv.
        *    Also updates window caption
        '''

        self.board_num += 1
        if (next):
            new_board_arr = Sudoku_board(self.READER.get_next_board())
        else:
            new_board_arr = Sudoku_board(self.READER.get_random_board())

        self.CX.update_caption(str("Board # " + str(self.board_num)))
        new_pg_board = Pygame_sudoku_board(
            self.cf,
            new_board_arr,
            self.CX,
            self.MENU,
            self.cf.misc['board_margin_left'],   # pos x
            self.cf.misc['board_margin_top'],   # pos y
            self.cf.misc['board_size'])

        # retain current square selection through board swap
        new_pg_board.selected_square = new_pg_board.PG_SQUARES[self.selected_x][self.selected_y]
        new_pg_board.selected_square.selected = True
        return new_pg_board

    def _toggle_relation_highlighting(self):
        self.pg_board.clear_highlighted_squares()
        if (self.cf.misc['highlight_related_squares']):
            self.cf.misc['highlight_related_squares'] = False
            return False
        else:
            self.cf.misc['highlight_related_squares'] = True
            return True

    def _create_popup_info(self, text):
        ''' for popup window with no options, simply an "ok" or similar to close the window '''

        self.popup_active = True
        return Pygame_popup_info(
            self.cf,
            self.CX,
            int(self.CX.WIDTH / 2),
            self.pg_board.re.center[1],
            self.cf.misc['popup_window_height'],
            self.cf.misc['popup_window_width'],
            self.cf.misc['menu_btn_margin'],
            1,
            text)

    def _create_popup_options(self, text, option_id):
        ''' for popup window with clickable yes/no options '''

        self.popup_active = True
        NUM_OPTIONS = 2
        return Pygame_popup_options(
            self.cf,
            self.CX,
            int(self.CX.WIDTH / 2),
            self.pg_board.re.center[1],
            self.cf.misc['popup_window_height'],
            self.cf.misc['popup_window_width'],
            self.cf.misc['menu_btn_margin'],
            NUM_OPTIONS,
            text,
            option_id)

    def _adjust_difficulty(self):
        ''' increase (or reset) the difficulty setting '''

        self.READER.close_file()
        self.difficulty = int(self.difficulty)
        if self.difficulty == int(len(self.cf.misc['reader_path'])):
            self.difficulty = 1
        else:
            self.difficulty += 1
        self.READER = Sudoku_reader(self.cf.misc['reader_path'][str(self.difficulty)])

    def _get_active_popup(self):
        return self.popup_window[0]

    def _new_segment(self, save_segment):
        # if (save_segment) and not (self.pg_board.assisted_solve):
        # ^ avoid cheating segments with 'solve'
        if (save_segment):
            self.time_segments.append(self.current_board_time)
            self.fastest_time = min(self.time_segments)
        self.current_board_time = 0
        self.current_board_start = self.total_time

    def _change_theme(self):
        self.cf.cycle_theme()
        self.MENU.update_theme_colors()
        self.MENU_RIGHT.update_theme_colors()

    def _btn_function_redirect(self, btn_id):
        ''' redirect button functionality by btn_id '''

        if self.popup_active:
            if self._get_active_popup().option_id == 'generic_info':
                if (btn_id == "BTN_ok"):
                    self.popup_window = []
                    self.popup_active = False
            elif (self._get_active_popup().option_id == "BTN_reset"):
                if (btn_id == "BTN_yes"):
                    self.popup_window = []
                    self.popup_active = False
                    self.pg_board.reset()
                if (btn_id == "BTN_no"):
                    self.popup_window = []
                    self.popup_active = False
        else:
            match btn_id:
                case "BTN_change_theme":
                    if len(self.cf.theme_list) > 0:
                        self._change_theme()
                    else:
                        print("Oops! only one theme is available")
                case "BTN_toggle_highlighting":
                    if (self._toggle_relation_highlighting()):
                        info_txt = "Highlighting of squares related to current turned _ON"
                    else:
                        info_txt = "Highlighting of squares related to current turned _OFF"
                    self.popup_window = [self._create_popup_info(info_txt)]
                case "BTN_reset":
                    option_txt = "Are you sure you want to reset the board to its original state?"
                    self.popup_window = [self._create_popup_options(option_txt, btn_id)]
                    self._new_segment(False)
                case "BTN_check":
                    result_txt = str(self.pg_board.BOARD.verify_solution())
                    self.popup_window = [self._create_popup_info(result_txt)]
                case "BTN_solve":
                    if not (self.pg_board.BOARD.solved):
                        self.pg_board.reset()
                        print('Solving . . .')
                        meth = self.pg_board.BOARD.solve()
                        if meth == 1:
                            print('Solved using one piece method')
                        else:
                            print('Solved using backtracking')
                        self.pg_board.assisted_solve = True
                    else:
                        info_txt = "Board is already solved. Reset or click _New for a new board."
                        self.popup_window = [self._create_popup_info(info_txt)]
                case "BTN_new_board":
                    if (self.pg_board.BOARD.solved):
                        self._new_segment(True)
                        if not (self.pg_board.assisted_solve):
                            self.boards_completed += 1
                    else:
                        self._new_segment(False)
                    self.pg_board = self._get_new_board(False)
                case "BTN_change_difficulty":
                    self._adjust_difficulty()
                    self._new_segment(False)
                    self.pg_board = self._get_new_board(False)
                    info_txt = "Difficulty changed to \n "
                    if (self.difficulty == 1):
                        info_txt += "_Beginner"
                    elif (self.difficulty == 2):
                        info_txt += "_Intermediate"
                    elif (self.difficulty == 3):
                        info_txt += "_Expert"
                    self.popup_window = [self._create_popup_info(info_txt)]
                case _:
                    print(f'_btn_function_redirect\n\t --> unknown redirect -> btn = "{btn_id}"')

    def _event_keydown(self, key):
        ''' check if key matches any target event keys '''
        match key:
            case pygame.K_UP:
                if (self.cf.misc['controls'] == 'mouse') and (self.selected_y-1 in range(0, 9)):
                    self.selected_y -= 1
                    self.pg_board.update_selected_square(self.selected_x, self.selected_y)
            case pygame.K_DOWN:
                if (self.cf.misc['controls'] == 'mouse') and (self.selected_y+1 in range(0, 9)):
                    self.selected_y += 1
                    self.pg_board.update_selected_square(self.selected_x, self.selected_y)
            case pygame.K_LEFT:
                if (self.cf.misc['controls'] == 'mouse') and (self.selected_x-1 in range(0, 9)):
                    self.selected_x -= 1
                    self.pg_board.update_selected_square(self.selected_x, self.selected_y)
            case pygame.K_RIGHT:
                if (self.cf.misc['controls'] == 'mouse') and (self.selected_x+1 in range(0, 9)):
                    self.selected_x += 1
                    self.pg_board.update_selected_square(self.selected_x, self.selected_y)

            # number keys
            case pygame.K_0:
                self.pg_board.update_selected_square_value(0)
            case pygame.K_1:
                self.pg_board.update_selected_square_value(1)
            case pygame.K_2:
                self.pg_board.update_selected_square_value(2)
            case pygame.K_3:
                self.pg_board.update_selected_square_value(3)
            case pygame.K_4:
                self.pg_board.update_selected_square_value(4)
            case pygame.K_5:
                self.pg_board.update_selected_square_value(5)
            case pygame.K_6:
                self.pg_board.update_selected_square_value(6)
            case pygame.K_7:
                self.pg_board.update_selected_square_value(7)
            case pygame.K_8:
                self.pg_board.update_selected_square_value(8)
            case pygame.K_9:
                self.pg_board.update_selected_square_value(9)

            # misc keys
            case pygame.K_BACKSPACE:
                # does the same as K_0, reset square if not static
                self.pg_board.update_selected_square_value(0)
            case pygame.K_SPACE:                            # solve board
                if not (self.pg_board.BOARD.solved):
                    self.pg_board.reset()
                    self.pg_board.BOARD.solve()
            case pygame.K_r:                                # reset board
                self.pg_board.reset()
            case pygame.K_c:                                # verify solution
                self.pg_board.BOARD.verify_solution()
            case pygame.K_n:                                # load the next board
                self.pg_board = self._get_new_board(True)
            case pygame.K_f:                                # load a new random board
                self.pg_board = self._get_new_board(False)

    def loop(self):  # noqa
        ''' main loop for drawing, checking events and updating the game '''
        while (self.running):
            # get and store mouse position
            MOUSE_POS = pygame.mouse.get_pos()
            self.clock.tick(240)    # limit fps

            # update timers
            self.total_time = pygame.time.get_ticks()

            if self.first_run:
                # first board timer init
                self.current_board_time = self.total_time
                self.first_run = False
            else:
                # increment current time
                # print(f'board start: {self.current_board_start}')
                self.current_board_time = self.total_time - self.current_board_start
                # print(f'current board time: {self.current_board_time}')

            # update selected square based on mouse position
            if (self.popup_active):
                self.pg_board.selected_square.selected = False
            elif (self.cf.misc['controls'] == 'mouse'):
                self.outline_selected = False
                # do not apply visual hovering effect if popup is active
                for row in self.pg_board.PG_SQUARES:
                    for sq in row:
                        if sq.re.collidepoint(MOUSE_POS):
                            sq.selected = True
                            self.pg_board.selected_square = sq
                            self.outline_selected = True
                        else:
                            sq.selected = False
                if not (self.outline_selected):
                    # mouse is off screen, ignore selected
                    self.pg_board.selected_square.selected = False

            '''
            *   if hovering over a button, change cursor to hand style
            *   note: _btn_mouseover(MOUSE_POS) returns True if collision is found
            *   ignore main menu if popup is active
            '''
            if (self.popup_active):
                # if a popup is active, check button mouseover status
                if (self._get_active_popup()._btn_mouseover(MOUSE_POS)):
                    pygame.mouse.set_cursor(self.CX.HAND_CURSOR)
                    self.CX.hand_cursor_is_active = True
                elif (self.CX.hand_cursor_is_active):
                    pygame.mouse.set_cursor(self.CX.NORMAL_CURSOR)
                    self.CX.hand_cursor_is_active = False
            else:
                # else, check for main menu buttons
                if (self.MENU._btn_mouseover(MOUSE_POS)):
                    pygame.mouse.set_cursor(self.CX.HAND_CURSOR)
                    self.CX.hand_cursor_is_active = True
                elif (self.CX.hand_cursor_is_active):
                    pygame.mouse.set_cursor(self.CX.NORMAL_CURSOR)
                    self.CX.hand_cursor_is_active = False

            # fill, draw and update the display
            self.CX.display.fill(self.cf.theme['WINDOW_BACKGROUND'])
            self.pg_board.draw()

            if (self.cf.misc['show_right_menu']):
                self.MENU_RIGHT.draw_background(self.MENU_RIGHT.re)
                self.MENU_RIGHT.update_sub_menus(
                    self.total_time,
                    self.current_board_time,
                    self.boards_completed,
                    self.fastest_time,
                    self.difficulty)
                self.MENU_RIGHT.draw_sub_menus()

            # if the highlight option is active, apply to the drawing process
            # if a popup is active, only clear highlighted squares
            if (self.cf.misc['highlight_related_squares']):
                self.pg_board.clear_highlighted_squares()
                if (self.outline_selected) and not (self.popup_active):
                    self.pg_board.selected_square.highlight_related_squares()

            self.pg_board.draw_box_grid_lines()

            if (self.debug_draw_containers):
                self.CX.debug_draw(self.MENU.re)

            self.MENU.draw_buttons()

            if (self.popup_active):
                self._get_active_popup().draw()

            pygame.display.update()

            # handle queued events
            for event in pygame.event.get():
                if event.type == pygame.QUIT:   # exit the app
                    self.running = False

                # keyboard events
                if (event.type == pygame.KEYDOWN) and not (self.popup_active):
                    # arrow keys, for changing selected square if settings are set to keyboard
                    # ignore keydown events if popup is active
                    self._event_keydown(event.key)

                # if there is a mouse click => (check if mouse is over a button = if yes => redirect)
                if event.type == pygame.MOUSEBUTTONUP:
                    if (self.popup_active):
                        for btn in self.popup_window[0].buttons:
                            if btn.re.collidepoint(MOUSE_POS):
                                self._btn_function_redirect(btn.btn_id)
                    else:
                        for btn in self.MENU.buttons:
                            if btn.re.collidepoint(MOUSE_POS):
                                self._btn_function_redirect(btn.btn_id)


def init_game():
    pygame.init()
    GAME = Pygame_sudoku_wrapper(_settings_)
    GAME.loop()


if __name__ == "__main__":
    init_game()
