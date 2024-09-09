# Jucimar Jr
# Cassiel Dutra
# 2024

import pygame
import random

AI_ERROR_ODDS = 0.1
MAX_SPEED_X = 11.5
MAX_SPEED_Y = 10

# Function to put a limit in ball's speed
def limit_ball_speed():
    global ball_dx, ball_dy

    # horizontal speed
    if ball_dx > MAX_SPEED_X:
        ball_dx = MAX_SPEED_X
    elif ball_dx < -MAX_SPEED_X:
        ball_dx = -MAX_SPEED_X
    
    # Vertical Speed
    if ball_dy > MAX_SPEED_Y:
        ball_dy = MAX_SPEED_Y
    elif ball_dy < -MAX_SPEED_Y:
        ball_dy = -MAX_SPEED_Y

pygame.init()

COLOR_BLACK = (0, 0, 0)
COLOR_WHITE = (255, 255, 255)

SCORE_MAX = 2

size = (1280, 720)
screen = pygame.display.set_mode(size)
pygame.display.set_caption("MyPong - PyGame Edition - 2024-09-08")

# score text
score_font = pygame.font.Font('assets\PressStart2P.ttf', 44)
score_text = score_font.render('00 x 00', True, COLOR_WHITE, COLOR_BLACK)
score_text_rect = score_text.get_rect()
score_text_rect.center = (680, 50)

# victory text
victory_font = pygame.font.Font('assets/PressStart2P.ttf', 100)
victory_text = victory_font.render('VICTORY', True, COLOR_WHITE, COLOR_BLACK)
victory_text_rect = score_text.get_rect()
victory_text_rect.center = (450, 350)

# sound effects
bounce_sound_effect = pygame.mixer.Sound('assets\pong-pygame_assets_bounce (1).wav')
scoring_sound_effect = pygame.mixer.Sound('C:assets\pong-pygame_assets_258020__kodack__arcade-bleep-sound.wav')

# player 1
player_1 = pygame.image.load("assets/player.png")
player_1_y = 300  # Posição inicial do p1
player_1_move_up = False 
player_1_move_down = False

# player 2 - robot
player_2 = pygame.image.load("assets/player.png")
player_2_y = 300  # Posição inicial do p2

# ball
ball = pygame.image.load("assets/ball.png")
ball_x = 640
ball_y = 360
ball_dx = 5
ball_dy = 5

# score
score_1 = 0
score_2 = 0

# game loop
game_loop = True
game_clock = pygame.time.Clock()

while game_loop:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game_loop = False

        #  keystroke events
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player_1_move_up = True
            if event.key == pygame.K_DOWN:
                player_1_move_down = True
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                player_1_move_up = False
            if event.key == pygame.K_DOWN:
                player_1_move_down = False

    # checking the victory condition
    if score_1 < SCORE_MAX and score_2 < SCORE_MAX:

        # clear screen
        screen.fill(COLOR_BLACK)

        # ball collision with the wall
        if ball_y > 700:
            ball_y = 700
            ball_dy *= -1.1
            bounce_sound_effect.play()
        elif ball_y <= 0:
            ball_y = 0
            ball_dy *= -1.1
            bounce_sound_effect.play()

        # ball collision with p1's paddle
        if ball_x < 100:  # verify if the ball is in the p1 paddle area
            if player_1_y < ball_y + 25 and player_1_y + 150 > ball_y:  # paddle collison
                ball_dx *= -1.1 # Reverses horizontal direction 
                
                # calculates the relative position of the ball
                relative_position = (ball_y - player_1_y) / 150  # 150 = paddle's height
                
                # Adjust the vertical direction (ball_dy) fallowing the collision point
                ball_dy = (relative_position - 1) * 10
                
                # Ball Speed Up
                ball_dx *= 1.15
                ball_dy *= 1.15

                # Try to prevent the bug where the ball gets stuck in the paddle      
                if ball_x < 100:  # collision with P1
                    ball_x = 100  # Ball go out of the paddle

                limit_ball_speed()
                
                # Sound effect
                bounce_sound_effect.play()

        # ball collision with the player 2 's paddle
        if ball_x > 1160:
            if player_2_y < ball_y + 25 and player_2_y + 150 > ball_y:
                    ball_dx *= -1.1

                    relative_position = (ball_y - player_2_y) / 150

                    ball_dy = (relative_position -0.7) * 10

                    # Try to prevent the bug where the ball gets stuck in the paddle      
                    if ball_x > 1160:  # Collision with P2
                        ball_x = 1160  # Ball go out of the paddle

                    limit_ball_speed()

                    '''
                    Disabled due to progressive speed up
                    ball_dx *= 1.1 
                    ball_dy *= 1.1'''

                    bounce_sound_effect.play()

        # scoring points
        if ball_x < -10:
            ball_x = 640
            ball_y = 360
            ball_dy *= -0.7
            ball_dx *= -0.7
            score_2 += 1
            scoring_sound_effect.play()
        elif ball_x > 1270:
            ball_x = 640
            ball_y = 360
            ball_dy *= -0.7
            ball_dx *= -0.7
            score_1 += 1
            scoring_sound_effect.play()

        # ball movement
        ball_x = ball_x + ball_dx
        ball_y = ball_y + ball_dy

        limit_ball_speed()

        # player 1 up movement
        if player_1_move_up:
            player_1_y -= 16 
        else:
            player_1_y += 0

        # player 1 down movement
        if player_1_move_down:
            player_1_y += 16
        else:
            player_1_y += 0

        # player 1 collides with upper wall
        if player_1_y <= 0:
            player_1_y = 0

        # player 1 collides with lower wall
        elif player_1_y >= 570:
            player_1_y = 570

        # player 2 "Artificial Intelligence"
        ai_speed = 5.8  # AI speed adjust

        # Establishes a fix speed to the AI's paddle fallowing the ball movement
        if player_2_y + 75 < ball_y:  # Under the paddle's center
            player_2_y += ai_speed 
        elif player_2_y + 75 > ball_y:  # Upper the paddle's center
            player_2_y -= ai_speed 

        if random.random() < AI_ERROR_ODDS:
            # Chance of the AI failling
            if player_2_y + 75 < ball_y:
                player_2_y += ai_speed // 2  # Slowdown the speed downwards
            elif player_2_y + 75 > ball_y:
                player_2_y -= ai_speed // 2  #Slowdown the speed upwards
   
        # Makes the P2 paddle "stay" in the screen
        if player_2_y <= 0:
            player_2_y = 0
        elif player_2_y >= 570:
            player_2_y = 570

        # update score hud
        score_text = score_font.render(str(score_1) + ' x ' + str(score_2), True, COLOR_WHITE, COLOR_BLACK)

        # drawing objects
        screen.blit(ball, (ball_x, ball_y))
        screen.blit(player_1, (50, player_1_y))
        screen.blit(player_2, (1180, player_2_y))
        screen.blit(score_text, score_text_rect)
    else:
        # drawing victory
        screen.fill(COLOR_BLACK)
        screen.blit(score_text, score_text_rect)
        screen.blit(victory_text, victory_text_rect)

    # update screen
    pygame.display.flip()
    game_clock.tick(60)

pygame.quit()
