import pygame
from button import Button
import sys
from random import randint

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
font = "./assets/font.ttf"
menu_button= "./assets/menu_rect.png"
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
        key_name = ['F5','F6','F7','F8']
    if level == 2:
        key_name = ['6','7','8','9']
    if level == 3:
        key_name = ['y','u','i','o']
    if level == 4:
        key_name = ['h','j','k','l']
    if level == 5:
        key_name = ['n','m','comma','period']

    return key_name

stages_passed = 0
def stage_1():
    level_1 = get_font(10).render("level 1", True, "white")
    color = 'red'
    screen.fill(color)
    screen.blit(level_1, (10, 50))




level_controls = ['']*5
main_menu()
#game loop
while keepRunning:
    clock = pygame.time.Clock()
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            keepRunning = False

    if controls_not_shown:
        level = randint(1,5)
        level_controls = show_controls(level)
        controls_text = get_font(10).render(f'Controls: {level_controls}', True, "white")
        screen.fill(color)
        screen.blit(controls_text, (window_width//2-150, window_height//2 - 250))
        press_space_text = get_font(10).render('Press Space to continue', True, "white")
        screen.blit(press_space_text, (window_width//2 - 80,window_height-100))
        controls_not_shown = False

    keys = pygame.key.get_pressed()
    if keys[pygame.K_SPACE]:
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