import pygame
from pygame_sub_menu import Pygame_sub_menu
from pygame_menu import Pygame_menu

class Pygame_right_menu(Pygame_menu):
    '''
        Wrapper for the right coloumn-style menu
        Contains a list of sub-menus
    '''

    def __init__(self, cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text):
        super().__init__(cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text)
        self.re = pygame.Rect(
            self.pos_x,
            self.pos_y,
            self.width,
            self.height)
        self.text_color = self.cf.theme['RIGHT_MENU_TEXT']
        self.bg_color = self.cf.theme['RIGHT_MENU_BACKGROUND']
        self.border_color = self.cf.theme['RIGHT_MENU_BORDER']
        self.text_bg_color = self.bg_color
        self.sub_menus = self._set_up_sub_menus()

    def update_submenu_colors(self):
        for m in self.sub_menus:
            m.set_theme_colors(
                self.bg_color,
                self.border_color,
                self.text_color,
                self.text_color_big,
                self.text_bg_color)

    def update_theme_colors(self):
        self.text_color = self.cf.theme['RIGHT_MENU_TEXT']
        self.bg_color = self.cf.theme['RIGHT_MENU_BACKGROUND']
        self.border_color = self.cf.theme['RIGHT_MENU_BORDER']
        self.text_color_big = self.cf.theme['MENU_TEXT_BIG']
        self.text_bg_color = self.bg_color
        self.update_submenu_colors()

    def _set_up_sub_menus(self):
        ''' not dynamic by any means '''
        MARGIN = self.cf.misc['menu_btn_margin']
        menus = []
        sub_one = Pygame_sub_menu(
            self.cf,
            self.CX,
            self.re.left,
            self.re.top,
            self.height/4,
            self.width,
            MARGIN,
            0,
            None)
        menus.append(sub_one)
        sub_two = Pygame_sub_menu(
            self.cf,
            self.CX,
            self.re.left,
            sub_one.re.bottom,
            self.height/4,
            self.width,
            MARGIN,
            0,
            None)
        menus.append(sub_two)
        sub_three = Pygame_sub_menu(
            self.cf,
            self.CX,
            self.re.left,
            sub_two.re.bottom,
            self.height/4,
            self.width,
            MARGIN,
            0,
            None)
        menus.append(sub_three)
        sub_four = Pygame_sub_menu(
            self.cf,
            self.CX,
            self.re.left,
            sub_three.re.bottom,
            self.height/4,
            self.width,
            MARGIN,
            0,
            None)
        menus.append(sub_four)
        for m in menus:
            m.set_theme_colors(
                self.bg_color,
                self.border_color,
                self.text_color,
                self.text_color_big,
                self.text_bg_color)
        return menus

    def format_ms_time(self, ms):
        # TODO:
        # move this function somewhere more appropriate
        #
        sec = int(ms/1000) % 60
        min = int(ms/(1000*60)) % 60
        hou = int(ms/(1000*60*60)) % 24
        if hou == 0:
            return f'{min:02d}:{sec:02d}'
        return f'{hou:02d}:{min:02d}:{sec:02d}'

    def update_sub_menus(self, total_time, current_board_time, boards_completed, fastest_solved, difficulty):
        # sub one == total timer
        sub_one_txt = "Total Time: \n _" + str(self.format_ms_time(total_time))
        self.sub_menus[0].set_text(sub_one_txt)

        # sub two == current board timer
        sub_two_txt = "This Board: \n _" + str(self.format_ms_time(current_board_time))
        self.sub_menus[1].set_text(sub_two_txt)

        # sub three == difficulty
        sub_three_txt = "Difficulty: \n "
        if (difficulty == 1):
            sub_three_txt += "_Beginner"
        elif (difficulty == 2):
            sub_three_txt += "_Intermediate"
        elif (difficulty == 3):
            sub_three_txt += "_Expert"
        self.sub_menus[2].set_text(sub_three_txt)

        # sub three == boards solved, fastest time
        sub_four_txt = "Completed Boards: _" + str(boards_completed)
        if fastest_solved:
            sub_four_txt += "Fastest: \n _" + str(self.format_ms_time(fastest_solved))  # noqa
        # else:
        #     sub_four_txt += " \n Fastest: _n/a"  # noqa
        self.sub_menus[3].set_text(sub_four_txt)

    def draw_sub_menus(self):
        for menu in self.sub_menus:
            menu.draw_text(menu.re)
