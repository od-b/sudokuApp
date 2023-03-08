import pygame

class Pygame_menu:
    ''' root class of pygame menu system '''

    def __init__(self, cf, CX, pos_x, pos_y, height, width, btn_margin, n_total_buttons, text):
        self.cf = cf
        self.n_total_buttons: int = n_total_buttons
        self.CX = CX
        self.pos_x = int(pos_x)
        self.pos_y = int(pos_y)
        self.height = int(height)
        self.width = int(width)
        self.btn_margin = int(btn_margin)
        self.btn_width = int(self._calc_btn_width())
        self.text = text
        self.buttons = []

        # set default settings, typically overwritten in subclasses
        self.border_width = int(self.cf.misc['menu_border_width'])
        self.TEXT_LINE_SPACE = int(self.cf.misc['menu_text_line_space'])        # space between lines
        self.TEXT_WORD_SPACE = int(self.cf.misc['menu_text_word_space'])        # space between words
        self.TEXT_MARGIN_TOP = int(self.cf.misc['menu_text_margin_top'])        # margin to the top of the parent roct
        self.TEXT_MARGIN_LEFT = int(self.cf.misc['menu_text_margin_left'])      # margin to the left of the parent rect

        # colors
        self.bg_color = self.cf.theme['MENU_BACKGROUND']
        self.border_color = self.cf.theme['MENU_BORDER']
        self.text_color = self.cf.theme['MENU_TEXT']
        self.text_color_big = self.cf.theme['MENU_TEXT_BIG']
        self.text_bg_color = self.bg_color

    def update_theme_colors(self):
        self.bg_color = self.cf.theme['MENU_BACKGROUND']
        self.border_color = self.cf.theme['MENU_BORDER']
        self.text_color = self.cf.theme['MENU_TEXT']
        self.text_color_big = self.cf.theme['MENU_TEXT_BIG']
        self.text_bg_color = self.bg_color

    def _calc_btn_width(self):
        ''' dynamically calculate appropriate button width '''
        if (self.n_total_buttons > 2):
            # if many buttons
            total_padding = (self.n_total_buttons - 2) * self.btn_margin
            total_width = (self.width - total_padding) - int(total_padding / (self.n_total_buttons - 2))
            return int(total_width / self.n_total_buttons)
        elif (self.n_total_buttons == 2):
            # if exactly two buttons -- yes/no popup, for example
            total_padding = (self.n_total_buttons) * self.btn_margin
            total_width = (self.width - total_padding) - total_padding
            return int((total_width - (2 * self.btn_margin)) / self.n_total_buttons)
        # else, only one button -- 'ok' popup
        return int(self.width - (2 * self.btn_margin))

    def _btn_mouseover(self, mouse_pos):
        '''
            * Requires mouse position within the pygame frame as a tuple (x, y)
            * Check if mouse is over a button, if it is, set 'btn.mouse_over = True.
            * Returns True/False depending on whether mouse is over a button
        '''
        # ensure all buttons are checked before returning
        is_hovering = False

        for btn in self.buttons:
            if btn.re.collidepoint(mouse_pos):
                btn.mouse_over = True
                is_hovering = True
            else:
                btn.mouse_over = False
        return is_hovering

    def _format_text(self):
        ''' changes the text string into a list of words '''
        if (self.text):
            self.text = str(self.text).split()

    def set_text(self, new_text):
        self.text = str(new_text)
        self._format_text()

    def draw_text(self, re):
        '''
            Dynamic positioning of text within the given rect. (top --> bottom; left --> right)
            Pygame does not inheritly have newlines within text boxes, so a workaround is needed.
        '''

        ''' * Documentation:
            Once the font is created, its size cannot be changed.
            A Font object is used to create a Surface object from a string.
            Pygame does not provide a direct way to write text onto a Surface object.
            The method render() must be used to create a Surface object from the text,
            which then can be blit to the screen. The method render() can only render single lines.
            A newline character is not rendered.

            Initializing the font can take a few seconds.
            On a MacBook Air the the creation of a system Font object:

                t0 = time.time()
                font = pygame.font.SysFont(None, 48)
                print('time needed for Font creation :', time.time()-t0)

            took more then 8 seconds:
                => 'time needed for Font creation : 8.230187892913818'

            src: https://pygame.readthedocs.io/en/latest/4_text/text.html
        '''

        if not self.text:
            # there is no text to draw, return without action
            return

        RE_BORDER_WIDTH = int(2 * self.border_width)           # ensure text is not overlapping border of parent rect
        MAX_WIDTH = int(re.width + (2 * self.TEXT_MARGIN_TOP) + RE_BORDER_WIDTH)   # max width of any word rect to be placed

        last_word_rect = None
        current_line_width = int((2 * self.TEXT_MARGIN_TOP) + RE_BORDER_WIDTH)
        num_lines = 0

        for word in self.text:
            # method to highlight words with '_'
            if '_' in str(word):
                STYLE = self.CX.FONTS['MENU_TXT_BIG']
                COLOR = self.text_color_big
                WORD = word.replace('_', '')
            else:
                STYLE = self.CX.FONTS['MENU_TXT']
                COLOR = self.text_color
                WORD = word.replace('_', '')

            if self.cf.misc['debug_draw_containers']:
                txt_bgcolor = self.cf.theme['DEBUG']
            else:
                txt_bgcolor = self.bg_color

            # https://www.pygame.org/docs/ref/font.html#pygame.font.Font.render
            _TXT = STYLE.render(
                str(WORD),        # string to display
                True,             # whether or not to apply antialiasing (should prob disable if pixelfont)
                COLOR,            # text color
                txt_bgcolor       # background color of the rect
            )
            _RECT = _TXT.get_rect()

            # if there is a word already, base position of the new words' rect in relation to it
            # newline is not rendered, but fills the line width when read.
            if (_RECT.width > MAX_WIDTH):
                # word is too long to be displayed properly within the parent rect
                print(f'word {str(word)} is above the max width of its parent rect. Max = {MAX_WIDTH}')
                quit(-2)
                # TODO:
                # implement word split with '-' and newline
            elif not (last_word_rect):
                # set first word position
                _RECT.topleft = (
                    int(re.left + self.TEXT_MARGIN_TOP),              # x
                    int(re.topleft[1] + self.TEXT_MARGIN_LEFT)   # y
                )
                num_lines += 1
            elif ((_RECT.width + current_line_width) > re.width):
                # line is full, draw new line
                # reset line width
                current_line_width = (2 * self.TEXT_MARGIN_TOP) + RE_BORDER_WIDTH
                _RECT.topleft = (
                    int(re.left + self.TEXT_MARGIN_TOP),                                                         # x
                    int(re.topleft[1] + self.TEXT_MARGIN_LEFT + (num_lines * (_RECT.height + self.TEXT_LINE_SPACE)))  # y
                )
                num_lines += 1
            else:
                # word in same line as last word
                # position word based on last placed word
                _RECT.topleft = (
                    int(last_word_rect.right + self.TEXT_WORD_SPACE),   # x
                    int(last_word_rect.topleft[1])           # y
                )

            current_line_width += (_RECT.width + self.TEXT_WORD_SPACE)
            last_word_rect = _RECT
            self.CX.display.blit(_TXT, _RECT)

    def draw_background(self, rect):
        ''' draw the menu background '''

        pygame.draw.rect(self.CX.display, self.bg_color, rect, 0)
        pygame.draw.rect(self.CX.display, self.border_color, rect, 2)

    def draw_buttons(self):
        ''' draw the buttons within the menu '''

        for btn in self.buttons:
            if btn.mouse_over:
                pygame.draw.rect(self.CX.display, self.cf.theme['BTN_BACKGROUND_HOVER'], btn.re, 0)
                pygame.draw.rect(self.CX.display, self.cf.theme['BTN_BORDERS_HOVER'], btn.re, 3)
                pygame.draw.rect(self.CX.display, self.cf.theme['BTN_BORDERS_EDGE_HOVER'], btn.re, 1)
                TXT = self.CX.FONTS['MENU_TXT_HOVER'].render(
                    str(btn.text), True, self.cf.theme['BTN_TEXT_HOVER'], self.cf.theme['BTN_BACKGROUND_HOVER'])
            else:
                pygame.draw.rect(self.CX.display, self.cf.theme['BTN_BACKGROUND'], btn.re, 0)
                pygame.draw.rect(self.CX.display, self.cf.theme['BTN_BORDERS'], btn.re, 3)
                pygame.draw.rect(self.CX.display, self.cf.theme['BTN_BORDERS_EDGE'], btn.re, 1)
                TXT = self.CX.FONTS['MENU_TXT'].render(
                    str(btn.text), True, self.cf.theme['BTN_TEXT'], self.cf.theme['BTN_BACKGROUND'])
            _RECT = TXT.get_rect()
            _RECT.center = btn.re.center
            self.CX.display.blit(TXT, _RECT)
