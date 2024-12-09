import pygame
import sys
from settings import *
from screens.start import Start
from models.keys import Keys
from utils import load_key_sprite_sheets

class ControlsScreen:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        global last_update, frame,animation_cooldown
        background = pygame.image.load("assets/sprites/background.png")
        background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

        keys_loaded = load_key_sprite_sheets( 1)
        controls_text = Start.get_font(self,30).render('Controls:', True, BLACK)
        press_any = Start.get_font(self,20).render('Press ANY KEY to CONTINUE', True, BLACK)
        button_sfx = pygame.mixer.Sound(BUTTON_PRESS)
        button_sfx.set_volume(0.3)
        running = True
        while running:
            self.display.blit(background,(0,0))

            # update animation
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= animation_cooldown:
                frame += 1
                last_update = current_time
                if frame >= 3:
                    frame = 0
            self.display.blit(controls_text, (SCREEN_WIDTH//2 - 130, 300))
            self.display.blit(press_any,(150,SCREEN_HEIGHT-100))

            if len(keys_loaded)>=4:
                self.display.blit(keys_loaded[0][frame], (SCREEN_WIDTH//2 -100,SCREEN_HEIGHT//2 ))
                self.display.blit(keys_loaded[1][frame], (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2))
                self.display.blit(keys_loaded[2][frame], (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2 ))
                self.display.blit(keys_loaded[3][frame], (SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2))
                self.display.blit(keys_loaded[4][frame],(SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2))
            else:
                self.display.blit(keys_loaded[0][frame],(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                self.display.blit(keys_loaded[1][frame], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))
                self.display.blit(keys_loaded[2][frame], (SCREEN_WIDTH // 2 , SCREEN_HEIGHT // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    sound_effect_channel.play(button_sfx)
                    running = False
            pygame.display.update()
        self.gameStateManager.set_state('level 1')





class ControlsScreen2:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        global last_update, frame,animation_cooldown
        background = pygame.image.load("assets/sprites/background.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        keys_loaded = load_key_sprite_sheets(2)
        controls_text = Start.get_font(self,30).render('Controls:', True, BLACK)
        press_any = Start.get_font(self,20).render('Press ANY KEY to CONTINUE', True, BLACK)
        button_sfx = pygame.mixer.Sound(BUTTON_PRESS)
        button_sfx.set_volume(0.3)
        running = True
        while running:
            self.display.fill(SKY_BLUE)
            self.display.blit(background, (0, 0))

            # update animation
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= animation_cooldown:
                frame += 1
                last_update = current_time
                if frame >= 3:
                    frame = 0
            self.display.blit(controls_text, (SCREEN_WIDTH//2 - 130, 300))
            self.display.blit(press_any,(150,SCREEN_HEIGHT-100))

            if len(keys_loaded)>=4:
                self.display.blit(keys_loaded[0][frame], (SCREEN_WIDTH//2 -100,SCREEN_HEIGHT//2 ))
                self.display.blit(keys_loaded[1][frame], (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2))
                self.display.blit(keys_loaded[2][frame], (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2 ))
                self.display.blit(keys_loaded[3][frame], (SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2))
                self.display.blit(keys_loaded[4][frame],(SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2))
                self.display.blit(keys_loaded[5][frame],(SCREEN_WIDTH//2+150,SCREEN_HEIGHT//2))
            else:
                self.display.blit(keys_loaded[0][frame], (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                self.display.blit(keys_loaded[1][frame], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    sound_effect_channel.play(button_sfx)
                    running = False
            pygame.display.update()
        self.gameStateManager.set_state('level 2')


class ControlsScreen3:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        global last_update, frame,animation_cooldown
        background = pygame.image.load("assets/sprites/background.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        keys_loaded = load_key_sprite_sheets(3)
        controls_text = Start.get_font(self,30).render('Controls:', True, BLACK)
        press_any = Start.get_font(self,20).render('Press ANY KEY to CONTINUE', True, BLACK)
        button_sfx = pygame.mixer.Sound(BUTTON_PRESS)
        button_sfx.set_volume(0.3)
        running = True
        while running:
            self.display.fill(SKY_BLUE)
            self.display.blit(background, (0, 0))

            # update animation
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= animation_cooldown:
                frame += 1
                last_update = current_time
                if frame >= 3:
                    frame = 0
            self.display.blit(controls_text, (SCREEN_WIDTH//2 - 130, 300))
            self.display.blit(press_any,(150,SCREEN_HEIGHT-100))

            if len(keys_loaded)>=4:
                self.display.blit(keys_loaded[0][frame], (SCREEN_WIDTH//2 -100,SCREEN_HEIGHT//2 ))
                self.display.blit(keys_loaded[1][frame], (SCREEN_WIDTH//2 - 50, SCREEN_HEIGHT//2))
                self.display.blit(keys_loaded[2][frame], (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2 ))
                self.display.blit(keys_loaded[3][frame], (SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2))
                self.display.blit(keys_loaded[4][frame],(SCREEN_WIDTH//2 + 100, SCREEN_HEIGHT//2))
                self.display.blit(keys_loaded[5][frame],(SCREEN_WIDTH//2 + 150,SCREEN_HEIGHT//2))
            else:
                self.display.blit(keys_loaded[0][frame], (SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2))
                self.display.blit(keys_loaded[1][frame], (SCREEN_WIDTH // 2 - 50, SCREEN_HEIGHT // 2))

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    sound_effect_channel.play(button_sfx)
                    running = False
            pygame.display.update()
        self.gameStateManager.set_state('level 3')

