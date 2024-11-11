import pygame
from classes import player, platform
from settings import *
from classes.player import *
import random
from itertools import product
from classes.platform import *
import sys
from main import combinations_size, letters_1

from settings import PLATFORM_WIDTH, PLATFORM_HEIGHT, MAX_COMBINATIONS, explosion_group,SCREEN_WIDTH,sound_effect_channel,button_sfx,SKY_BLUE



class Level_1:
    def __init__(self,display,gameStateManager,player_class, platform_class):
        self.display = display
        pygame.display.set_caption("Typing Game - Phase 1")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, LETTER_SIZE)
        self.player = Player(self.display,SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE)
        self.platform = (Platform(0,0, 'ola'))
        self.platforms = self.create_platforms()
        self.target_platform_idx = 0
        self.player_class = player
        self.platform_class = platform
        self.game_over = False
        self.won = False
        self.gameStateManager = gameStateManager
        self.background = pygame.image.load("assets/sprites/background.png")
        self.background = pygame.transform.scale(self.background, (SCREEN_WIDTH, SCREEN_HEIGHT))

    def sequence_generator(self): #função que controla a criação das sequencias das letras
        platform_texts = []
        for size in range(1, combinations_size + 1): #limita o numero maximo de elementos
            for word in product(letters_1, repeat = size):
                platform_texts.append("".join(word))

        return platform_texts

    def create_platforms(self):
        platforms = []
        platform_texts = self.sequence_generator()
        random.shuffle(platform_texts)
        print(platform_texts)

        
        base_y = SCREEN_HEIGHT - 100
        for i, text in enumerate(platform_texts):
            y = base_y - (i * VERTICAL_SPACING)
            x = random.randint(50, SCREEN_WIDTH - PLATFORM_WIDTH - 50)

            if i==0: #posiciona o player na primeira plataforma
                self.player.x = x + (PLATFORM_WIDTH // 2) - (PLAYER_SIZE // 2)
                self.player.y = y

            if i > 0:
                prev_platform = platforms[i-1]
                min_spacing = VERTICAL_SPACING - 20
                if prev_platform.y - y < min_spacing:
                    y = prev_platform.y - min_spacing

            if i == MAX_COMBINATIONS:
                break
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
                
                if event.unicode in letters_1:
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
                if pygame.key.get_pressed()[pygame.K_BACKSPACE]:
                    target_platform.typed = ""


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
        #condição de game over
        if self.player.rect.bottom >= SCREEN_HEIGHT - PLAYER_SIZE :
            self.game_over = True


    def draw(self):
        self.display.fill(SKY_BLUE)
        self.display.blit(self.background,(0,0))

        for i, platform in enumerate(self.platforms):
            self.display.blit(self.platform.platform_typeA, (platform.x - 9, platform.y - 30))
            if platform.completed:
                outline_coordinates = []
                for pixel in self.platform.outline_pixels:
                    point = (pixel[0] + platform.x - 10, platform.y + pixel[1] - 30)
                    outline_coordinates.append(point)
                pygame.draw.polygon(self.display,(0,255,0),outline_coordinates,5)

            
            text_surface = self.font.render(platform.text, True, BLACK)
            text_rect = text_surface.get_rect(center=(platform.x + PLATFORM_WIDTH/2, platform.y + PLATFORM_HEIGHT/2))
            self.display.blit(text_surface, text_rect)
            
            current_idx = self.find_current_platform()
            if i == current_idx and not platform.completed:
                typed_surface = self.font.render(platform.typed, True, BLUE)
                typed_rect = typed_surface.get_rect(midleft=(platform.rect.right + 10, platform.rect.centery))
                self.display.blit(typed_surface, typed_rect)

        pygame.draw.rect(self.display, RED, self.player.rect)
        self.display.blit(self.player.character, (self.player.x - 25, self.player.y - 30))

        if self.game_over:
            text = self.font.render("Game Over! Press R to restart", True, BLACK)
            self.display.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

        elif self.won:
            sound_effect_channel.play(CORRECT)

            text = self.font.render("You Won! Press R to proceed!", True, BLACK)
            self.display.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

        pygame.display.flip()

    def run(self):
        running = True
        time = 30
        pygame.time.set_timer(pygame.USEREVENT,1000)
        screen = self.background
        timer_text = self.font.render(f"{time}", True, BLACK)
        timer_text_rect = pygame.Rect(40,50,40,35)
        timer_text_rect.center = (40,40)
        pygame.draw.rect(screen,WHITE,timer_text_rect)

        while running:
            if time <=0:
                self.game_over = True
                running = False
                break
            pygame.draw.rect(screen, WHITE, timer_text_rect)
            timer_text = self.font.render(f"{time}", True, BLACK)
            screen.blit(timer_text,timer_text_rect)
            for event in pygame.event.get():
                if event.type == pygame.USEREVENT:
                    time -=1
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:

                    if event.key == pygame.K_r and self.game_over:
                        self.game_over = False
                        self.won = False
                        running = False
                        break
                    elif event.key == pygame.K_r and self.won:
                        sound_effect_channel.play(button_sfx)
                        self.won = False
                        self.game_over = False
                        running = False
                        break
                    elif event.key == pygame.K_SPACE:
                        self.game_over = True
                        running = False
                        break
                    else:
                        self.handle_input(event)
            self.gameStateManager.set_state('controls screen 2')

            if not self.game_over and not self.won:
                self.update()


            self.draw()
            self.clock.tick(FPS)
        if self.game_over:
            self.player = Player(self.display, SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE)
            self.platforms = self.create_platforms()
            self.target_platform_idx = 0
            self.gameStateManager.set_state('controls screen')
            self.game_over = False
            running = True
        else:
            self.gameStateManager.set_state('controls screen 2')




