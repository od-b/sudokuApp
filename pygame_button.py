import pygame

class Pygame_button:
    def __init__(self, CX, width, height, pos_x, pos_y, text, btn_id):
        self.CX = CX
        self.width = width
        self.height = height
        self.pos_x = pos_x
        self.pos_y = pos_y
        self.text = text
        self.btn_id = btn_id
        self.mouse_over = False
        self.re = pygame.Rect(self.pos_x, self.pos_y, self.width, self.height)

    def __str__(self):
        return str(f'button with text = {self.text}, id = {self.btn_id}')
