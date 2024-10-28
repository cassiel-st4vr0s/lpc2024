import pygame
import random
import sys

from models.keys import Keys
from button import Button

pygame.init()
pygame.mixer.init()

# Defining audio channels
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
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 40
PLAYER_SIZE = 30
GRAVITY = 0.5
JUMP_SPEED = -10
VERTICAL_SPACING = 100
TITLE = 'UP IN THE SKY'

#assets
FONT = './assets/menu/font.ttf'
MENU_BUTTON = './assets/menu/menu_rect.png'
JUMP = pygame.mixer.Sound('./assets/sfx/jump.mp3')
BG_MENU = './assets/menu/bg_castle.jpg'
BG_MUSIC = pygame.mixer.Sound('./assets/sfx/bg_music.mp3')
BUTTON_PRESS = pygame.mixer.Sound('./assets/sfx/button.mp3')
MISS = pygame.mixer.Sound('./assets/sfx/miss.mp3')


#animation
last_update = pygame.time.get_ticks()
frame = 0
animation_cooldown = 300

class Player:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.target_y = y
        self.vel_y = 0
        self.jumping = False
        self.current_platform = None
        self.rect = pygame.Rect(x, y, PLAYER_SIZE, PLAYER_SIZE)

    def update(self):
        if self.jumping:
            if abs(self.y - self.target_y) > 2:
                self.y += (self.target_y - self.y) * 0.1
            else:
                self.y = self.target_y
                self.jumping = False
        else:
            self.vel_y += GRAVITY
            self.y += self.vel_y
            
            if self.y > SCREEN_HEIGHT - PLAYER_SIZE:
                self.y = SCREEN_HEIGHT - PLAYER_SIZE
                self.vel_y = 0

        self.rect.y = self.y
        self.rect.x = self.x

    def jump_to_platform(self, platform):
        self.jumping = True
        self.target_y = platform.y - PLAYER_SIZE
        self.x = platform.x + (PLATFORM_WIDTH // 2) - (PLAYER_SIZE // 2)
        self.rect.x = self.x
        self.vel_y = 0

class Platform:
    def __init__(self, x, y, text):
        self.x = x
        self.y = y
        self.text = text
        self.typed = ""
        self.completed = False
        self.rect = pygame.Rect(x, y, PLATFORM_WIDTH, PLATFORM_HEIGHT)

    def is_text_match(self):
        return self.typed == self.text
class GameLoop:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Typing Game - Phase 1")



        self.gameStateManager = GameStateManager('main menu')
        self.start = Start(self.screen, self.gameStateManager)
        self.controlsScreen = ControlsScreen(self.screen, self.gameStateManager)
        self.level_1 = Level_1(self.screen,self.gameStateManager)

        self.states = {'main menu': self.start, 'controls screen': self.controlsScreen, 'level 1': self.level_1}

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
            self.states[self.gameStateManager.get_state()].run()
            pygame.display.update()

class Level_1:
    def __init__(self,display,gameStateManager):
        self.display = display
        pygame.display.set_caption("Typing Game - Phase 1")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE)
        self.platforms = self.create_platforms()
        self.target_platform_idx = 0
        self.game_over = False
        self.won = False

        self.gameStateManager = gameStateManager
    def create_platforms(self):
        platforms = []
        platform_texts = [
            "fj", "ff", "jj",
            "fjf", "jfj", "ffj", "jjf",
            "ffjj"
        ]
        
        base_y = SCREEN_HEIGHT - 100
        for i, text in enumerate(platform_texts):
            y = base_y - (i * VERTICAL_SPACING)
            x = random.randint(50, SCREEN_WIDTH - PLATFORM_WIDTH - 50)
            
            if i > 0:
                prev_platform = platforms[i-1]
                min_spacing = VERTICAL_SPACING - 20
                if prev_platform.y - y < min_spacing:
                    y = prev_platform.y - min_spacing
            platforms.append(Platform(x, y, text))
        
        return platforms

    def find_current_platform(self):
        # find the platform the player is currently on or closest to
        closest_platform = None
        min_distance = float('inf')
        
        for i, platform in enumerate(self.platforms):
            if not platform.completed:
                # check if player is on or very close to this platform
                if (abs(self.player.rect.bottom - platform.rect.top) < 5 and
                    self.player.x >= platform.x and 
                    self.player.x <= platform.x + PLATFORM_WIDTH):
                    return i
                
                # calculate distance to platform
                dx = (platform.x + PLATFORM_WIDTH/2) - (self.player.x + PLAYER_SIZE/2)
                dy = (platform.y) - (self.player.y + PLAYER_SIZE)
                distance = (dx * dx + dy * dy) ** 0.5
                
                if distance < min_distance:
                    min_distance = distance
                    closest_platform = i
        
        return closest_platform if closest_platform is not None else 0

    def handle_input(self, event):
        if event.type == pygame.KEYDOWN:
            if not self.player.jumping and self.target_platform_idx < len(self.platforms):
                current_idx = self.find_current_platform()
                target_platform = self.platforms[current_idx]
                
                if event.unicode in ['f', 'j']:
                    target_platform.typed += event.unicode
                    
                    if target_platform.is_text_match():
                        target_platform.completed = True
                        self.target_platform_idx = current_idx + 1

                        if self.target_platform_idx < len(self.platforms):
                            # find the next uncompleted platform
                            while (self.target_platform_idx < len(self.platforms) and 
                                   self.platforms[self.target_platform_idx].completed):
                                self.target_platform_idx += 1
                            
                            if self.target_platform_idx < len(self.platforms):
                                next_platform = self.platforms[self.target_platform_idx]
                                self.player.jump_to_platform(next_platform)
                                sound_effect_channel.play(JUMP)
                            else:
                                self.won = True
                        else:
                            self.won = True
                    elif len(target_platform.typed) >= len(target_platform.text):
                        target_platform.typed = ""
                        sound_effect_channel.play(MISS)

    def update(self):
        self.player.update()

        if not self.player.jumping:
            for platform in self.platforms:
                if (self.player.rect.colliderect(platform.rect) and 
                    self.player.vel_y > 0 and 
                    not platform.completed):
                    self.player.y = platform.rect.top - PLAYER_SIZE
                    self.player.vel_y = 0
                    self.player.current_platform = platform

        if self.player.y > SCREEN_HEIGHT:
            self.game_over = True

    def draw(self):
        self.display.fill(SKY_BLUE)

        for i, platform in enumerate(self.platforms):
            color = GREEN if platform.completed else WHITE
            pygame.draw.rect(self.display, color, platform.rect)
            
            text_surface = self.font.render(platform.text, True, BLACK)
            text_rect = text_surface.get_rect(center=(platform.x + PLATFORM_WIDTH/2, platform.y + PLATFORM_HEIGHT/2))
            self.display.blit(text_surface, text_rect)
            
            current_idx = self.find_current_platform()
            if i == current_idx and not platform.completed:
                typed_surface = self.font.render(platform.typed, True, BLUE)
                typed_rect = typed_surface.get_rect(center=(platform.x + PLATFORM_WIDTH/2, platform.y - 25))
                self.display.blit(typed_surface, typed_rect)

        pygame.draw.rect(self.display, RED, self.player.rect)

        if self.game_over:
            text = self.font.render("Game Over! Press R to restart", True, WHITE)
            self.display.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
        elif self.won:
            text = self.font.render("You Won! Press R to restart", True, WHITE)
            self.display.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and (self.game_over or self.won):
                        self.__init__(self.display,self.gameStateManager)
                    else:
                        self.handle_input(event)

            if not self.game_over and not self.won:
                self.update()
            self.draw()
            self.clock.tick(FPS)



class Start:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager

    def get_font(self, size):
        return pygame.font.Font(FONT, size)

    def run(self):
        global background_channel
        pygame.display.set_caption("Main Menu")
        running = True
        bg = pygame.image.load(BG_MENU)
        bg = pygame.transform.scale_by(bg, 0.7)
        background_channel.play(BG_MUSIC,loops=-1)
        BG_MUSIC.set_volume(0.2)

        BUTTON_PRESS.set_volume(0.3)

        while running:
            self.display.fill(SKY_BLUE)
            self.display.blit(bg, (0,100))

            menu_mouse_pos = pygame.mouse.get_pos()
            menu_text = Start.get_font(self, 36).render(TITLE, True, GRAY)
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH //2, 100))
            image = pygame.image.load(MENU_BUTTON)
            start_game = Button(image=pygame.transform.scale(image, (370, 80)),
                                pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                text_input="PLAY", font=Start.get_font(self, 25), base_color=BLACK,
                                hovering_color=GRAY)

            self.display.blit(menu_text, menu_rect)

            for button in [start_game]:
                button.change_color(menu_mouse_pos)
                button.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_game.check_for_input(menu_mouse_pos):
                        sound_effect_channel.play(BUTTON_PRESS)
                        running = False


            pygame.display.update()

        self.gameStateManager.set_state('controls screen')

class ControlsScreen:
    def __init__(self,display,gameStateManager):
        self.display = display
        self.gameStateManager = gameStateManager
    def run(self):
        global last_update, frame,animation_cooldown

        bg = pygame.image.load(BG_MENU)
        keys_loaded = (ControlsScreen.load_key_sprite_sheets(self, 1))
        controls_text = Start.get_font(self,30).render('Controls:', True, WHITE)
        press_any = Start.get_font(self,20).render('Press ANY KEY to CONTINUE', True, WHITE)
        button_sfx = pygame.mixer.Sound(BUTTON_PRESS)
        button_sfx.set_volume(0.3)
        running = True
        while running:
            self.display.fill(SKY_BLUE)

            # update animation
            current_time = pygame.time.get_ticks()
            if current_time - last_update >= animation_cooldown:
                frame += 1
                last_update = current_time
                if frame >= 3:
                    frame = 0
            self.display.blit(controls_text, (SCREEN_WIDTH//2 - 130, 300))
            self.display.blit(press_any,(150,SCREEN_HEIGHT-100))
            self.display.blit(keys_loaded[0][frame], (SCREEN_WIDTH//2-100,SCREEN_HEIGHT//2 ))
            self.display.blit(keys_loaded[1][frame], (SCREEN_WIDTH//2 + 50, SCREEN_HEIGHT//2))

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
        if level == 1:
            key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/F.png")
            key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
            for x in range(animation_steps):
                key_1_list.append(Keys.get_image(key_sprite_sheet_1, x, 19, 21, 2, BLACK))
            key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/J.png")
            key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
            for x in range(animation_steps):
                key_2_list.append(Keys.get_image(key_sprite_sheet_2, x, 19, 21, 2, BLACK))


        elif level == 2:
            key_sprite_sheet_image_1 = pygame.image.load("./assets/controls/Y.png")
            key_sprite_sheet_1 = Keys(key_sprite_sheet_image_1)
            for x in range(animation_steps):
                key_1_list.append(Keys.get_image(key_sprite_sheet_1, x, 19, 21, 2, BLACK))
            key_sprite_sheet_image_2 = pygame.image.load("./assets/controls/U.png")
            key_sprite_sheet_2 = Keys(key_sprite_sheet_image_2)
            for x in range(animation_steps):
                key_2_list.append(Keys.get_image(key_sprite_sheet_2, x, 19, 21, 2, BLACK))
            key_sprite_sheet_image_3 = pygame.image.load("./assets/controls/I.png")
            key_sprite_sheet_3 = Keys(key_sprite_sheet_image_3)
            for x in range(animation_steps):
                key_3_list.append(Keys.get_image(key_sprite_sheet_3, x, 19, 21, 2, BLACK))
            key_sprite_sheet_image_4 = pygame.image.load("./assets/controls/O.png")
            key_sprite_sheet_4 = Keys(key_sprite_sheet_image_4)
            for x in range(animation_steps):
                key_4_list.append(Keys.get_image(key_sprite_sheet_4, x, 19, 21, 2, BLACK))
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

        return [key_1_list, key_2_list, key_3_list, key_4_list]


class GameStateManager:
    def __init__(self,currentState):
        self.currentState = currentState

    def get_state(self):
        return self.currentState
    def set_state(self,state):
        self.currentState = state

if __name__ == "__main__":
    gameLoop = GameLoop()
    gameLoop.run()



