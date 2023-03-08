import pygame

class Pygame_window:
    def __init__(self, cf, caption, WIDTH, HEIGHT):
        pygame.init()
        self.cf = cf
        self.caption = caption
        self.WIDTH = WIDTH
        self.HEIGHT = HEIGHT
        self.display = pygame.display.set_mode((self.WIDTH, self.HEIGHT))
        self.NORMAL_CURSOR = pygame.SYSTEM_CURSOR_ARROW
        self.HAND_CURSOR = pygame.SYSTEM_CURSOR_HAND
        self.hand_cursor_is_active = False

        self.FONTS = {
            'SQUARE_NUM': pygame.font.Font(
                self.cf.fonts['SQUARE_NUM']['style'],
                self.cf.fonts['SQUARE_NUM']['size']),
            'MENU_TXT': pygame.font.Font(
                self.cf.fonts['MENU_TXT']['style'],
                self.cf.fonts['MENU_TXT']['size']),
            'MENU_TXT_BIG': pygame.font.Font(
                self.cf.fonts['MENU_TXT_BIG']['style'],
                self.cf.fonts['MENU_TXT_BIG']['size']),
            'MENU_TXT_HOVER': pygame.font.Font(
                self.cf.fonts['MENU_TXT_HOVER']['style'],
                self.cf.fonts['MENU_TXT_HOVER']['size'])
        }

    def update_caption(self, text):
        pygame.display.set_caption(str(self.caption + text))

    def debug_draw(self, re):
        ''' draw a special color background for the given rect '''
        pygame.draw.rect(self.display, self.cf.theme['DEBUG'], re)

    def __str__(self):
        return str(f'[Pygame_window]:\n\tHeight = {self.HEIGHT}px\n\tWidth = {self.WIDTH}px')
