import pygame
import sys
import random

# initialize pygame and mixer
pygame.init()
pygame.mixer.init()

# load audio files
menu_music = pygame.mixer.Sound("SOUNDTRACKS/Castlevania II Music (NES) - Bloody Tears (Day Theme) - explod2A03.mp3")
gameplay_music = pygame.mixer.Sound("SOUNDTRACKS/phoenixwright_[cut_89sec].mp3")
gameplay_music.set_volume(0.4)
explosion_sound = pygame.mixer.Sound("assets/áudios/explosão.mp3")
bounce_sound_effect = pygame.mixer.Sound("assets/áudios/bounce.wav")
bounce_sound_effect.set_volume(0.2)
game_over_sound = pygame.mixer.Sound("SOUNDTRACKS/Victory Sound Effect.mp3")
game_over_sound.set_volume(0.5)

# screen setup
SCREEN_WIDTH, SCREEN_HEIGHT = 1200, 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("space battle multiplayer")

# load and scale background image
background_image = pygame.image.load("assets/imagens/spce.png")
background_image = pygame.transform.scale(background_image, (SCREEN_WIDTH, SCREEN_HEIGHT))

# load and rotate ship images for both players
ship_image_p1 = pygame.image.load("assets/imagens/yblueship.png")
ship_image_p2 = pygame.image.load("assets/imagens/yredship.png")

ship_image_p1 = pygame.transform.scale(ship_image_p1, (40, 30))
ship_image_p2 = pygame.transform.scale(ship_image_p2, (40, 30))

ship_image_p1 = pygame.transform.rotate(ship_image_p1, -90)  # rotate clockwise
ship_image_p2 = pygame.transform.rotate(ship_image_p2, 90)  # rotate clockwise

# colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)
BROWN = (139, 69, 19)
LIGHT_BLUE = (72, 149, 239)
PURPLE = (114, 9, 183)
LIGHT_PURPLE = (181, 23, 158)
PINK = (247, 37, 133)

# initial positions
PLAYER1_INITIAL_POS = (50, SCREEN_HEIGHT // 2)
PLAYER2_INITIAL_POS = (SCREEN_WIDTH - 100, SCREEN_HEIGHT // 2)

# player setup
player1 = {
    "rect": pygame.Rect(PLAYER1_INITIAL_POS[0], PLAYER1_INITIAL_POS[1], 40, 30),
    "color": BLUE,
    "speed": 5,
    "score": 0,
    "last_shot_time": 0,
    "shot_cooldown": 500,
    "direction": pygame.math.Vector2(1, 0)
}

player2 = {
    "rect": pygame.Rect(PLAYER2_INITIAL_POS[0], PLAYER2_INITIAL_POS[1], 40, 30),
    "color": RED,
    "speed": 5,
    "score": 0,
    "last_shot_time": 0,
    "shot_cooldown": 500,
    "direction": pygame.math.Vector2(-1, 0)
}

projectiles = []
obstacles = []

# game state
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
            # limit movement to central area
            if self.rect.right > central_area_x_max or self.rect.left < central_area_x_min:
                self.speed = -self.speed
        elif self.move_direction == "vertical":
            self.rect.y += self.speed
            # limit movement to screen edges
            if self.rect.bottom > SCREEN_HEIGHT or self.rect.top < 0:
                self.speed = -self.speed

    def apply_effect(self, projectile):
        if self.effect == "increase":
            projectile["speed"] = min(projectile["speed"] + 2, 15)  # increase speed with a max cap
        elif self.effect == "decrease":
            projectile["speed"] = max(projectile["speed"] - 2, 3)  # decrease speed with a min cap


def generate_obstacles():
    obstacles.clear()

    # define the limits of the central area (where obstacles can appear)
    central_area_x_min = SCREEN_WIDTH // 4
    central_area_x_max = 3 * SCREEN_WIDTH // 4

    # generate fixed obstacles (light blue increases speed, purple decreases)
    for _ in range(2):
        width, height = 100, 50
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), LIGHT_BLUE, effect="increase"))

        size = 50
        x = random.randint(central_area_x_min, central_area_x_max - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        obstacles.append(Obstacle(pygame.Rect(x, y, size, size), PURPLE, effect="decrease"))

    # generate dynamic obstacles (light purple moves horizontally, pink vertically)
    for _ in range(2):
        width, height = 120, 20
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), LIGHT_PURPLE, move_direction="horizontal", speed=3))

        width, height = 20, 120
        x = random.randint(central_area_x_min, central_area_x_max - width)
        y = random.randint(0, SCREEN_HEIGHT - height)
        obstacles.append(Obstacle(pygame.Rect(x, y, width, height), PINK, move_direction="vertical", speed=3))

    # generate black holes (circular obstacles)
    for _ in range(random.randint(1, 2)):
        size = random.randint(40, 60)
        x = random.randint(central_area_x_min, central_area_x_max - size)
        y = random.randint(0, SCREEN_HEIGHT - size)
        obstacles.append(Obstacle(pygame.Rect(x, y, size, size), BLACK, is_circle=True))


# draw game elements, including dynamic obstacles
def draw():
    screen.blit(background_image, (0, 0))

    # draw obstacles
    for obstacle in obstacles:
        if obstacle.is_circle:
            pygame.draw.circle(screen, obstacle.color, obstacle.rect.center, obstacle.rect.width // 2)
        else:
            pygame.draw.rect(screen, obstacle.color, obstacle.rect)

    # draw player ships
    draw_ship(screen, player1, ship_image_p1)
    draw_ship(screen, player2, ship_image_p2)

    # draw projectiles
    for proj in projectiles:
        pygame.draw.rect(screen, proj["color"], proj["rect"])

    # display scores
    font = pygame.font.Font(None, 36)
    score_text1 = font.render(f"p1 score: {player1['score']}", True, WHITE)
    score_text2 = font.render(f"p2 score: {player2['score']}", True, WHITE)
    screen.blit(score_text1, (10, 10))
    screen.blit(score_text2, (SCREEN_WIDTH - 200, 10))

    draw_boundaries()


# draw individual ships
def draw_ship(surface, tank, tank_image):
    surface.blit(tank_image, tank["rect"].topleft)

# draw screen boundaries
def draw_boundaries():
    pygame.draw.line(screen, GRAY, (SCREEN_WIDTH // 4, 0), (SCREEN_WIDTH // 4, SCREEN_HEIGHT), 5)
    pygame.draw.line(screen, GRAY, (3 * SCREEN_WIDTH // 4, 0), (3 * SCREEN_WIDTH // 4, SCREEN_HEIGHT), 5)


# create projectiles
def create_projectile(x, y, direction, speed, color):
    return {
        "rect": pygame.Rect(x, y, 6, 6),
        "direction": direction,
        "speed": speed,
        "color": color,
        "creation_time": pygame.time.get_ticks()
    }

# update projectiles, handling collisions with obstacles and boundaries
def update_projectiles():
    current_time = pygame.time.get_ticks()
    for proj in projectiles[:]:
        if current_time - proj["creation_time"] > 8000:  # lifetime of 8 seconds
            projectiles.remove(proj)
            continue

        old_pos = proj["rect"].copy()
        proj["rect"].x += proj["direction"].x * proj["speed"]
        proj["rect"].y += proj["direction"].y * proj["speed"]

        # check for collisions with map edges
        if proj["rect"].left <= 0 or proj["rect"].right >= SCREEN_WIDTH:
            proj["direction"].x *= -1
            proj["rect"].x = old_pos.x
            bounce_sound_effect.play()
        if proj["rect"].top <= 0 or proj["rect"].bottom >= SCREEN_HEIGHT:
            proj["direction"].y *= -1
            proj["rect"].y = old_pos.y
            bounce_sound_effect.play()

        # check for collisions with obstacles
        for obstacle in obstacles:
            if proj["rect"].colliderect(obstacle.rect):
                if obstacle.is_circle and obstacle.color == BLACK:
                    projectiles.remove(proj)
                    break

                obstacle.apply_effect(proj)

                # determine collision side and adjust position
                dx = proj["rect"].centerx - obstacle.rect.centerx
                dy = proj["rect"].centery - obstacle.rect.centery

                if abs(dx) > abs(dy):
                    proj["direction"].x *= -1
                    if dx > 0:
                        proj["rect"].left = obstacle.rect.right
                    else:
                        proj["rect"].right = obstacle.rect.left
                else:
                    proj["direction"].y *= -1
                    if dy > 0:
                        proj["rect"].top = obstacle.rect.bottom
                    else:
                        proj["rect"].bottom = obstacle.rect.top

                bounce_sound_effect.play()
                break


# display the game over screen
def show_game_over_screen(message):
    screen.fill(BLACK)
    game_over_sound.play()
    font = pygame.font.Font(None, 74)
    game_over_text = font.render(message, True, WHITE)
    text_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 20))
    instructions_text = font.render("press r to restart or q to quit", True, WHITE)
    instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 40))

    screen.blit(game_over_text, text_rect)
    screen.blit(instructions_text, instructions_rect)

    pygame.display.flip()


# reset game state
def reset_game():
    global player1, player2, projectiles
    gameplay_music.play()
    player1["rect"].topleft = PLAYER1_INITIAL_POS
    player2["rect"].topleft = PLAYER2_INITIAL_POS
    player1["score"] = 0
    player2["score"] = 0
    player1["direction"] = pygame.math.Vector2(1, 0)
    player2["direction"] = pygame.math.Vector2(-1, 0)
    projectiles.clear()


# start screen display
def show_start_screen():
    screen.fill(BLACK)
    menu_music.play()

    font = pygame.font.Font(None, 74)
    title_text = font.render("space battle multiplayer", True, WHITE)
    title_rect = title_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 40))

    instructions_text = font.render("press enter to start", True, WHITE)
    instructions_rect = instructions_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    controls_text1 = pygame.font.Font(None, 36).render("p1: wasd to move, space to shoot", True, WHITE)
    controls_text2 = pygame.font.Font(None, 36).render("p2: arrow keys to move, enter to shoot", True, WHITE)
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
                    menu_music.stop()
                    gameplay_music.play(-1)


# handle collisions in the game
def check_collisions():
    for proj in projectiles[:]:
        if player1["rect"].colliderect(proj["rect"]) and proj["color"] != player1["color"]:
            player2["score"] += 1
            projectiles.remove(proj)
            explosion_sound.play()
            respawn_players()
            generate_obstacles()
            countdown()
            if player2["score"] >= MAX_SCORE:
                return "player 2 wins!"
        elif player2["rect"].colliderect(proj["rect"]) and proj["color"] != player2["color"]:
            player1["score"] += 1
            projectiles.remove(proj)
            explosion_sound.play()
            respawn_players()
            generate_obstacles()
            countdown()
            if player1["score"] >= MAX_SCORE:
                return "player 1 wins!"

    return None


# move player and handle obstacle collisions
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

    # check collision with obstacles
    collision = False
    for obstacle in obstacles:
        if new_rect.colliderect(obstacle.rect):
            collision = True
            break

    if not collision:
        player["rect"] = new_rect.clamp(pygame.Rect(0, 0, SCREEN_WIDTH, SCREEN_HEIGHT))

    if new_direction.length() > 0:
        player["direction"] = new_direction.normalize()


# countdown timer for game reset
def countdown():
    font = pygame.font.Font(None, 74)
    for i in range(3, 0, -1):
        screen.fill(BLACK)
        count_text = font.render(str(i), True, WHITE)
        text_rect = count_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
        screen.blit(count_text, text_rect)
        pygame.display.flip()
        pygame.time.wait(1000)


# respawn both players
def respawn_players():
    player1["rect"].topleft = PLAYER1_INITIAL_POS
    player2["rect"].topleft = PLAYER2_INITIAL_POS
    player1["direction"] = pygame.math.Vector2(1, 0)
    player2["direction"] = pygame.math.Vector2(-1, 0)
    projectiles.clear()


# main game loop
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
                    if current_time - player1["last_shot_time"] >= player1["shot_cooldown"]:
                        projectiles.append(create_projectile(player1["rect"].centerx, player1["rect"].centery, player1["direction"], 7, BLUE))
                        player1["last_shot_time"] = current_time
                elif event.key == pygame.K_RETURN:
                    if current_time - player2["last_shot_time"] >= player2["shot_cooldown"]:
                        projectiles.append(create_projectile(player2["rect"].centerx, player2["rect"].centery, player2["direction"], 7, RED))
                        player2["last_shot_time"] = current_time

        keys = pygame.key.get_pressed()
        move_player(player1, keys, pygame.K_w, pygame.K_s, pygame.K_a, pygame.K_d)
        move_player(player2, keys, pygame.K_UP, pygame.K_DOWN, pygame.K_LEFT, pygame.K_RIGHT)
        update_projectiles()

        # move dynamic obstacles
        for obstacle in obstacles:
            obstacle.move()

        draw()
        pygame.display.flip()

        game_over_message = check_collisions()
        if game_over_message:
            show_game_over_screen(game_over_message)
            gameplay_music.stop()
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

        clock.tick(60)


# start the game
show_start_screen()
main_game_loop()
