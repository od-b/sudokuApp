import pygame
from pygame_button import Pygame_button
from pygame_menu import Pygame_menu

class Pygame_popup_info(Pygame_menu):
    ''' popup with only one button '''
    def __init__(self, cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text):
        super().__init__(cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text)
        self.text = text
        self.re = pygame.Rect(
            (self.pos_x - (self.width / 2)),
            (self.pos_y - (self.height / 2)),
            self.width,
            self.height)
        self.option_id = 'generic_info'
        self.border_width = self.cf.misc['popup_menu_border_width']

        self.update_theme_colors()
        self._set_up_buttons()
        self._format_text()

    def update_theme_colors(self):
        self.bg_color = self.cf.theme['POPUP_MENU_BACKGROUND']
        self.border_color = self.cf.theme['POPUP_MENU_BORDER']
        self.text_color = self.cf.theme['POPUP_MENU_TEXT']
        self.text_color_big = self.cf.theme['MENU_TEXT_BIG']
        self.text_bg_color = self.bg_color

    def _set_up_buttons(self):
        height = self.cf.misc['menu_height'] - (2 * self.btn_margin)
        new_btn = Pygame_button(
            self.CX,
            int(self.btn_width/2),
            height,                                                 # height
            int(self.re.center[0] - ((self.btn_width/2)/2)),        # pos x (left)
            int(self.pos_y + height - (2 * self.btn_margin)),       # pos y (top)
            self.cf.buttons['popup_info']['BTN_ok']['description'],    # display text
            self.cf.buttons['popup_info']['BTN_ok']['id'])
        self.buttons.append(new_btn)

    def draw(self):
        self.draw_background(self.re)
        self.draw_text(self.re)
        self.draw_buttons()
