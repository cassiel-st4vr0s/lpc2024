import pygame
import random
import sys

pygame.init()

# constants
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
FPS = 60
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
PLATFORM_WIDTH = 150
PLATFORM_HEIGHT = 40
PLAYER_SIZE = 30
GRAVITY = 0.5
JUMP_SPEED = -10
VERTICAL_SPACING = 100

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

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Typing Game - Phase 1")
        self.clock = pygame.time.Clock()
        self.font = pygame.font.Font(None, 36)
        
        self.player = Player(SCREEN_WIDTH // 2, SCREEN_HEIGHT - PLAYER_SIZE)
        self.platforms = self.create_platforms()
        self.target_platform_idx = 0
        self.game_over = False
        self.won = False

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
                            else:
                                self.won = True
                        else:
                            self.won = True
                    elif len(target_platform.typed) >= len(target_platform.text):
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

        if self.player.y > SCREEN_HEIGHT:
            self.game_over = True

    def draw(self):
        self.screen.fill(BLACK)

        for i, platform in enumerate(self.platforms):
            color = GREEN if platform.completed else WHITE
            pygame.draw.rect(self.screen, color, platform.rect)
            
            text_surface = self.font.render(platform.text, True, BLACK)
            text_rect = text_surface.get_rect(center=(platform.x + PLATFORM_WIDTH/2, platform.y + PLATFORM_HEIGHT/2))
            self.screen.blit(text_surface, text_rect)
            
            current_idx = self.find_current_platform()
            if i == current_idx and not platform.completed:
                typed_surface = self.font.render(platform.typed, True, BLUE)
                typed_rect = typed_surface.get_rect(center=(platform.x + PLATFORM_WIDTH/2, platform.y - 25))
                self.screen.blit(typed_surface, typed_rect)

        pygame.draw.rect(self.screen, RED, self.player.rect)

        if self.game_over:
            text = self.font.render("Game Over! Press R to restart", True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))
        elif self.won:
            text = self.font.render("You Won! Press R to restart", True, WHITE)
            self.screen.blit(text, (SCREEN_WIDTH//2 - 150, SCREEN_HEIGHT//2))

        pygame.display.flip()

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_r and (self.game_over or self.won):
                        self.__init__()
                    else:
                        self.handle_input(event)

            if not self.game_over and not self.won:
                self.update()
            self.draw()
            self.clock.tick(FPS)

        pygame.quit()
        sys.exit()

if __name__ == "__main__":
    game = Game()
    game.run()