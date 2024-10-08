#  Title of game's window
SCREEN_TITLE = 'Arkanoid'

#  Game level ending types
EXIT = 'exit'
GAME_OVER = 'game over'
PASSED = 'level passed'

#  Indent from the top of the screen
TOP_INDENT = 50

#  Info panel size
INFO_PANEL_HEIGHT = 30

#  Window size
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500 + TOP_INDENT + INFO_PANEL_HEIGHT

#  Frame rate to fps
FPS = 60

#  Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

#  Platform and ball color
FIRE_BRICK = (178, 34, 34)
SILVER = (192, 192, 192)
GRAY = (128, 128, 128)

#  Bricks colors
#  Hardness = 1 (green)
GREEN_YELLOW = (173, 255, 47)
DARK_GREEN = (0, 100, 0)

#  Hardness = 2 (red)
RED = (255, 140, 0)
DARK_RED = (139, 0, 0)

#  Hardness = 3 (blue)
ROYAL_BLUE = (65, 105, 225)
DARK_BLUE = (0, 0, 139)

#  Bonuses
LIME_GREEN = (50, 205, 50)

#  Brick size
BRICK_WIDTH = 50
BRICK_HEIGHT = 20

#  Platform size
PLATFORM_WIDTH = 72
PLATFORM_HEIGHT = 16

#  Number of player's lives
NUMBER_PLAYER_LIVES = 3

#  Laser firing delay
LASER_FIRE_DELAY = 15

#  Levels
LEVEL_01 = ((1,	1, 1, 1, 1,	1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
            (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
            (1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1),
            (1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 1),
            (1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1),
            (1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1),
            (1, 1, 1, 2, 2, 3, 3, 3, 3, 3, 3, 2, 2, 1, 1, 1),
            (1, 1, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 1, 1),
            (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
            (1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1),
            )

LEVEL_02 = ((1,	1, 2, 3, 3,	3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 1),
            (1, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 1),
            (0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0),
            (0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0),
            (0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0),
            (0, 1, 2, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 2, 1, 0),
            (0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0),
            (0, 0, 1, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 1, 0, 0),
            (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
            (0, 0, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0),
            )

LEVEL_03 = ((0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0),
            (0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0),
            (0, 0, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 0, 0),
            (0, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 0),
            (3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3),
            (3, 3, 2, 2, 1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 3, 3),
            (0, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 0),
            (0, 0, 3, 3, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 0, 0),
            (0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0),
            (0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 0, 0, 0, 0),
            )
