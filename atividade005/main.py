import pygame
import sys
import random
import os

# Initialize Pygame
pygame.init()
pygame.mixer.init()

# Screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
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
BROWN = (139, 69, 19)
LIGHT_BLUE = (72, 149, 239)
PURPLE = (114, 9, 183)
LIGHT_PURPLE = (181, 23, 158)
PINK = (247, 37, 133)

# Initial positions
PLAYER1_INITIAL_POS = (50, SCREEN_HEIGHT // 2)
PLAYER2_INITIAL_POS = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

# Game objects
player1 = {
    "rect": pygame.Rect(PLAYER1_INITIAL_POS[0], PLAYER1_INITIAL_POS[1], 40,
                        30),
    "color": BLUE,
    "speed": 5,
    "score": 0,
    "last_shot_time": 0,
    "shot_cooldown": 500,
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
    "shot_cooldown": 500,
    "turret_color": YELLOW,
    "direction": pygame.math.Vector2(-1, 0)
}

projectiles = []
obstacles = []

# Game state
MAX_SCORE = 5

# Obstacle Class for dynamic behaviors
class Obstacle:
    def __init__(self, rect, color, effect=None, move_direction=None, speed=2, is_circle=False):
        self.rect = rect
        self.color = color
        self.effect = effect  # Efeito no projétil ("increase", "decrease", ou None)
        self.move_direction = move_direction  # "horizontal" ou "vertical"
        self.speed = speed
        self.is_circle = is_circle  # Se for True, o obstáculo será desenhado como um círculo

    def move(self):
        central_area_x_min = SCREEN_WIDTH // 4
        central_area_x_max = 3 * SCREEN_WIDTH // 4

        if self.move_direction == "horizontal":
            self.rect.x += self.speed
            # Limitar o movimento dentro da área central
            if self.rect.right > central_area_x_max or self.rect.left < central_area_x_min:
                self.speed = -self.speed
        elif self.move_direction == "vertical":
            self.rect.y += self.speed
            # Limitar o movimento vertical nas bordas da tela
            if self.rect.bottom > SCREEN_HEIGHT or self.rect.top < 0:
                self.speed = -self.speed

    def apply_effect(self, projectile):
        if self.effect == "increase":
            projectile["speed"] = min(projectile["speed"] + 2, 15)  # Increase speed with a max cap
        elif self.effect == "decrease":
            projectile["speed"] = max(projectile["speed"] - 2, 3)  # Decrease speed with a min cap


def generate_obstacles():
    obstacles.clear()
    
    # Definir os limites da área central (área onde os obstáculos podem aparecer)
    central_area_x_min = SCREEN_WIDTH // 4
    central_area_x_max = 3 * SCREEN_WIDTH // 4

    # Gerar múltiplos obstáculos normais
    for _ in range(2):  # Número de Light Blue e Purple
        # Light Blue (aumenta velocidade) - Obstáculo fixo
        width, height = 100, 50
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), LIGHT_BLUE, effect="increase"))

        # Purple (diminui velocidade) - Obstáculo fixo
        size = 50
        x = random.randint(central_area_x_min, central_area_x_max - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        obstacles.append(Obstacle(pygame.Rect(x, y, size, size), PURPLE, effect="decrease"))

    # Gerar múltiplos obstáculos dinâmicos (movimentação)
    for _ in range(2):  # Número de Light Purple e Pink
        # Light Purple (se move horizontalmente)
        width, height = 120, 20
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), LIGHT_PURPLE, move_direction="horizontal", speed=3))

        # Pink (se move verticalmente)
        width, height = 20, 120
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), PINK, move_direction="vertical", speed=3))

    # Gerar 1 ou 2 black holes (buracos negros)
    for _ in range(random.randint(1, 2)):
        size = random.randint(40, 60)  # Tamanho do círculo
        x = random.randint(central_area_x_min, central_area_x_max - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        obstacles.append(Obstacle(pygame.Rect(x, y, size, size), BLACK, is_circle=True))  # Buraco negro é circular



# Modified draw function to include dynamic obstacles and black holes
def draw():
    screen.fill(BLACK)

    # Draw grass texture
    for y in range(0, SCREEN_HEIGHT, 20):
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.rect(screen, (0, 100, 0), (x, y, 20, 20))
            pygame.draw.rect(screen, (0, 120, 0), (x, y, 18, 18))

    # Draw obstacles
    for obstacle in obstacles:
        if obstacle.is_circle:
            # Desenhar buraco negro como círculo
            pygame.draw.circle(screen, obstacle.color, obstacle.rect.center, obstacle.rect.width // 2)
        else:
            # Desenhar os outros obstáculos como retângulos
            pygame.draw.rect(screen, obstacle.color, obstacle.rect)

    # Draw tanks
    draw_tank(screen, player1)
    draw_tank(screen, player2)

    # Draw projectiles
    for proj in projectiles:
        pygame.draw.rect(screen, proj["color"], proj["rect"])

    # Display scores
    font = pygame.font.Font(None, 36)
    score_text1 = font.render(f"P1 Score: {player1['score']}", True, WHITE)
    score_text2 = font.render(f"P2 Score: {player2['score']}", True, WHITE)
    screen.blit(score_text1, (10, 10))
    screen.blit(score_text2, (SCREEN_WIDTH - 200, 10))

    draw_boundaries()


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


def draw_boundaries():
    pygame.draw.line(screen, GRAY, (SCREEN_WIDTH // 4, 0), (SCREEN_WIDTH // 4, SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, GRAY, (3 * SCREEN_WIDTH // 4, 0), (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT), 5)


def create_projectile(x, y, direction, speed, color):
    return {
        "rect": pygame.Rect(x, y, 6, 6),
        "direction": direction,
        "speed": speed,
        "color": color
    }


# Update projectiles with obstacle effects
def update_projectiles():
    for proj in projectiles[:]:
        proj["rect"].x += proj["direction"].x * proj["speed"]
        proj["rect"].y += proj["direction"].y * proj["speed"]

        # Verificar colisões com as bordas do mapa
        if proj["rect"].left <= 0 or proj["rect"].right >= SCREEN_WIDTH:
            proj["direction"].x *= -1  # Ricochetear nas bordas horizontais
        if proj["rect"].top <= 0 or proj["rect"].bottom >= SCREEN_HEIGHT:
            proj["direction"].y *= -1  # Ricochetear nas bordas verticais

        # Verificar colisões com obstáculos
        for obstacle in obstacles:
            if proj["rect"].colliderect(obstacle.rect):
                if obstacle.is_circle and obstacle.color == BLACK:
                    # Se for um buraco negro, o projétil desaparece
                    projectiles.remove(proj)
                    break

                # Aplicar efeito de velocidade conforme o tipo de obstáculo
                obstacle.apply_effect(proj)

                # Ricochetear nos obstáculos (não ricocheteia no buraco negro)
                if not obstacle.is_circle:  # Somente ricochetear se não for buraco negro
                    if proj["rect"].right > obstacle.rect.left and proj["rect"].left < obstacle.rect.left:
                        proj["direction"].x *= -1
                    elif proj["rect"].left < obstacle.rect.right and proj["rect"].right > obstacle.rect.right:
                        proj["direction"].x *= -1
                    if proj["rect"].bottom > obstacle.rect.top and proj["rect"].top < obstacle.rect.top:
                        proj["direction"].y *= -1
                    elif proj["rect"].top < obstacle.rect.bottom and proj["rect"].bottom > obstacle.rect.bottom:
                        proj["direction"].y *= -1

                break


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


# Modified check_collisions function to include obstacles
def check_collisions():
    for proj in projectiles[:]:
        # Verificar se o projétil colide com o player 1
        if player1["rect"].colliderect(proj["rect"]) and proj["color"] != player1["color"]:
            player2["score"] += 1
            projectiles.remove(proj)
            respawn_players()
            generate_obstacles()
            countdown()
            if player2["score"] >= MAX_SCORE:
                return "Player 2 Wins!"
            break
        # Verificar se o projétil colide com o player 2
        elif player2["rect"].colliderect(proj["rect"]) and proj["color"] != player2["color"]:
            player1["score"] += 1
            projectiles.remove(proj)
            respawn_players()
            generate_obstacles()
            countdown()
            if player1["score"] >= MAX_SCORE:
                return "Player 1 Wins!"
            break

        # Verificar colisões com obstáculos
        for obstacle in obstacles:
            if proj["rect"].colliderect(obstacle.rect):
                # Aplicar o efeito de velocidade do obstáculo
                obstacle.apply_effect(proj)

                # Ricochetear nos obstáculos
                if proj["rect"].right > obstacle.rect.left and proj["rect"].left < obstacle.rect.left:
                    proj["direction"].x *= -1  # Ricochetear horizontalmente
                elif proj["rect"].left < obstacle.rect.right and proj["rect"].right > obstacle.rect.right:
                    proj["direction"].x *= -1  # Ricochetear horizontalmente
                if proj["rect"].bottom > obstacle.rect.top and proj["rect"].top < obstacle.rect.top:
                    proj["direction"].y *= -1  # Ricochetear verticalmente
                elif proj["rect"].top < obstacle.rect.bottom and proj["rect"].bottom > obstacle.rect.bottom:
                    proj["direction"].y *= -1  # Ricochetear verticalmente

                break  # Sair do loop após o ricochete


# New function for countdown
def countdown():
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        count_text = font.render(str(i), True, WHITE)
        text_rect = count_text.get_rect(
            center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(count_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)


# Modified respawn function to respawn both players
def respawn_players():
    player1["rect"].topleft = PLAYER1_INITIAL_POS
    player2["rect"].topleft = PLAYER2_INITIAL_POS
    player1["direction"] = pygame.math.Vector2(1, 0)
    player2["direction"] = pygame.math.Vector2(-1, 0)
    projectiles.clear()


# Modified move_player function to include obstacle collision
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

    # Limit movement to the nearest line
    if player == player1:
        new_rect.x = min(new_rect.x, SCREEN_WIDTH // 4 - player["rect"].width)
    elif player == player2:
        new_rect.x = max(new_rect.x, 3 * SCREEN_WIDTH // 4)

    new_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # Check collision with obstacles
    for obstacle in obstacles:
        if new_rect.colliderect(obstacle):
            new_rect = player["rect"].copy()
            break

    player["rect"] = new_rect

    if new_direction.length() > 0:
        player["direction"] = new_direction.normalize()


# Main game loop (with minor modifications)
def main_game_loop():
    clock = pygame.time.Clock()
    generate_obstacles()

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

        # Move dynamic obstacles
        for obstacle in obstacles:
            obstacle.move()

        draw()
        pygame.display.flip()
        clock.tick(60)

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
                            generate_obstacles()
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