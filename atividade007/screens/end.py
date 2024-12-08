import pygame
import sys
from settings import *
from models.button import Button

from settings import SCREEN_HEIGHT, SCREEN_WIDTH, WHITE,BLUE


class End:
    def __init__(self,display,gameStateManager,Level_1):
        self.display = display
        self.gameStateManager = gameStateManager
        self.Level_1 = Level_1

    def get_font(self, size):
        return pygame.font.Font(FONT, size)

    def run(self):
        global background_channel
        pygame.display.set_caption("End Screen")
        running = True
        bg = pygame.image.load(BG_MENU)
        bg = pygame.transform.scale(bg,(SCREEN_WIDTH,SCREEN_HEIGHT))
        background_channel.play(BG_MUSIC,loops=-1)
        BG_MUSIC.set_volume(0.2)
        BUTTON_PRESS.set_volume(0.3)

        current_time = pygame.time.get_ticks()
        total_time = current_time - self.Level_1.get_initial_time()

        while running:
            self.display.fill(SKY_BLUE)
            self.display.blit(bg, (0,0))

            menu_mouse_pos = pygame.mouse.get_pos()
            menu_text = End.get_font(self, 36).render(TITLE, True, BLUE)
            menu_rect = menu_text.get_rect(center=(SCREEN_WIDTH //2, 100))
            time_text = End.get_font(self, 15).render(f"SUCCESS!! You've gotten to the sky in {total_time//1000} seconds! ", True, BLUE)
            time_text_rect = time_text.get_rect(center =(SCREEN_WIDTH//2,200))
            image = pygame.image.load(MENU_BUTTON)
            pygame.Surface.convert_alpha(image)
            start_game = Button(image=pygame.transform.scale(image, (370, 80)),
                                pos=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2),
                                text_input="To Main Menu", font=End.get_font(self, 25), base_color=BLACK,
                                hovering_color=GRAY)

            self.display.blit(menu_text, menu_rect)
            self.display.blit(time_text,time_text_rect)

            for button in [start_game]:
                button.change_color(menu_mouse_pos)
                button.update(self.display)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if start_game.check_for_input(menu_mouse_pos):
                        sound_effect_channel.play(BUTTON_PRESS)
                        running = False


            pygame.display.update()
        level = 1
        self.gameStateManager.set_state('main menu')

