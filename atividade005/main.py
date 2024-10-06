import pygame
import sys
import random

# Initialize Pygame
pygame.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 800, 600
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

# Initial positions
PLAYER1_INITIAL_POS = (50, SCREEN_HEIGHT // 2)
PLAYER2_INITIAL_POS = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

soundtrack_list =\
["SOUNDTRACKS/Castlevania II Music (NES) - Bloody Tears (Day Theme) - ",
"explod2A03.mp3",
"SOUNDTRACKS/phoenixwright.mp3"
 ]

soundtrack_selection = random.choice(soundtrack_list)
soundtrack = pygame.mixer.Sound(soundtrack_selection)

soundtrack.set_volume(0.3)
soundtrack.play()

# Game objects
player1 = {
    "rect": pygame.Rect(PLAYER1_INITIAL_POS[0], PLAYER1_INITIAL_POS[1], 40,
                        30),
    "color": BLUE,
    "speed": 5,
    "score": 0,
    "last_shot_time": 0,
    "shot_cooldown": 500,  # Cooldown in milliseconds
    "turret_color": NAVY_BLUE,
    "direction": pygame.math.Vector2(1, 0)
}

player2 = {
    "rect": pygame.Rect(PLAYER2_INITIAL_POS[0], PLAYER2_INITIAL_POS[1], 40,
                        30),
    "color": RED,
    "speed": 5,
    "score": 0,
    "last_shot_time": 0,
    "shot_cooldown": 500,  # Cooldown in milliseconds
    "turret_color": YELLOW,
    "direction": pygame.math.Vector2(-1, 0)
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
    pygame.draw.line(surface, tank["turret_color"], turret_origin, turret_end,
                     turret_width)


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

    new_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    if not any(barrier.colliderect(new_rect) for barrier in barriers):
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
        new_rect = proj["rect"].copy()
        new_rect.x += proj["direction"].x * proj["speed"]
        new_rect.y += proj["direction"].y * proj["speed"]

        if (new_rect.left <= 0 or new_rect.right >= SCREEN_WIDTH or
                new_rect.top <= 0 or new_rect.bottom >= SCREEN_HEIGHT or
                any(barrier.colliderect(new_rect) for barrier in barriers)):
            projectiles.remove(proj)
        else:
            proj["rect"] = new_rect


def check_collisions():
    for proj in projectiles[:]:
        if player1["rect"].colliderect(proj["rect"]) and proj["color"] != \
                player1["color"]:
            player2["score"] += 1
            projectiles.remove(proj)
            respawn_player(player1)
            if player2["score"] >= MAX_SCORE:
                return "Player 2 Wins!"
            break
        elif player2["rect"].colliderect(proj["rect"]) and proj["color"] != \
                player2["color"]:
            player1["score"] += 1
            projectiles.remove(proj)
            respawn_player(player2)
            if player1["score"] >= MAX_SCORE:
                return "Player 1 Wins!"
            break
    return None


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
    text_rect = game_over_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    instructions_text = font.render("Press R to Restart or Q to Quit", True,
                                    WHITE)
    instructions_rect = instructions_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

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

    # Draw barriers
    for barrier in barriers:
        pygame.draw.rect(screen, (100, 100, 100), barrier)
        pygame.draw.rect(screen, (150, 150, 150), barrier.inflate(-4, -4))

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


def show_start_screen():
    screen.fill(BLACK)

    font = pygame.font.Font(None, 74)
    title_text = font.render("Battle Tanks Multiplayer", True, WHITE)
    title_rect = title_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))

    instructions_text = font.render("Press Enter to Start", True, WHITE)
    instructions_rect = instructions_text.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    controls_text1 = pygame.font.Font(None, 36).render(
        "P1: WASD to move, SPACE to shoot", True, WHITE)
    controls_text2 = pygame.font.Font(None, 36).render(
        "P2: Arrow keys to move, ENTER to shoot", True, WHITE)
    controls_rect1 = controls_text1.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 80))
    controls_rect2 = controls_text2.get_rect(
        center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 120))

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
                    if current_time - player1["last_shot_time"] >= player1[
                        "shot_cooldown"]:
                        projectiles.append(
                            create_projectile(player1["rect"].centerx,
                                              player1["rect"].centery,
                                              player1["direction"], 7, BLUE))
                        player1["last_shot_time"] = current_time
                        player1["turret_color"] = RED
                elif event.key == pygame.K_RETURN:
                    if current_time - player2["last_shot_time"] >= player2[
                        "shot_cooldown"]:
                        projectiles.append(
                            create_projectile(player2["rect"].centerx,
                                              player2["rect"].centery,
                                              player2["direction"], 7, RED))
                        player2["last_shot_time"] = current_time
                        player2["turret_color"] = YELLOW

        if current_time - player1["last_shot_time"] >= player1[
            "shot_cooldown"]:
            player1["turret_color"] = NAVY_BLUE
        if current_time - player2["last_shot_time"] >= player2[
            "shot_cooldown"]:
            player2["turret_color"] = YELLOW

        keys = pygame.key.get_pressed()
        move_player(player1, keys, pygame.K_w, pygame.K_s, pygame.K_a,
                    pygame.K_d)
        move_player(player2, keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT,
                    pygame.K_RIGHT)
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