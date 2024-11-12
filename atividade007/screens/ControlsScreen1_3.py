import pygame
import sys
from settings import *
from screens.start import Start
from models.keys import Keys

class ControlsScreen:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        global last_update, frame,animation_cooldown
        background = pygame.image.load("assets/sprites/background.png")
        background = pygame.transform.scale(background,(SCREEN_WIDTH,SCREEN_HEIGHT))

        keys_loaded = (ControlsScreen.load_key_sprite_sheets(self, 1))
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


    def load_key_sprite_sheets(self,level):
        animation_steps = 3
        key_1_list = []
        key_2_list = []
        key_3_list = []
        key_4_list = []
        key_5_list =[]
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
                key_3_list.append(Keys.get_image(key_sprite_sheet_3,x,53,21,2,BLACK))
            return [key_1_list,key_2_list,key_3_list]

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
            return [key_1_list, key_2_list, key_3_list, key_4_list, key_5_list,key_6_list]

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
        else:
            key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/N.png")
            key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
            for x in range(animation_steps):
                key_1_list.append(Keys.get_image(key_sprite_sheet_1, x, 19, 21, 2, BLACK))
            key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/M.png")
            key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
            for x in range(animation_steps):
                key_2_list.append(Keys.get_image(key_sprite_sheet_2, x, 19, 21, 2, BLACK))
            key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/LESSTHAN.png")
            key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
            for x in range(animation_steps):
                key_3_list.append(Keys.get_image(key_sprite_sheet_3, x, 19, 21, 2, BLACK))
            key_sprite_sheet_image_4 = pygame.image.load("./assets/controls/GREATERTHAN.png")
            key_sprite_sheet_4 = Keys(key_sprite_sheet_image_4)
            for x in range(animation_steps):
                key_4_list.append(Keys.get_image(key_sprite_sheet_4, x, 19, 21, 2, BLACK))

class ControlsScreen2:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        global last_update, frame,animation_cooldown
        background = pygame.image.load("assets/sprites/background.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        keys_loaded = (ControlsScreen.load_key_sprite_sheets(self, 2))
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

    def load_key_sprite_sheets(self,level):
        animation_steps = 3
        key_1_list = []
        key_2_list = []
        key_3_list = []
        key_4_list = []
        key_5_list =[]
        key_6_list = []

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
class ControlsScreen3:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        global last_update, frame,animation_cooldown
        background = pygame.image.load("assets/sprites/background.png")
        background = pygame.transform.scale(background, (SCREEN_WIDTH, SCREEN_HEIGHT))

        keys_loaded = (ControlsScreen.load_key_sprite_sheets(self, 3))
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

    def load_key_sprite_sheets(self,level):
        animation_steps = 3
        key_1_list = []
        key_2_list = []
        key_3_list = []
        key_4_list = []
        key_5_list =[]
        key_6_list = []

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