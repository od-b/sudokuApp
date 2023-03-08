import pygame
from pygame_button import Pygame_button
from pygame_menu import Pygame_menu

class Pygame_popup_options(Pygame_menu):
    ''' popup window with > 1 button '''
    def __init__(self, cf, SURFACE, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text, option_id):
        super().__init__(cf, SURFACE, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text)
        self.text = text
        self.re = pygame.Rect(
            (self.pos_x - (self.width / 2)),
            (self.pos_y - (self.height / 2)),
            self.width,
            self.height)
        self.option_id = option_id
        self.border_width = self.cf.misc['popup_menu_border_width']

        self.update_theme_colors()
        self._set_up_buttons()
        self._format_text()

    def update_theme_colors(self):
        self.border_color = self.cf.theme['POPUP_MENU_BORDER']
        self.text_color = self.cf.theme['POPUP_MENU_TEXT']
        self.bg_color = self.cf.theme['POPUP_MENU_BACKGROUND']
        self.text_bg_color = self.bg_color

    def _set_up_buttons(self):
        HEIGHT = self.cf.misc['menu_height'] - (2 * self.btn_margin)
        btns_created = 0
        btn_list = []
        for key in self.cf.buttons['popup_options']:
            new_btn = Pygame_button(
                self.CX,
                self.btn_width,
                int(HEIGHT),                                    # height
                int(2 + self.re.left + (2 * self.btn_margin) + ((btns_created) * (self.btn_width + self.btn_margin))),  # pos x (left)
                int(self.re.bottom - HEIGHT - (2 * self.btn_margin)),                                                   # pos y (top)
                self.cf.buttons['popup_options'][key]['description'],                                                       # display text
                self.cf.buttons['popup_options'][key]['id'])                                                                # internal id
            btn_list.append(new_btn)
            btns_created += 1
        self.buttons = btn_list

    def draw(self):
        self.draw_background(self.re)
        self.draw_text(self.re)
        self.draw_buttons()
