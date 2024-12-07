from enum import Enum
from turtledemo.colormixer import ColorTurtle


TITLE = "Galatic Defenders"
FONT = "assets/MENU/font.ttf"
RECT = "assets/MENU/menu_rect.png"
BASE_COLOR = (255,255,255)
HOVERING_COLOR = (255,0,255)
BG_MUSIC = "assets/Sound Game/menu_bg_music.mp3"
BUTTON_SELECT = "assets/Sound Game/menu_button.mp3"
VICTORY_THEME = "assets/Sound Game/victory_theme.mp3"

BLACK = (0,0,0)
WHITE = (255,255,255)
WINDOW_WIDTH = 700
WINDOW_HEIGHT = 650
RED = (255,0,0)

BULLET_RADIUS = 100
BULLET_SPEED = 20
BULLET_DX = 0
BULLET_DY = 0
BULLET_COLOR = (255, 255, 255)

MAX_LIFES = 4

MAX_ENEMY_SPAWN = 7


class BulletDirection(Enum):
    LEFT = 0
    RIGHT = 1
    UP = 2
    DOWN = 3
