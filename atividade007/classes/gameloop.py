import pygame
import sys
from levels.level1 import *
from levels.level2 import *
from levels.level3 import *
from pygame import MOUSEBUTTONDOWN
from settings import SCREEN_WIDTH, SCREEN_HEIGHT
from screens.start import Start
from screens.ControlsScreen1_3 import ControlsScreen, ControlsScreen2, ControlsScreen3
from classes import player, platform
from classes.player import *
from classes.gamestate_manager import GameStateManager


class GameLoop:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption("Typing Game - Phase 1")
        self.player_class = player
        self.platform_class = platform
        self.gameStateManager = GameStateManager('main menu')
        self.start = Start(self.screen, self.gameStateManager)
        self.controlsScreen = ControlsScreen(self.screen, self.gameStateManager)
        self.controlsScreen2 = ControlsScreen2(self.screen, self.gameStateManager)
        self.controlsScreen3 = ControlsScreen3(self.screen,self.gameStateManager)
        self.level_1 = Level_1(self.screen,self.gameStateManager,self.player_class,self.platform_class)
        self.level_2 = Level_2(self.screen,self.gameStateManager, self.player_class,self.platform_class)
        self.level_3 = Level_3(self.screen,self.gameStateManager, self.player_class,self.platform_class)
        self.states = {'main menu': self.start, 'controls screen': self.controlsScreen, 'level 1': self.level_1,'level 2':self.level_2,
                       'level 3':self.level_3,'controls screen 2':self.controlsScreen2,'controls screen 3':self.controlsScreen3}

    def run(self):
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                    pygame.quit()
                    sys.exit()

            self.states[self.gameStateManager.get_state()].run()
            pygame.display.update()