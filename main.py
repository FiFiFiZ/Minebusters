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
        self.sprites = self.assets.sprites

        self.player = Player()
        self.grid = self.player.grid
        self.grid_width = self.player.grid_width
        self.grid_height = self.player.grid_height

        self.SCREEN_WIDTH = 640
        self.SCREEN_HEIGHT = 360
        # self.SCREEN_WIDTH = pygame.display.Info().current_w
        # self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SCALED)
        # pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.run = True
        pass

    def check_mouse(self, x, y, xw, yw):
        if self.mouse_pos[0] in range (x, x+xw) and self.mouse_pos[1] in range (y, y+yw):
            if self.mouse_jr[0] == True: # uncover
                return ("clicked")
            elif self.mouse_c[2] == True: # mark
                return ("mark")
            elif self.mouse_c[0] == True: # clicking
                return ("clicking") # clicking

    def game_run(self):
        while self.run:
            self.clock.tick(30)            
            self.key = pygame.key.get_just_pressed()
            self.mouse_jr = pygame.mouse.get_just_released()
            self.mouse_c = pygame.mouse.get_pressed()
            self.mouse_pos = pygame.mouse.get_pos()

            self.screen.fill((255,255,255))
            self.player.main()
            self.uncovered = self.player.uncovered

            for i in range (0, self.grid_height):
                for n in range (0, self.grid_width):
                    position = i*self.grid_width+n

                    x = i*15
                    y = n*15

                    if self.uncovered[position] == 1:
                        cell_val = self.grid[position]
                        if cell_val == 0 or cell_val == "":
                            img = "cell_uncovered"
                        elif cell_val == "mine":
                            img = "cell_mine"
                        else:
                            img = "cell_" + str(cell_val)
                    else:
                        check_mouse = self.check_mouse(x, y, 15, 15)
                        if check_mouse == "clicked":
                            img = "cell_hidden_clicked"
                            self.uncovered[position] = 1
                        else:
                            if check_mouse == "clicking":
                                img = "cell_hidden_clicked"
                            else:
                                img = "cell_hidden"


                    self.screen.blit(self.sprites[img], (x, y))
                    check_mouse = self.check_mouse(x, y, 15, 15)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()