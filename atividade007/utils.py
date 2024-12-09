import pygame
from models.keys import Keys
from settings import *

def load_key_sprite_sheets(level):
    animation_steps = 3
    key_1_list = []
    key_2_list = []
    key_3_list = []
    key_4_list = []
    key_5_list = []
    key_6_list = []
    if level == 1:
        key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/F.png")
        key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
        for x in range(animation_steps):
            key_1_list.append(Keys.get_image(key_sprite_sheet_1, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/J.png")
        key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
        for x in range(animation_steps):
            key_2_list.append(Keys.get_image(key_sprite_sheet_2, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/BACKSPACE.png")
        key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
        for x in range(animation_steps):
            key_3_list.append(Keys.get_image(key_sprite_sheet_3, x, 53, 21, 2, BLACK))
        return [key_1_list, key_2_list, key_3_list]

    elif level == 2:
        key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/A.png")
        key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
        for x in range(animation_steps):
            key_1_list.append(Keys.get_image(key_sprite_sheet_1, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/S.png")
        key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
        for x in range(animation_steps):
            key_2_list.append(Keys.get_image(key_sprite_sheet_2, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/D.png")
        key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
        for x in range(animation_steps):
            key_3_list.append(Keys.get_image(key_sprite_sheet_3, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_4 = pygame.image.load("./assets/controls/F.png")
        key_sprite_sheet_4 = Keys(key_sprite_sheet_image_4)
        for x in range(animation_steps):
            key_4_list.append(Keys.get_image(key_sprite_sheet_4, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_5 = pygame.image.load("./assets/controls/G.png")
        key_sprite_sheet_5 = Keys(key_sprite_sheet_image_5)
        for x in range(animation_steps):
            key_5_list.append(Keys.get_image(key_sprite_sheet_5, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_6 = pygame.image.load("./assets/controls/BACKSPACE.png")
        key_sprite_sheet_6 = Keys(key_sprite_sheet_image_6)
        for x in range(animation_steps):
            key_6_list.append(Keys.get_image(key_sprite_sheet_6, x, 53, 21, 2, BLACK))
        return [key_1_list, key_2_list, key_3_list, key_4_list, key_5_list, key_6_list]

    elif level == 3:
        key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/H.png")
        key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
        for x in range(animation_steps):
            key_1_list.append(Keys.get_image(key_sprite_sheet_1, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/J.png")
        key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
        for x in range(animation_steps):
            key_2_list.append(Keys.get_image(key_sprite_sheet_2, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/K.png")
        key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
        for x in range(animation_steps):
            key_3_list.append(Keys.get_image(key_sprite_sheet_3, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_4 = pygame.image.load("./assets/controls/L.png")
        key_sprite_sheet_4 = Keys(key_sprite_sheet_image_4)
        for x in range(animation_steps):
            key_4_list.append(Keys.get_image(key_sprite_sheet_4, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_5 = pygame.image.load("./assets/controls/C.png")
        key_sprite_sheet_5 = Keys(key_sprite_sheet_image_5)
        for x in range(animation_steps):
            key_5_list.append(Keys.get_image(key_sprite_sheet_5, x, 19, 21, 2, BLACK))
        key_sprite_sheet_image_6 = pygame.image.load("./assets/controls/BACKSPACE.png")
        key_sprite_sheet_6 = Keys(key_sprite_sheet_image_6)
        for x in range(animation_steps):
            key_6_list.append(Keys.get_image(key_sprite_sheet_6, x, 53, 21, 2, BLACK))
        return [key_1_list, key_2_list, key_3_list, key_4_list, key_5_list, key_6_list]


