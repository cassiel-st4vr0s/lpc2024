import pygame
import sys
import random
import os

# initialize Pygame
pygame.init()
pygame.mixer.init()

# screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Battle Tanks Multiplayer")

# colors
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

# initial positions
PLAYER1_INITIAL_POS = (50, SCREEN_HEIGHT // 2)
PLAYER2_INITIAL_POS = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

# game objects
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

# obstacle class for dynamic behaviors
class Obstacle:
    def __init__(self, rect, color, effect=None, move_direction=None, speed=2, is_circle=False):
        self.rect = rect
        self.color = color
        self.effect = effect  # effect on the projectile ("increase", "decrease", or None)
        self.move_direction = move_direction  # "horizontal" or "vertical"
        self.speed = speed
        self.is_circle = is_circle  # if True, the obstacle will be a circle

    def move(self):
        central_area_x_min = SCREEN_WIDTH // 4
        central_area_x_max = 3 * SCREEN_WIDTH // 4

        if self.move_direction == "horizontal":
            self.rect.x += self.speed
            # limit the movement inside the central area
            if self.rect.right > central_area_x_max or self.rect.left < central_area_x_min:
                self.speed = -self.speed
        elif self.move_direction == "vertical":
            self.rect.y += self.speed
            # limit the moviment on the edges of the screen
            if self.rect.bottom > SCREEN_HEIGHT or self.rect.top < 0:
                self.speed = -self.speed

    def apply_effect(self, projectile):
        if self.effect == "increase":
            projectile["speed"] = min(projectile["speed"] + 2, 15)  # increase speed with a max cap
        elif self.effect == "decrease":
            projectile["speed"] = max(projectile["speed"] - 2, 3)  # decrease speed with a min cap


def generate_obstacles():
    obstacles.clear()
    
    # define the limits of the central area (area where obstacles can appear)
    central_area_x_min = SCREEN_WIDTH // 4
    central_area_x_max = 3 * SCREEN_WIDTH // 4

    # generate multiple normal obstacles
    for _ in range(2):  # numbers of light blue and purple
        # light Blue (increases speed) - fixed obstacle
        width, height = 100, 50
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), LIGHT_BLUE, effect="increase"))

        # purple (decreases speed) - fixed obstacle
        size = 50
        x = random.randint(central_area_x_min, central_area_x_max - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        obstacles.append(Obstacle(pygame.Rect(x, y, size, size), PURPLE, effect="decrease"))

    # generate multiple dynamic obstacles (movement)
    for _ in range(2):  # numbers of light purple and pink
        # light Purple (moves horizontally)
        width, height = 120, 20
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), LIGHT_PURPLE, move_direction="horizontal", speed=3))

        # pink (moves vertically)
        width, height = 20, 120
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), PINK, move_direction="vertical", speed=3))

    # generate 1 or 2 black holes
    for _ in range(random.randint(1, 2)):
        size = random.randint(40, 60)  # size of the circle
        x = random.randint(central_area_x_min, central_area_x_max - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        obstacles.append(Obstacle(pygame.Rect(x, y, size, size), BLACK, is_circle=True))  # Buraco negro é circular


# modified draw function to include dynamic obstacles and black holes
def draw():
    screen.fill(BLACK)

    # draw grass texture
    for y in range(0, SCREEN_HEIGHT, 20):
        for x in range(0, SCREEN_WIDTH, 20):
            pygame.draw.rect(screen, (0, 100, 0), (x, y, 20, 20))
            pygame.draw.rect(screen, (0, 120, 0), (x, y, 18, 18))

    # draw obstacles
    for obstacle in obstacles:
        if obstacle.is_circle:
            # draw black hole as circle
            pygame.draw.circle(screen, obstacle.color, obstacle.rect.center, obstacle.rect.width // 2)
        else:
            # draw the other obstacles as rectangles
            pygame.draw.rect(screen, obstacle.color, obstacle.rect)

    # draw tanks
    draw_tank(screen, player1)
    draw_tank(screen, player2)

    # draw projectiles
    for proj in projectiles:
        pygame.draw.rect(screen, proj["color"], proj["rect"])

    # display scores
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


# update projectiles with obstacle effects
def update_projectiles():
    for proj in projectiles[:]:
        proj["rect"].x += proj["direction"].x * proj["speed"]
        proj["rect"].y += proj["direction"].y * proj["speed"]

        # check for collisions with map edges
        if proj["rect"].left <= 0 or proj["rect"].right >= SCREEN_WIDTH:
            proj["direction"].x *= -1  # Ricochetear nas bordas horizontais
        if proj["rect"].top <= 0 or proj["rect"].bottom >= SCREEN_HEIGHT:
            proj["direction"].y *= -1  # Ricochetear nas bordas verticais

        # check for collisions with obstacles
        for obstacle in obstacles:
            if proj["rect"].colliderect(obstacle.rect):
                if obstacle.is_circle and obstacle.color == BLACK:
                    # if it's a black hole, the projectile disappears
                    projectiles.remove(proj)
                    break

                # apply speed effect depending on the type of obstacle
                obstacle.apply_effect(proj)

                # ricochet off obstacles
                if not obstacle.is_circle:  # only ricochet if it's not a black hole
                    if proj["rect"].centerx < obstacle.rect.left:
                        proj["direction"].x = abs(proj["direction"].x)  # rebound to the right
                    elif proj["rect"].centerx > obstacle.rect.right:
                        proj["direction"].x = -abs(proj["direction"].x)  # rebound to the left
                    if proj["rect"].centery < obstacle.rect.top:
                        proj["direction"].y = abs(proj["direction"].y)  # rebound down
                    elif proj["rect"].centery > obstacle.rect.bottom:
                        proj["direction"].y = -abs(proj["direction"].y)  # rebound up

                break
  # exit loop after ricochet


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


# modified check_collisions function to include obstacles
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
        # check if the projectile collides with player 2
        elif player2["rect"].colliderect(proj["rect"]) and proj["color"] != player2["color"]:
            player1["score"] += 1
            projectiles.remove(proj)
            respawn_players()
            generate_obstacles()
            countdown()
            if player1["score"] >= MAX_SCORE:
                return "Player 1 Wins!"
            break

        # check for collisions with obstacles
        for obstacle in obstacles:
            if proj["rect"].colliderect(obstacle.rect):
                # apply the obstacle speed effect
                obstacle.apply_effect(proj)

                # ricochet off obstacles
                if proj["rect"].right > obstacle.rect.left and proj["rect"].left < obstacle.rect.left:
                    proj["direction"].x *= -1  # ricochet horizontally
                elif proj["rect"].left < obstacle.rect.right and proj["rect"].right > obstacle.rect.right:
                    proj["direction"].x *= -1  # ricochet horizontally
                if proj["rect"].bottom > obstacle.rect.top and proj["rect"].top < obstacle.rect.top:
                    proj["direction"].y *= -1  # ricochet vertically
                elif proj["rect"].top < obstacle.rect.bottom and proj["rect"].bottom > obstacle.rect.bottom:
                    proj["direction"].y *= -1  # ricochet vertically

                break  # exit loop after ricochet


# new function for countdown
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


# modified respawn function to respawn both players
def respawn_players():
    player1["rect"].topleft = PLAYER1_INITIAL_POS
    player2["rect"].topleft = PLAYER2_INITIAL_POS
    player1["direction"] = pygame.math.Vector2(1, 0)
    player2["direction"] = pygame.math.Vector2(-1, 0)
    projectiles.clear()


# modified move_player function to include obstacle collision
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

    # limit movement to the nearest line
    if player == player1:
        new_rect.x = min(new_rect.x, SCREEN_WIDTH // 4 - player["rect"].width)
    elif player == player2:
        new_rect.x = max(new_rect.x, 3 * SCREEN_WIDTH // 4)

    new_rect.clamp_ip(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    # check collision with obstacles
    for obstacle in obstacles:
        if new_rect.colliderect(obstacle):
            new_rect = player["rect"].copy()
            break

    player["rect"] = new_rect

    if new_direction.length() > 0:
        player["direction"] = new_direction.normalize()


# main game loop (with minor modifications)
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

        # move dynamic obstacles
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

# run the game
show_start_screen()
main_game_loop()