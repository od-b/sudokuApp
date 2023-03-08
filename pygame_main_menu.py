import pygame
from pygame_button import Pygame_button
from pygame_menu import Pygame_menu

class Pygame_main_menu(Pygame_menu):
    def __init__(self, cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text):
        super().__init__(cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text)
        self.re = pygame.Rect(int(self.pos_x), int(self.pos_y), int(self.width), int(self.height))
        self._set_up_buttons()

    def _set_up_buttons(self):
        '''
            * dynamically adjusts position, width spacing to fit within menu on creation.
            * Does NOT need to be altered when creating new buttons
        '''

        btns_created = 0
        btn_list = []
        for key in self.cf.buttons['main_menu']:
            new_btn = Pygame_button(
                self.CX,
                int(self.btn_width),
                int(self.height - (2 * self.btn_margin)),                                     # height
                int(self.re.left + 1 + (btns_created) * (self.btn_width + self.btn_margin)),  # pos x (left)
                int(self.pos_y + self.btn_margin),                                            # pos y (top)
                self.cf.buttons['main_menu'][key]['description'],                             # display text
                self.cf.buttons['main_menu'][key]['id'])                                      # internal id
            btn_list.append(new_btn)
            btns_created += 1
        self.buttons = btn_list
