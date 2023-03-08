
class Local_settings:
    ''' wrapper for setting dicts '''
    def __init__(self, misc, fonts, buttons, theme_list):
        self.misc = misc
        self.fonts = fonts
        self.buttons = buttons
        self.theme_list = theme_list
        self.active_theme = self.misc['default_theme']
        self.theme = theme_list[self.active_theme]
        print(f'\nSuccesfully loaded {self}')

    def cycle_theme(self):
        if (len(self.theme_list) == 0):
            return
        if (self.active_theme == (len(self.theme_list) - 1)):
            self.active_theme = 0
        else:
            self.active_theme += 1
        self.theme = self.theme_list[self.active_theme]

    def __str__(self):
        theme_name = self.theme['description']
        available_themes = ''
        for t in self.theme_list:
            description = str(t['description'])
            available_themes += f' {description},'

        return str(f'Settings\n\tDefault theme:\t{theme_name}\n\tLoaded Themes: {available_themes}')


# color pallete
# TODO: un-caps these
COLORS = {
    'BLACK': (0, 0, 0),
    'OFFBLACK': (24, 26, 31),
    'DARKGRAY_DARKER': (42, 42, 42),
    'DARKGRAY_DARK': (70, 70, 70),
    'DARKGRAY': (80, 80, 80),
    'DARKGRAY_LIGHT': (90, 90, 90),
    'GRAY_SOFT': (108, 108, 108),
    'GRAY': (128, 128, 128),
    'GRAY_MEDIUM': (148, 148, 148),
    'GRAY_LIGHT': (168, 168, 158),
    'GRAY_LIGHTER': (178, 178, 168),
    'BONE': (237, 228, 201),
    'BONE_DARK': (217, 208, 191),
    'BONE_LIGHT': (207, 198, 181),
    'DARKLIVER': (100, 83, 83),
    'DARKLIVER_DARKER': (84, 73, 73),
    'SAGE': (200, 204, 146),
    'URANIANBLUE': (185, 230, 255),
    'DUTCHWHITE': (244, 228, 186),
    'MARYGOLD': (240, 162, 2),
    'MARYGOLD_DARK': (220, 162, 2),
    'ORANGE': (255, 123, 84),
    'PEACH': (255, 178, 107),
    'YELLOW': (255, 213, 111),
    'LIGHTYELLOW': (255, 251, 172),
    'LIGHTORANGE': (255, 188, 164),
    'NAVY': (32, 82, 149)
}

# general settings, mostly read in main.py
MISC = {
    'show_right_menu': True,  # whether or not to show the right pane (TODO: allow change during runtime)
    'debug_draw_containers': False,  # visualize the containers of screen objects
    # 'debug_color': COLORS['URANIANBLUE'],  # replaces some colors if debug_draw_containers
    'debug_color': COLORS['BLACK'],  # replaces some colors if debug_draw_containers
    'default_theme': 0,  # refers to index of settings.theme_list
    'caption': str("Sudoku Game - "),  # window caption
    'reader_path': {
        '1': str("./data/sudoku_boards/sudoku_easy_20000.csv"),
        '2': str("./data/sudoku_boards/sudoku_intermediate_5000.csv"),
        '3': str("./data/sudoku_boards/sudoku_expert_5000.csv"),
        # new csv files can be added here. sorted by difficulty
    },
    'reader_default_difficulty': '1',   # refers to reader_path key
    'board_size': int(630),  # window size == (board size + menu size + board margins)
    'box_grid_linewidth': int(2),
    'board_margin_top': int(20),
    'board_margin_bottom': int(10),
    'board_margin_right': int(20),
    'board_margin_left': int(20),
    'right_menu_width': int(200),
    'menu_height': int(70),  # height of the main menu container
    # TODO: own setting for button height instead of using menu_height
    'menu_btn_margin': int(8),
    'menu_border_width': int(2),
    'popup_menu_border_width': int(2),
    'sub_menu_border_width': int(2),
    'menu_text_line_space': int(2),    # space between lines
    'menu_text_word_space': int(7),    # space between words
    'menu_text_margin_top': int(14),   # margin to the top of the parent roct
    'menu_text_margin_left': int(14),  # margin to the left of the parent rect
    'popup_window_width': int(300),
    'popup_window_height': int(200),
    'max_fps': float(240),  # unsigned int | None
    'controls': str('mouse'),  # 'mouse' | 'keyboard'
    'highlight_related_squares': True,
}

# change fonts // font size from here
FONTS = {
    'SQUARE_NUM': {'style': './data/fonts/JetBrainsMono-SemiBold.ttf', 'size': 42},
    'MENU_TXT': {'style': './data/fonts/JetBrainsMono-SemiBold.ttf', 'size': 21},
    'MENU_TXT_BIG': {'style': './data/fonts/JetBrainsMono-Bold.ttf', 'size': 21},
    'MENU_TXT_HOVER': {'style': './data/fonts/JetBrainsMono-Bold.ttf', 'size': 24}
}

# change colors for different parts of the UI
# theme color settings. Refers to COLORS
PASTEL_THEME = {
    'description': 'PASTEL_THEME',
    'WINDOW_BACKGROUND': COLORS['DARKGRAY'],
    # default menu style
    'MENU_BACKGROUND': COLORS['DARKGRAY'],
    'MENU_BORDER': COLORS['BLACK'],
    # right menu / sub menus
    'MENU_TEXT': COLORS['BLACK'],
    'MENU_TEXT_BIG': COLORS['OFFBLACK'],
    'RIGHT_MENU_BACKGROUND': COLORS['LIGHTORANGE'],
    'RIGHT_MENU_BORDER': COLORS['OFFBLACK'],
    'RIGHT_MENU_TEXT': COLORS['DARKLIVER'],
    'POPUP_MENU_BACKGROUND': COLORS['DARKGRAY'],
    'POPUP_MENU_TEXT': COLORS['GRAY_LIGHT'],
    'POPUP_MENU_BORDER': COLORS['OFFBLACK'],
    # buttons
    'BTN_BACKGROUND': COLORS['DUTCHWHITE'],
    'BTN_BORDERS': COLORS['ORANGE'],
    'BTN_BORDERS_EDGE': COLORS['PEACH'],
    'BTN_BACKGROUND_HOVER': COLORS['LIGHTYELLOW'],
    'BTN_BORDERS_HOVER': COLORS['MARYGOLD'],
    'BTN_BORDERS_EDGE_HOVER': COLORS['ORANGE'],
    'BTN_TEXT': COLORS['DARKGRAY'],
    'BTN_TEXT_HOVER': COLORS['OFFBLACK'],
    # board
    'BOARD_BORDER': COLORS['OFFBLACK'],
    'BOX_GRID': COLORS['OFFBLACK'],
    # squares
    'SQUARE_TEXT_MEDI': COLORS['NAVY'],
    'SQUARE_TEXT_HARD': COLORS['BLACK'],
    'SQUARE_BORDER': COLORS['GRAY'],
    'SQUARE_BACKGROUND': COLORS['BONE'],
    # selected / highlighted squares
    'SELECTED_SQUARE_BACKGROUND': COLORS['PEACH'],
    'SELECTED_SQUARE_BORDER': COLORS['MARYGOLD_DARK'],
    'SELECTED_SQUARE_RELATION_BACKGROUND': COLORS['BONE_DARK'],
    'SELECTED_SQUARE_RELATION_BORDER': COLORS['LIGHTORANGE'],
    'DEBUG': MISC['debug_color'],
}

DARK_THEME = {
    'description': 'DARK_THEME',
    'WINDOW_BACKGROUND': COLORS['DARKLIVER_DARKER'],
    # default menu style
    'MENU_BACKGROUND': COLORS['DARKGRAY'],
    'MENU_BORDER': COLORS['BLACK'],
    # right menu / sub menus
    'MENU_TEXT': COLORS['BLACK'],
    'MENU_TEXT_BIG': COLORS['GRAY_LIGHTER'],
    'RIGHT_MENU_TEXT': COLORS['OFFBLACK'],
    'POPUP_MENU_TEXT': COLORS['GRAY_LIGHT'],
    'RIGHT_MENU_BACKGROUND': COLORS['DARKLIVER_DARKER'],
    'POPUP_MENU_BACKGROUND': COLORS['DARKGRAY'],
    'RIGHT_MENU_BORDER': COLORS['DARKLIVER_DARKER'],
    'POPUP_MENU_BORDER': COLORS['OFFBLACK'],
    # buttons
    'BTN_BACKGROUND': COLORS['GRAY_LIGHT'],
    'BTN_BORDERS': COLORS['DARKGRAY_DARKER'],
    'BTN_BORDERS_EDGE': COLORS['DARKLIVER_DARKER'],
    'BTN_BACKGROUND_HOVER': COLORS['GRAY'],
    'BTN_BORDERS_HOVER': COLORS['GRAY'],
    'BTN_BORDERS_EDGE_HOVER': COLORS['BONE'],
    'BTN_TEXT': COLORS['DARKGRAY_DARKER'],
    'BTN_TEXT_HOVER': COLORS['OFFBLACK'],
    # board
    'BOARD_BORDER': COLORS['DARKLIVER_DARKER'],
    'BOX_GRID': COLORS['DARKGRAY'],
    # squares
    'SQUARE_TEXT_MEDI': COLORS['BONE_DARK'],
    'SQUARE_TEXT_HARD': COLORS['OFFBLACK'],
    'SQUARE_BORDER': COLORS['GRAY_LIGHT'],
    'SQUARE_BACKGROUND': COLORS['GRAY'],
    # selected / highlighted squares
    'SELECTED_SQUARE_BACKGROUND': COLORS['GRAY_MEDIUM'],
    'SELECTED_SQUARE_BORDER': COLORS['BONE'],
    'SELECTED_SQUARE_RELATION_BACKGROUND': COLORS['GRAY_SOFT'],
    'SELECTED_SQUARE_RELATION_BORDER': COLORS['GRAY'],
    'DEBUG': MISC['debug_color'],
}

# add buttons, sizing / position is done dynamically.
# to add a new button:
# 1. add it to the dict here
# 2. alter _btn_function_redirect() in main.py to link the button id with any functionality
# Note: Functionality is not required in order for the button to appear correctly.
BUTTONS = {
    'main_menu': {
        'BTN_toggle_highlighting': {
            'id': 'BTN_toggle_highlighting',
            'description': str('Mode')
        },
        'BTN_change_theme': {
            'id': 'BTN_change_theme',
            'description': str('Theme')
        },
        'BTN_change_difficulty': {
            'id': 'BTN_change_difficulty',
            'description': str('Level')
        },
        'BTN_check': {
            'id': 'BTN_check',
            'description': str('Check')
        },
        'BTN_solve': {
            'id': 'BTN_solve',
            'description': str('Solve')
        },
        'BTN_reset': {
            'id': 'BTN_reset',
            'description': str('Reset')
        },
        'BTN_new_board': {
            'id': 'BTN_new_board',
            'description': str('New')
        },
    },
    'popup_info': {
        'BTN_ok': {
            'id': 'BTN_ok',
            'description': str('OK')
        }
    },
    'popup_options': {
        'BTN_yes': {
            'id': 'BTN_yes',
            'description': str('YES')
        },
        'BTN_no': {
            'id': 'BTN_no',
            'description': str('NO')
        }
    }
}

themes = [PASTEL_THEME, DARK_THEME]
settings = Local_settings(MISC, FONTS, BUTTONS, themes)
