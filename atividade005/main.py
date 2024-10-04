import pygame
import sys
import time
import random

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle Tanks")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)

# Initial positions
PLAYER_INITIAL_POS = (50, SCREEN_HEIGHT // 2)
ENEMY_INITIAL_POS = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

# Game objects
player = {
    "rect": pygame.Rect(PLAYER_INITIAL_POS[0], PLAYER_INITIAL_POS[1], 40, 30),
    "color": BLUE,
    "speed": 5,
    "health": 3,
    "last_shot_time": 0,
    "shot_cooldown": 500  # Cooldown in milliseconds
}

enemy = {
    "rect": pygame.Rect(ENEMY_INITIAL_POS[0], ENEMY_INITIAL_POS[1], 40, 30),
    "color": RED,
    "speed": 0,
    "fire_rate": 2000,
    "lifetime": 10000,  # Enemy lifetime in milliseconds (10 seconds)
    "last_shot_time": 0,
    "shot_cooldown": 1000  # Cooldown in milliseconds
}

# Updated barrier design
barriers = [
    pygame.Rect(150, SCREEN_HEIGHT // 2 - 100, 40, 200),
    pygame.Rect(SCREEN_WIDTH - 190, SCREEN_HEIGHT // 2 - 100, 40, 200),
    pygame.Rect(SCREEN_WIDTH // 2 - 100, 100, 200, 40),
    pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT - 140, 200, 40)
]

projectiles = []

# Game state
level = 1
game_over = False
level_start_time = 0
level_pause_duration = 3000  # 3 seconds pause between levels


# Helper functions
def draw_tank(surface, tank, turret_angle=0):
    pygame.draw.rect(surface, tank["color"], tank["rect"])
    turret_length = 20
    turret_width = 6
    turret_origin = tank["rect"].center
    turret_end = (
        turret_origin[0] + turret_length * pygame.math.Vector2(1, 0).rotate(
            turret_angle).x,
        turret_origin[1] + turret_length * pygame.math.Vector2(1, 0).rotate(
            turret_angle).y
    )
    pygame.draw.line(surface, tank["color"], turret_origin, turret_end,
                     turret_width)


def move_player(keys):
    new_rect = player["rect"].copy()
    if keys[pygame.K_LEFT]:
        new_rect.x -= player["speed"]
    if keys[pygame.K_RIGHT]:
        new_rect.x += player["speed"]
    if keys[pygame.K_UP]:
        new_rect.y -= player["speed"]
    if keys[pygame.K_DOWN]:
        new_rect.y += player["speed"]

    new_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    if not any(barrier.colliderect(new_rect) for barrier in barriers):
        player["rect"] = new_rect


def move_enemy():
    if level >= 2:
        new_rect = enemy["rect"].copy()
        new_rect.y += enemy["speed"]
        if new_rect.top <= 0 or new_rect.bottom >= SCREEN_HEIGHT:
            enemy["speed"] *= -1
        elif not any(barrier.colliderect(new_rect) for barrier in barriers):
            enemy["rect"] = new_rect


def create_projectile(x, y, direction, speed, color):
    return {
        "rect": pygame.Rect(x, y, 6, 6),
        "direction": direction,
        "speed": speed,
        "color": color
    }


def update_projectiles():
    for proj in projectiles[:]:
        new_rect = proj["rect"].copy()
        new_rect.x += proj["direction"][0] * proj["speed"]
        new_rect.y += proj["direction"][1] * proj["speed"]

        if (new_rect.left <= 0 or new_rect.right >= SCREEN_WIDTH or
                new_rect.top <= 0 or new_rect.bottom >= SCREEN_HEIGHT or
                any(barrier.colliderect(new_rect) for barrier in barriers)):
            projectiles.remove(proj)
        else:
            proj["rect"] = new_rect


def check_collisions():
    global game_over, level_up_called
    for proj in projectiles[:]:
        # Verifica se o projétil vermelho (inimigo) atinge o jogador
        if proj["color"] == RED and player["rect"].colliderect(proj["rect"]):
            player["health"] -= 1
            projectiles.remove(proj)
            if player["health"] <= 0:
                game_over = True
            break

        # Checks if the blue projectile (player) hits the enemy
        elif proj["color"] == BLUE and enemy["rect"].colliderect(proj["rect"]):
            if not level_up_called:
                print(f"Enemy hit! Leveling up from level {level}.")
                level_up()
                level_up_called = True
            projectiles.remove(proj)
            break
    else:
        level_up_called = False  # Reset if no collision occurred


def level_up():
    global level, enemy, level_start_time
    level += 1
    level_start_time = pygame.time.get_ticks()

    if level > 5:
        print("Congratulations! You've beaten all levels!")
        pygame.quit()
        sys.exit()

    # Reset player and enemy positions
    player["rect"].topleft = PLAYER_INITIAL_POS
    enemy["rect"].topleft = ENEMY_INITIAL_POS

    enemy["lifetime"] = max(5000, 10000 - (level - 1) * 1000)  # Diminui a vida útil a cada nível
    if level == 2:
        enemy["speed"] = 2
    elif level == 3:
        enemy["fire_rate"] = 1500
    elif level == 4:
        enemy["speed"] = 3
    elif level == 5:
        enemy["fire_rate"] = 1000

    # Removes the timer for the enemy death event
    pygame.time.set_timer(enemy_die_event, 0)


def draw():
    screen.fill(BLACK)

    # Draw grass texture
    for y in range(0, SCREEN_HEIGHT, 20):
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.rect(screen, (0, 100, 0), (x, y, 20, 20))
            pygame.draw.rect(screen, (0, 120, 0), (x, y, 18, 18))

    # Draw barriers
    for barrier in barriers:
        pygame.draw.rect(screen, (100, 100, 100), barrier)
        pygame.draw.rect(screen, (150, 150, 150), barrier.inflate(-4, -4))

    # Draw tanks
    mouse_x, mouse_y = pygame.mouse.get_pos()
    player_angle = pygame.math.Vector2(mouse_x - player["rect"].centerx,
                                       mouse_y - player[
                                           "rect"].centery).angle_to((1, 0))
    draw_tank(screen, player, player_angle)
    draw_tank(screen, enemy, 180)

    for proj in projectiles:
        pygame.draw.rect(screen, proj["color"], proj["rect"])

    font = pygame.font.Font(None, 36)
    health_text = font.render(f"Health: {player['health']}", True, WHITE)
    level_text = font.render(f"Level: {level}", True, WHITE)
    screen.blit(health_text, (10, 10))
    screen.blit(level_text, (SCREEN_WIDTH - 100, 10))

    current_time = pygame.time.get_ticks()
    if current_time - level_start_time < level_pause_duration:
        pause_text = font.render(f"Level {level}", True, WHITE)
        text_rect = pause_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(pause_text, text_rect)


# Game loop
clock = pygame.time.Clock()
enemy_fire_event = pygame.USEREVENT + 1
enemy_die_event = pygame.USEREVENT + 2
pygame.time.set_timer(enemy_fire_event, enemy["fire_rate"])
level_start_time = pygame.time.get_ticks()

while not game_over:
    current_time = pygame.time.get_ticks()
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if current_time - player["last_shot_time"] >= player[
                "shot_cooldown"]:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                dx, dy = mouse_x - player["rect"].centerx, mouse_y - player[
                    "rect"].centery
                direction = pygame.math.Vector2(dx, dy).normalize()
                projectiles.append(create_projectile(player["rect"].centerx,
                                                     player["rect"].centery,
                                                     direction, 7, BLUE))
                player["last_shot_time"] = current_time
        elif event.type == enemy_fire_event:
            if current_time - enemy["last_shot_time"] >= enemy[
                "shot_cooldown"]:
                direction = pygame.math.Vector2(-1, 0)
                projectiles.append(create_projectile(enemy["rect"].centerx,
                                                     enemy["rect"].centery,
                                                     direction,
                                                     5 if level > 2 else 3,
                                                     RED))
                enemy["last_shot_time"] = current_time
        elif event.type == enemy_die_event:
            level_up()

    if current_time - level_start_time >= level_pause_duration:
        keys = pygame.key.get_pressed()
        move_player(keys)
        move_enemy()
        update_projectiles()
        check_collisions()

    draw()
    pygame.display.flip()
    clock.tick(60)

print("Game Over!")
pygame.quit()
sys.exit()