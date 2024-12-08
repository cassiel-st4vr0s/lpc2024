import pygame

# Defining audio channels
pygame.mixer.init()
background_channel = pygame.mixer.Channel(0)
sound_effect_channel = pygame.mixer.Channel(1)

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
GRAY = (80,80,80)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
SKY_BLUE = (69,179,224)
PLATFORM_WIDTH = 100
PLATFORM_HEIGHT = 30
PLAYER_SIZE = 15
GRAVITY = 0.5
JUMP_SPEED = -10
VERTICAL_SPACING = 80
MAX_COMBINATIONS = 9

#assets
FONT = './assets/menu/font.ttf'
MENU_BUTTON = './assets/menu/menu_rect.png'
TITLE = 'UP IN THE SKY'
LETTER_SIZE = 45
JUMP = pygame.mixer.Sound('./assets/sfx/jump.mp3')
BG_MENU = './assets/menu/castle.png'
BG_MUSIC = pygame.mixer.Sound('./assets/sfx/bg_music.mp3')
BUTTON_PRESS = pygame.mixer.Sound('./assets/sfx/button.mp3')
MISS = pygame.mixer.Sound('./assets/sfx/miss.mp3')
CORRECT = pygame.mixer.Sound('./assets/sfx/correct.mp3')
button_sfx = pygame.mixer.Sound(BUTTON_PRESS)
button_sfx.set_volume(0.3)

#animation
last_update = pygame.time.get_ticks()
frame = 0
animation_cooldown = 300
explosion_group = pygame.sprite.Group

#level variables
combinations_size = 4 #controla a quantidade maxima de elementos agrupados
letters_1 = ['f','j'] #controla as letras combinadas
letters_2 = ['a','s','d','f','g']
letters_3 = ['h','j','k','l','ç']
