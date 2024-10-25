import pygame
from button import Button
import sys
from random import randint
from models.keys import Keys
pygame.init()
pygame.mixer.init()

# Defining mixer channels
background_channel = pygame.mixer.Channel(0)
sound_effect_channel = pygame.mixer.Channel(1)

keepRunning = True
Time = 0

#game settings
title = 'NEW GAME!'
color = "blue"
black = (0, 0, 0)
font = "./assets/menu/font.ttf"
menu_button= "./assets/menu/menu_rect.png"
window_width = 800
window_height = 600

#display setttings
screen = pygame.display.set_mode((window_width,window_height))


def get_font(size):
    return pygame.font.Font(font, size)

def main_menu():
    global keepRunning, Time,screen
    pygame.display.set_caption("Main Menu")

    while True:
        screen.blit(screen, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(38).render(title, True, "white")
        menu_rect = menu_text.get_rect(center=(window_width// 2, 100))
        image = pygame.image.load(menu_button)
        start_game = Button(image=pygame.transform.scale(image, (370, 80)),
                             pos=(window_width // 2, window_height // 2),
                             text_input="PLAY", font=get_font(25), base_color="black",
                             hovering_color="gray")

        screen.blit(menu_text, menu_rect)

        for button in [start_game]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if start_game.check_for_input(menu_mouse_pos):
                    keepRunning = True
                    return keepRunning



        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        pygame.display.update()

#controls settings
controls_not_shown = True
def show_controls(level):
    if level == 1:
        key_name = ['6','7','8','9']
    if level == 2:
        key_name = ['y','u','i','o']
    if level == 3:
        key_name = ['h','j','k','l']
    if level == 4:
        key_name = ['n','m','<','>']

    return key_name


stages_passed = 0
def stage_1():
    level_1 = get_font(10).render("level 1", True, "white")
    color = 'red'
    screen.fill(color)
    screen.blit(level_1, (10, 50))

    return True



#load space key sprite sheet
sprite_sheet_image = pygame.image.load("./assets/controls/SPACEALTERNATIVE.png")
sprite_sheet = Keys(sprite_sheet_image)
animation_list = []
animation_steps = 3
last_update= pygame.time.get_ticks()
animation_cooldown = 300
frame = 0

for x in range(animation_steps):
    animation_list.append(Keys.get_image(sprite_sheet,x,98,21,2,black))

#load keys sprite sheets

def load_key_sprite_sheets(level):
    global animation_steps
    key_1_list =[]
    key_2_list = []
    key_3_list = []
    key_4_list = []
    if level == 1:
        key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/6.png")
        key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
        for x in range(animation_steps):
            key_1_list.append(Keys.get_image(key_sprite_sheet_1,x,19,21,2,black))
        key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/7.png")
        key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
        for x in range(animation_steps):
            key_2_list.append(Keys.get_image(key_sprite_sheet_2,x,19,21,2,black))
        key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/8.png")
        key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
        for x in range(animation_steps):
            key_3_list.append(Keys.get_image(key_sprite_sheet_3,x,19,21,2,black))
        key_sprite_sheet_image_4 = pygame.image.load("./assets/controls/9.png")
        key_sprite_sheet_4 = Keys(key_sprite_sheet_image_4)
        for x in range(animation_steps):
            key_4_list.append(Keys.get_image(key_sprite_sheet_4,x,19,21,2,black))

    elif level == 2:
        key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/Y.png")
        key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
        for x in range(animation_steps):
            key_1_list.append(Keys.get_image(key_sprite_sheet_1,x,19,21,2,black))
        key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/U.png")
        key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
        for x in range(animation_steps):
            key_2_list.append(Keys.get_image(key_sprite_sheet_2,x,19,21,2,black))
        key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/I.png")
        key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
        for x in range(animation_steps):
            key_3_list.append(Keys.get_image(key_sprite_sheet_3,x,19,21,2,black))
        key_sprite_sheet_image_4 = pygame.image.load("./assets/controls/O.png")
        key_sprite_sheet_4 = Keys(key_sprite_sheet_image_4)
        for x in range(animation_steps):
            key_4_list.append(Keys.get_image(key_sprite_sheet_4,x,19,21,2,black))
    elif level == 3:
        key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/H.png")
        key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
        for x in range(animation_steps):
            key_1_list.append(Keys.get_image(key_sprite_sheet_1,x,19,21,2,black))
        key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/J.png")
        key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
        for x in range(animation_steps):
            key_2_list.append(Keys.get_image(key_sprite_sheet_2, x, 19, 21, 2, black))
        key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/K.png")
        key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
        for x in range(animation_steps):
            key_3_list.append(Keys.get_image(key_sprite_sheet_3, x, 19, 21, 2, black))
        key_sprite_sheet_image_4 = pygame.image.load("./assets/controls/L.png")
        key_sprite_sheet_4 = Keys(key_sprite_sheet_image_4)
        for x in range(animation_steps):
            key_4_list.append(Keys.get_image(key_sprite_sheet_4, x, 19, 21, 2, black))
    else:
        key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/N.png")
        key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
        for x in range(animation_steps):
            key_1_list.append(Keys.get_image(key_sprite_sheet_1, x, 19, 21, 2, black))
        key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/M.png")
        key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
        for x in range(animation_steps):
            key_2_list.append(Keys.get_image(key_sprite_sheet_2, x, 19, 21, 2, black))
        key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/LESSTHAN.png")
        key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
        for x in range(animation_steps):
            key_3_list.append(Keys.get_image(key_sprite_sheet_3, x, 19, 21, 2, black))
        key_sprite_sheet_image_4 = pygame.image.load("./assets/controls/GREATERTHAN.png")
        key_sprite_sheet_4 = Keys(key_sprite_sheet_image_4)
        for x in range(animation_steps):
            key_4_list.append(Keys.get_image(key_sprite_sheet_4, x, 19, 21, 2, black))


    return [key_1_list,key_2_list,key_3_list,key_4_list]





#apoio
level_controls = ['']*5




main_menu()
controls_screen = True
level = randint(1,4)

#game loop
while keepRunning:
    clock = pygame.time.Clock()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepRunning = False

    #controls screen

    if controls_screen:
        level_controls = show_controls(level)
        screen.fill(color)

        controls_text = get_font(10).render(f'Controls: {level_controls}', True, "white")
        screen.blit(controls_text, (window_width//2-150, window_height//2 - 250))
        press_space_text = get_font(10).render('Press Space to continue', True, "white")
        screen.blit(press_space_text, (window_width//2 - 100
                                       ,window_height-100))


        # update animation
        current_time = pygame.time.get_ticks()
        if current_time - last_update >= animation_cooldown:
            frame += 1
            last_update = current_time
            if frame >= len(animation_list):
                frame = 0

        # show key frame images
        keys_loaded = (load_key_sprite_sheets(level))
        screen.blit(animation_list[frame], (window_width // 2 - 100, window_height - 200))
        screen.blit(keys_loaded[0][frame],(window_width // 2 - 100,window_height - 280))
        screen.blit(keys_loaded[1][frame],(window_width // 2 - 60,window_height - 280))
        screen.blit(keys_loaded[2][frame],(window_width // 2 - 20,window_height - 280))
        screen.blit(keys_loaded[3][frame],(window_width // 2 + 20,window_height - 280))






        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            controls_screen =False
            stage_1()

        if keys[pygame.K_ESCAPE]:
            keepRunning = False
            pygame.quit()
            quit()






    keys = pygame.key.get_pressed()
    if keys[pygame.K_ESCAPE]:
        keepRunning = False
        pygame.quit()
        quit()

    pygame.display.flip()