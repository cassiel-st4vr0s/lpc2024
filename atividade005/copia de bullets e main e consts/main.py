import pygame
import constants as consts
import sys
import random
from button import Button
import mechanics as mec
from models.Enemy import Enemy
from models.Bullet import Bullet

running = False
Time = 0

pygame.init()
pygame.mixer.init()

# Defining audios channel
background_channel = pygame.mixer.Channel(0)
sound_effect_channel = pygame.mixer.Channel(1)


def survival_time(difficulty):
    if difficulty == 'easy':
        return 120* 60
    if difficulty == 'medium':
        return 150 * 60
    if difficulty == 'hard':
        return 180 * 60


def get_font(size):
    return pygame.font.Font(consts.FONT, size)


def main_menu():
    global running, Time
    pygame.display.set_caption("Main Menu")
    bg_music = pygame.mixer.Sound(consts.BG_MUSIC)
    button_sound = pygame.mixer.Sound(consts.BUTTON_SELECT)
    background_channel.play(bg_music, loops=-1)

    while True:
        screen.blit(background_image, (0, 0))

        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(38).render(consts.TITLE, True, consts.WHITE)
        menu_rect = menu_text.get_rect(center=(consts.WINDOW_WIDTH // 2, 100))
        image = pygame.image.load(consts.RECT)
        easy_button = Button(image=pygame.transform.scale(image, (370, 80)),
                             pos=(consts.WINDOW_WIDTH // 2, consts.WINDOW_HEIGHT // 2),
                             text_input="EASY", font=get_font(25), base_color=consts.BASE_COLOR,
                             hovering_color=consts.HOVERING_COLOR)
        medium_button = Button(image=pygame.transform.scale(image, (370, 80)),
                               pos=(consts.WINDOW_WIDTH // 2, consts.WINDOW_HEIGHT // 2 + 100),
                               text_input="MEDIUM", font=get_font(25), base_color=consts.BASE_COLOR,
                               hovering_color=consts.HOVERING_COLOR)
        hard_button = Button(image=pygame.transform.scale(image, (370, 80)),
                             pos=(consts.WINDOW_WIDTH // 2, consts.WINDOW_HEIGHT // 2 + 200),
                             text_input="HARD", font=get_font(25), base_color=consts.BASE_COLOR,
                             hovering_color=consts.HOVERING_COLOR)

        screen.blit(menu_text, menu_rect)

        for button in [easy_button, medium_button, hard_button]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if easy_button.check_for_input(menu_mouse_pos):
                    running = True
                    background_channel.play(game_background_music, loops=-1)
                    button_sound.play()
                    Time = survival_time("easy")
                    return 'easy'
                if medium_button.check_for_input(menu_mouse_pos):
                    running = True
                    background_channel.play(game_background_music, loops=-1)
                    button_sound.play()
                    Time = survival_time("medium")
                    return 'medium'
                if hard_button.check_for_input(menu_mouse_pos):
                    running = True
                    background_channel.play(game_background_music, loops=-1)
                    button_sound.play()
                    Time = survival_time("hard")
                    return 'hard'

        key = pygame.key.get_pressed()
        if key[pygame.K_ESCAPE]:
            pygame.quit()
            sys.exit()

        pygame.display.update()


# screen setup
screen = pygame.display.set_mode((consts.WINDOW_WIDTH, consts.WINDOW_HEIGHT))
clock = pygame.time.Clock()

# background
background_image = pygame.image.load("assets/Back_Image/Espace.jpg")

# player setup
player_original = pygame.image.load("assets/Player_1/Player 1.png")
player_width, player_height = 50, 50
player_original = pygame.transform.scale(player_original, (player_width, player_height))
player_x = (consts.WINDOW_WIDTH - player_width) // 2
player_y = consts.WINDOW_HEIGHT - player_height
player_speed = 5
player_angle = 0
last_time_blink = pygame.time.get_ticks()
blink_interval = 250
player_visible = True

# bullet setup
bullet_speed = 7
bullet = None
bullets_left = 4
max_bullets = 4
cooldown_time = 2
reloading = False
reload_start_time = 0
bullet_direction = consts.BulletDirection.UP
drawed_bullet = 4

# life
cooldown_lost_life = 2
lifes = 4
shadow_player = False

# Load music
pygame.mixer.music.set_volume(0.5)

# load sound effects
shoot_sound = pygame.mixer.Sound("assets/Sound game/Disparo.mp3")
reload_sound = pygame.mixer.Sound("assets/Sound game/Recarregamento.mp3")
lose_life_sound = pygame.mixer.Sound("assets/Sound game/lose_life_audio.mp3")
game_over_sound = pygame.mixer.Sound("assets/Sound game/game_over_sound.wav")
game_background_music = pygame.mixer.Sound("assets/Sound game/game_background_sound.mp3")

# Configuração dos inimigos
enemy_list = []
enemy_spawn_time = 2000  # Tempo para criação de novos inimigos (em milissegundos)
last_enemy_spawn = pygame.time.get_ticks()


def draw_lifes(lifes_remaining):
    x_lifes = 10
    for i in range(lifes_remaining):
        life_image = pygame.image.load("assets/hearts/heart.png")
        life_image = pygame.transform.scale(life_image, (50, 43))
        screen.blit(life_image, (x_lifes, 20))
        x_lifes += 50


def create_enemy():
    #Função para criar um inimigo em uma posição aleatória.
    x = random.randint(0, consts.WINDOW_WIDTH - 50)
    y = random.randint(0, consts.WINDOW_HEIGHT // 2)  # Inimigos começam na metade superior da tela
    speed = random.randint(1, 3)
    enemy = Enemy(x, y, 50, 50, speed, difficulty)
    enemy_list.append(enemy)


difficulty = main_menu()
score = 0
pygame.display.set_caption('Galactic Defenders')
timeout_shadow_player = 3000
timeout_max_time = 3000


def victory_screen():
    global difficulty, lifes, bullets_left, enemy_list, player_y, player_x, score, player_angle
    screen.blit(background_image, (0, 0))
    victory_theme = pygame.mixer.Sound(consts.VICTORY_THEME)
    button_sound = pygame.mixer.Sound(consts.BUTTON_SELECT)
    time_game_victory = 1500
    time_open_victory = pygame.time.get_ticks()
    bg_music = pygame.mixer.Sound(consts.BG_MUSIC)
    background_channel.stop()
    victory_theme_executed = False
    bg_music_executed = False

    while True:
        current_time_game_over = pygame.time.get_ticks()
        if current_time_game_over - time_open_victory <= time_game_victory:
            if not victory_theme_executed:
                background_channel.play(victory_theme, 0)
                victory_theme_executed = True
        else:
            if not bg_music_executed:
                background_channel.play(bg_music, -1)
                bg_music_executed = True
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(38).render("VICTORY!!!", True, consts.WHITE)
        menu_rect = menu_text.get_rect(center=(consts.WINDOW_WIDTH // 2, 100))
        image = pygame.image.load(consts.RECT)
        to_main_menu = Button(image=pygame.transform.scale(image, (370, 80)),
                              pos=((consts.WINDOW_WIDTH // 2), (consts.WINDOW_HEIGHT // 2) + 120),
                              text_input="Return to Menu", font=get_font(25), base_color=consts.BASE_COLOR,
                              hovering_color=consts.HOVERING_COLOR)
        score_text = font.render(f'Your Score: {score}', True, consts.WHITE)
        screen.blit(score_text, (consts.WINDOW_WIDTH // 2 - 145, 160))
        screen.blit(menu_text, menu_rect)

        for button in [to_main_menu]:
            button.change_color(menu_mouse_pos)
            button.update(screen)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                if to_main_menu.check_for_input(menu_mouse_pos):
                    background_channel.stop()
                    button_sound.play()
                    score = 0
                    bullets_left = 4
                    lifes = 4
                    enemy_list = []
                    player_x = (consts.WINDOW_WIDTH - player_width) // 2
                    player_y = consts.WINDOW_HEIGHT - player_height
                    difficulty = main_menu()
                    return
            key = pygame.key.get_pressed()
            if key[pygame.K_ESCAPE]:
                pygame.quit()
                sys.exit()
        pygame.display.update()


def game_over():
    global difficulty, lifes, bullets_left, enemy_list, player_y, player_x, score, player_angle
    pygame.display.set_caption("Game over")
    screen.blit(background_image, (0, 0))

    bg_music = pygame.mixer.Sound(consts.BG_MUSIC)
    button_sound = pygame.mixer.Sound(consts.BUTTON_SELECT)
    time_game_over = 1000
    time_open_game_over = pygame.time.get_ticks()
    background_channel.stop()
    game_over_sound_executed = False
    bg_music_executed = False

    while True:
        current_time_game_over = pygame.time.get_ticks()
        if current_time_game_over - time_open_game_over <= time_game_over:
            if not game_over_sound_executed:
                background_channel.play(game_over_sound, loops=0)
                game_over_sound_executed = True
        else:
            if not bg_music_executed:
                background_channel.play(bg_music, loops=-1)
                bg_music_executed = True
        menu_mouse_pos = pygame.mouse.get_pos()
        menu_text = get_font(38).render("GAME OVER", True, consts.WHITE)
        menu_rect = menu_text.get_rect(center=(consts.WINDOW_WIDTH // 2, 100))
        image = pygame.image.load(consts.RECT)
        to_main_menu = Button(image=pygame.transform.scale(image, (370, 80)),
                              pos=((consts.WINDOW_WIDTH // 2), (consts.WINDOW_HEIGHT // 2) + 120),
                              text_input="Return to menu", font=get_font(25), base_color=consts.BASE_COLOR,
                              hovering_color=consts.HOVERING_COLOR)
        screen.blit(menu_text, menu_rect)

        for button in [to_main_menu]:
            button.change_color(menu_mouse_pos)
            button.update(screen)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if to_main_menu.check_for_input(menu_mouse_pos):
                    button_sound.play()
                    score = 0
                    bullets_left = 4
                    lifes = 4
                    player_angle = 90
                    enemy_list = []
                    player_x = (consts.WINDOW_WIDTH - player_width) // 2
                    player_y = consts.WINDOW_HEIGHT - player_height
                    background_channel.stop()
                    difficulty = main_menu()
                    return
        pygame.display.update()


# Loop principal do jogo
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    # Key inputs
    key = pygame.key.get_pressed()

    if key[pygame.K_LEFT] and player_x > 0:
        player_x -= player_speed
        player_angle = 90

    if key[pygame.K_RIGHT] and player_x < consts.WINDOW_WIDTH - player_width:
        player_x += player_speed
        player_angle = -90

    if key[pygame.K_UP] and player_y > 0:
        player_y -= player_speed
        player_angle = 0

    if key[pygame.K_DOWN] and player_y < consts.WINDOW_HEIGHT - player_height:
        player_y += player_speed
        player_angle = 180

    # Escape key to quit the game
    if key[pygame.K_ESCAPE]:
        pygame.quit()
        sys.exit()

    # Space key to shoot a bullet, only if not in reload mode and bullets available
    if key[pygame.K_SPACE] and bullet is None and bullets_left > 0 and not reloading:
        sound_effect_channel.play(shoot_sound, loops=0)

        bullets_left -= 1
        if player_angle == 0:
            bullet = Bullet(player_x + player_width // 2, player_y,consts.BULLET_RADIUS,consts.BULLET_RADIUS,consts.BULLET_SPEED)
            bullet_direction = consts.BulletDirection.UP
        elif player_angle == 90:
            bullet = Bullet(player_x + player_width // 2, player_y,consts.BULLET_RADIUS,consts.BULLET_RADIUS,consts.BULLET_SPEED)
            bullet_direction = consts.BulletDirection.LEFT
        elif player_angle == 180:
            bullet = Bullet(player_x + player_width // 2, player_y,consts.BULLET_RADIUS,consts.BULLET_RADIUS,consts.BULLET_SPEED)
            bullet_direction = consts.BulletDirection.DOWN
        elif player_angle == -90:
            bullet = Bullet(player_x + player_width // 2, player_y,consts.BULLET_RADIUS,consts.BULLET_RADIUS,consts.BULLET_SPEED)
            bullet_direction = consts.BulletDirection.RIGHT

        # inicia a recarga
        if bullets_left == 0:
            reloading = True
            reload_start_time = pygame.time.get_ticks()
            sound_effect_channel.play(reload_sound, loops=0)

    # Se estiver recarregando, verifica o tempo de recarga
    if reloading:
        current_time = pygame.time.get_ticks()
        if current_time - reload_start_time >= cooldown_time * 1000:
            bullets_left = max_bullets
            reloading = False

    # Atualizar a bala
    if bullet:

        match bullet_direction:
            case consts.BulletDirection.UP:
                bullet.rect.y -= bullet_speed
                if bullet.rect.y<= 0:
                    bullet = None
            case consts.BulletDirection.DOWN:
                bullet.rect.y += bullet_speed
                if bullet.rect.y >= consts.WINDOW_HEIGHT:
                    bullet = None
            case consts.BulletDirection.LEFT:
                bullet.rect.x-= bullet_speed
                if bullet.rect.x <= 0:
                    bullet = None
            case consts.BulletDirection.RIGHT:
                bullet.rect.x += bullet_speed
                if bullet.rect.x >= consts.WINDOW_WIDTH:
                    bullet = None

    # Criar novos inimigos de acordo com o tempo
    current_time = pygame.time.get_ticks()
    if current_time - last_enemy_spawn > enemy_spawn_time:
        if len(enemy_list) <= consts.MAX_ENEMY_SPAWN:
            create_enemy()
        last_enemy_spawn = current_time

    # Atualizar movimento dos inimigos e verificar colisões
    for enemy in enemy_list:
        enemy.move()
        if bullet and enemy.rect.collidepoint(bullet.rect.x, bullet.rect.y):
            bullet = None  # Remove a bala
            enemy_list.remove(enemy)  # Remove o inimigo atingido
            score += 1

    if shadow_player:
        if current_time - last_time_blink >= blink_interval:
            player_visible = not player_visible
            last_time_blink = current_time

    # Desenhar na tela
    screen.blit(background_image, (0, 0))  # Fundo
    player_rotated = pygame.transform.rotate(player_original, player_angle)


    if player_visible:
        screen.blit(player_rotated, (player_x, player_y))  # Nave

    # Desenhar inimigos
    for enemy in enemy_list:
        enemy.draw(screen)

    if shadow_player:
        if current_time - timeout_shadow_player >= cooldown_lost_life * 1000:
            shadow_player = False

    # Verificar colisão com o jogador
    for enemy in enemy_list:
        if enemy.rect.colliderect(pygame.rect.Rect(player_x,
                                                   player_y,
                                                   player_rotated.get_rect().width,
                                                   player_rotated.get_rect().height)) and not shadow_player:
            if lifes == 1:
                running = False
                game_over()
            else:
                sound_effect_channel.play(lose_life_sound, 0)
                lifes -= 1
                shadow_player = True
                timeout_shadow_player = current_time

    draw_lifes(lifes)

    # Desenhar a bala
    if bullet:
        bullet_rotated = pygame.transform.rotate(bullet.image, player_angle+90)
        screen.blit(bullet_rotated, (bullet.rect.x, bullet.rect.y))
        bullet.draw(screen)
    # Exibir balas restantes
    font = get_font(20)
    ammo_text = font.render(f'ammo: {bullets_left}', True, consts.WHITE)
    screen.blit(ammo_text, (10, 70))

    # Exibir mensagem de recarregamento, se aplicável
    if reloading:
        reload_text = font.render('reloading...', True, consts.RED)
        screen.blit(reload_text, (10, 95))

    # SCORE
    score_text = font.render(f'score: {score}', True, consts.WHITE)
    screen.blit(score_text, (consts.WINDOW_WIDTH - 180, 50))

    # TIMER
    if Time == 0:
        running = False
        victory_screen()
    else:
        time_text = font.render(f'{Time // 60}', True, consts.WHITE)
        screen.blit(time_text, (10, 125))
        Time -= 1

    # Atualizar a tela
    pygame.display.update()
    clock.tick(60)
