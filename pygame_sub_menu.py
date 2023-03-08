
import pygame
from pygame_button import Pygame_button
from pygame_menu import Pygame_menu

class Pygame_sub_menu(Pygame_menu):
    def __init__(self, cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text):
        super().__init__(cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text)
        self.re = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def set_theme_colors(self, bg_color, border_color, text_color, text_color_big, text_bg_color):
        self.bg_color = bg_color
        self.border_color = border_color
        self.text_color = text_color
        self.text_color_big = text_color_big
        self.text_bg_color = text_bg_color
