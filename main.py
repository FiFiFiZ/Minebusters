import pygame
from math import*
from random import*
import sys
sys.path.append("./bin")

from player import Player # type: ignore
from assets import Assets # type: ignore


class Game:
    def __init__(self):
        pygame.init()

        self.assets = Assets()
        self.player = Player()
        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 360
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SCALED)
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.run = True
        pass

    def game_run(self):
        while self.run:
            self.clock.tick(30)            
            self.key = pygame.key.get_just_pressed()
            self.screen.fill((255,255,255))
            # self.player.main()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()