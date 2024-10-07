import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600  # Aumentado para 1200 pixels de largura
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle Tanks Multiplayer")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
NAVY_BLUE = (21, 52, 72)
GRAY = (128, 128, 128)

# Initial positions
PLAYER1_INITIAL_POS = (50, SCREEN_HEIGHT // 2)
PLAYER2_INITIAL_POS = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

# Sound setup (keeping this part for future use if needed)
soundtracks_dir = os.path.join(os.getcwd(), "SOUNDTRACKS")
soundtrack_list = [
    os.path.join(soundtracks_dir, "Castlevania II Music (NES) - Bloody Tears (Day Theme).wav"),
    os.path.join(soundtracks_dir, "explod2A03.wav"),
    os.path.join(soundtracks_dir, "phoenixwright.wav")
]

# Game objects
player1 = {
    "rect": pygame.Rect(PLAYER1_INITIAL_POS[0], PLAYER1_INITIAL_POS[1], 40, 30),
    "color": BLUE,
    "speed": 5,
    "score": 0,
    "last_shot_time": 0,
    "shot_cooldown": 500,  # Cooldown in milliseconds
    "turret_color": NAVY_BLUE,
    "direction": pygame.math.Vector2(1, 0)
}

player2 = {
    "rect": pygame.Rect(PLAYER2_INITIAL_POS[0], PLAYER2_INITIAL_POS[1], 40, 30),
    "color": RED,
    "speed": 5,
    "score": 0,
    "last_shot_time": 0,
    "shot_cooldown": 500,  # Cooldown in milliseconds
    "turret_color": YELLOW,
    "direction": pygame.math.Vector2(-1, 0)
}

projectiles = []

# Game state
MAX_SCORE = 5  # Game ends when a player reaches this score

# Helper functions
def draw_tank(surface, tank):
    pygame.draw.rect(surface, tank["color"], tank["rect"])
    turret_length = 30
    turret_width = 8
    turret_origin = tank["rect"].center
    turret_end = (
        turret_origin[0] + turret_length * tank["direction"].x,
        turret_origin[1] + turret_length * tank["direction"].y
    )
    pygame.draw.line(surface, tank["turret_color"], turret_origin, turret_end, turret_width)

def move_player(player, keys, up, down, left, right):
    new_rect = player["rect"].copy()
    new_direction = pygame.math.Vector2(0, 0)

    if keys[left]:
        new_rect.x -= player["speed"]
        new_direction.x = -1
    if keys[right]:
        new_rect.x += player["speed"]
        new_direction.x = 1
    if keys[up]:
        new_rect.y -= player["speed"]
        new_direction.y = -1
    if keys[down]:
        new_rect.y += player["speed"]
        new_direction.y = 1

    # Limitar movimento até a linha mais próxima
    if player == player1:
        new_rect.x = min(new_rect.x, SCREEN_WIDTH // 4 - player["rect"].width)  # Limite à esquerda
    elif player == player2:
        new_rect.x = max(new_rect.x, 3 * SCREEN_WIDTH // 4)  # Limite à direita

    new_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))
    player["rect"] = new_rect

    if new_direction.length() > 0:
        player["direction"] = new_direction.normalize()

def create_projectile(x, y, direction, speed, color):
    return {
        "rect": pygame.Rect(x, y, 6, 6),
        "direction": direction,
        "speed": speed,
        "color": color
    }

def update_projectiles():
    for proj in projectiles[:]:
        proj["rect"].x += proj["direction"].x * proj["speed"]
        proj["rect"].y += proj["direction"].y * proj["speed"]

        # Rebater nas bordas
        if proj["rect"].left <= 0 or proj["rect"].right >= SCREEN_WIDTH:
            proj["direction"].x *= -1  # Inverte a direção horizontal
        if proj["rect"].top <= 0 or proj["rect"].bottom >= SCREEN_HEIGHT:
            proj["direction"].y *= -1  # Inverte a direção vertical

def check_collisions():
    for proj in projectiles[:]:
        if player1["rect"].colliderect(proj["rect"]) and proj["color"] != player1["color"]:
            player2["score"] += 1
            projectiles.remove(proj)
            respawn_player(player1)
            if player2["score"] >= MAX_SCORE:
                return "Player 2 Wins!"
            break
        elif player2["rect"].colliderect(proj["rect"]) and proj["color"] != player2["color"]:
            player1["score"] += 1
            projectiles.remove(proj)
            respawn_player(player2)
            if player1["score"] >= MAX_SCORE:
                return "Player 1 Wins!"
            break
    return None

def draw_boundaries():
    # Draw sector boundaries
    pygame.draw.line(screen, GRAY, (SCREEN_WIDTH // 4, 0), (SCREEN_WIDTH // 4, SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, GRAY, (3 * SCREEN_WIDTH // 4, 0), (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT), 5)

def respawn_player(player):
    if player == player1:
        player["rect"].topleft = PLAYER1_INITIAL_POS
        player["direction"] = pygame.math.Vector2(1, 0)
    else:
        player["rect"].topleft = PLAYER2_INITIAL_POS
        player["direction"] = pygame.math.Vector2(-1, 0)

def show_game_over_screen(message):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 74)
    game_over_text = font.render(message, True, WHITE)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    instructions_text = font.render("Press R to Restart or Q to Quit", True, WHITE)
    instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

    screen.blit(game_over_text, text_rect)
    screen.blit(instructions_text, instructions_rect)

    pygame.display.flip()

def reset_game():
    global player1, player2, projectiles
    player1["rect"].topleft = PLAYER1_INITIAL_POS
    player2["rect"].topleft = PLAYER2_INITIAL_POS
    player1["score"] = 0
    player2["score"] = 0
    player1["direction"] = pygame.math.Vector2(1, 0)
    player2["direction"] = pygame.math.Vector2(-1, 0)
    projectiles.clear()

def draw():
    screen.fill(BLACK)

    # Draw grass texture
    for y in range(0, SCREEN_HEIGHT, 20):
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.rect(screen, (0, 100, 0), (x, y, 20, 20))
            pygame.draw.rect(screen, (0, 120, 0), (x, y, 18, 18))

    # Draw tanks
    draw_tank(screen, player1)
    draw_tank(screen, player2)

    for proj in projectiles:
        pygame.draw.rect(screen, proj["color"], proj["rect"])

    font = pygame.font.Font(None, 36)
    score_text1 = font.render(f"P1 Score: {player1['score']}", True, WHITE)
    score_text2 = font.render(f"P2 Score: {player2['score']}", True, WHITE)
    screen.blit(score_text1, (10, 10))
    screen.blit(score_text2, (SCREEN_WIDTH - 200, 10))

    draw_boundaries()

def show_start_screen():
    screen.fill(BLACK)

    font = pygame.font.Font(None, 74)
    title_text = font.render("Battle Tanks Multiplayer", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))

    instructions_text = font.render("Press Enter to Start", True, WHITE)
    instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    controls_text1 = pygame.font.Font(None, 36).render("P1: WASD to move, SPACE to shoot", True, WHITE)
    controls_text2 = pygame.font.Font(None, 36).render("P2: Arrow keys to move, ENTER to shoot", True, WHITE)
    controls_rect1 = controls_text1.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
    controls_rect2 = controls_text2.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))

    screen.blit(title_text, title_rect)
    screen.blit(instructions_text, instructions_rect)
    screen.blit(controls_text1, controls_rect1)
    screen.blit(controls_text2, controls_rect2)

    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    waiting = False

# Main game loop
def main_game_loop():
    clock = pygame.time.Clock()
    game_over = False

    while True:
        current_time = pygame.time.get_ticks()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    if current_time - player1["last_shot_time"] >= player1["shot_cooldown"]:
                        projectiles.append(create_projectile(player1["rect"].centerx, player1["rect"].centery, player1["direction"], 7, BLUE))
                        player1["last_shot_time"] = current_time
                        player1["turret_color"] = RED
                elif event.key == pygame.K_RETURN:
                    if current_time - player2["last_shot_time"] >= player2["shot_cooldown"]:
                        projectiles.append(create_projectile(player2["rect"].centerx, player2["rect"].centery, player2["direction"], 7, RED))
                        player2["last_shot_time"] = current_time
                        player2["turret_color"] = YELLOW

        if current_time - player1["last_shot_time"] >= player1["shot_cooldown"]:
            player1["turret_color"] = NAVY_BLUE
        if current_time - player2["last_shot_time"] >= player2["shot_cooldown"]:
            player2["turret_color"] = YELLOW

        keys = pygame.key.get_pressed()
        move_player(player1, keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        move_player(player2, keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        update_projectiles()

        game_over_message = check_collisions()
        if game_over_message:
            show_game_over_screen(game_over_message)
            waiting_for_restart = True
            while waiting_for_restart:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    if event.type == pygame.KEYDOWN:
                        if event.key == pygame.K_r:
                            reset_game()
                            waiting_for_restart = False
                        elif event.key == pygame.K_q:
                            pygame.quit()
                            sys.exit()

        draw()
        pygame.display.flip()
        clock.tick(60)

# Run the game
show_start_screen()
main_game_loop()
