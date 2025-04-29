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

        self.grid_width = 12
        self.grid_height = 12
        self.mine_n = 15

        self.SCREEN_WIDTH = self.grid_width*15
        self.SCREEN_HEIGHT = self.grid_height*15
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.run = True
        self.make_grid(0)
        self.initialized_game = 0
        self.quit = 0
        self.fps_cap = pygame.display.get_current_refresh_rate()

    def make_grid(self, call):
        if call == 0:
            self.grid = []
            self.uncovered = []
            for i in range (0, self.grid_width*self.grid_height):
                self.grid.append("")
                self.uncovered.append(0)

        else:
            self.grid = []
            self.uncovered = []

            # make an empty grid
            for i in range (0, self.grid_width*self.grid_height):
                self.grid.append("")
                self.uncovered.append(0)
            # print(len(self.grid))
            
            for item in self.spared_initial_cells:
                self.uncovered[item] = 1


            # add mines to the grid randomly
            mine_pos = []
            for i in range (self.mine_n):
                # add mine position and make sure to not repeat positions
                new_mine_position = randint(0, self.grid_width*self.grid_height-1)
                while new_mine_position in mine_pos or new_mine_position in self.spared_initial_cells:
                    new_mine_position = (new_mine_position + 1) % len(self.grid)
                mine_pos.append(new_mine_position)
                self.grid[mine_pos[i]] = "mine"
            self.mine_pos = mine_pos

            # assign numbers to cells (only check cells that are around a mine, and don't check cells more than once)
            checked_cells = []

            # for every mine in the grid
            for i in range (self.mine_n):
                # get the positions around the mine
                check_positions_around_mine = self.assign_numbers(mine_pos[i])
                # for every position around the mine
                for items in check_positions_around_mine:
                    # if that cell wasn't already checked
                    if items not in checked_cells and self.grid[items] != "mine":
                        # get list of positions around cell
                        check_positions_around_cell = self.assign_numbers(items)
                        # check mines at every position, assign number to cell
                        self.grid[items] = self.check_mines_around_cell(items, check_positions_around_cell)
                        # register that the cell has been checked
                        checked_cells.append(items)

            # uncover initial blanks
            self.uncovered_already = []

            for item in self.spared_initial_cells:
                self.uncover_blanks_in_vicinity(item)


    def uncover_blanks_in_vicinity(self, n, condition=None):
        positions_to_uncover = self.assign_numbers(n)
        for item in positions_to_uncover:
            if self.grid[item] != "mine" and item not in self.uncovered_already:
                if condition == None or (condition == "only_check_for_blanks" and self.grid[item] == ""):
                    self.uncovered[item] = 1
                    self.uncovered_already.append(item)
                    if self.grid[item] == "":
                        self.uncover_blanks_in_vicinity(item)


    def check_mines_around_cell(self, n, positions_to_check):
        number = 0
        for items in positions_to_check:
            if self.grid[items] == "mine":
                number += 1
        return number

    def assign_numbers(self, n):
        
        w = self.grid_width
        positions_to_check = []
        pos_list = [n-w-1, n-w, n-w+1, n-1, n+1, n+w-1, n+w, n+w+1]
        cell_line = floor(n/self.grid_width)
        line_list = [cell_line-1, cell_line-1, cell_line-1, cell_line, cell_line, cell_line+1, cell_line+1, cell_line+1]
        # only include positions that aren't out of the grid (and that are the intended ones)
        idx = -1
        for items in pos_list:
            idx += 1
            try:
                position = self.grid[items]
            except:
                pass
            else:
                # check whether it's on the intended line, if so add it to the list of positions to check around the cell
                if items >= 0:
                    if floor(items/self.grid_width) == line_list[idx]:
                        positions_to_check.append(items)
                
        return positions_to_check


    def check_mouse(self, x, y, xw, yw):
        x = round(x)
        xw = round(xw)
        y = round(y)
        yw = round(yw)
        if self.mouse_pos[0] in range (x, x+xw) and self.mouse_pos[1] in range (y, y+yw):
            if self.mouse_jr[0] == True: # uncover
                return ("clicked")
            elif self.mouse_jc[2] == True: # mark
                return ("mark")
            elif self.mouse_c[0] == True: # clicking
                return ("clicking") # clicking

    def game_run(self):
        while self.run:
            if self.quit == 1:
                self.make_grid(1)
                self.quit = 0
            self.clock.tick(self.fps_cap)            
            self.key = pygame.key.get_just_pressed()
            self.mouse_jr = pygame.mouse.get_just_released()
            self.mouse_c = pygame.mouse.get_pressed()
            self.mouse_jc = pygame.mouse.get_just_pressed()
            self.mouse_pos = pygame.mouse.get_pos()

            self.screen.fill((255,255,255))
            self.player.main()
            cell_sprite_size = 4
            cell_size_in_pixels = int(round(16*cell_sprite_size))

            grid_xoffs = (self.SCREEN_WIDTH-self.grid_width*cell_size_in_pixels)/2
            grid_yoffs = (self.SCREEN_HEIGHT-self.grid_height*cell_size_in_pixels)/2

            for i in range (0, self.grid_height):
                for n in range (0, self.grid_width):
                    position = i*self.grid_width+n

                    x = grid_xoffs
                    y = grid_yoffs
                    x += i*cell_size_in_pixels
                    y += n*cell_size_in_pixels

                    if self.uncovered[position] == 1:
                        cell_val = self.grid[position]
                        if cell_val == 0 or cell_val == "":
                            img = "cell_uncovered"
                        elif cell_val == "mine":
                            img = "cell_mine"
                        else:
                            img = "cell_" + str(cell_val)
                    else:
                        check_mouse = self.check_mouse(x, y, cell_size_in_pixels, cell_size_in_pixels)
                        if check_mouse == "clicked":
                            img = "cell_hidden_clicked"
                            self.uncovered[position] = 1
                            # if this is the first uncovering:
                            if self.initialized_game == 0:
                                self.initialized_game = 1
                                self.spared_initial_cells = [position]
                                self.quit = 1
                            else:
                                if self.grid[position] == "":
                                    self.uncover_blanks_in_vicinity(position)
                                elif self.grid[position] != "mine":
                                    self.uncover_blanks_in_vicinity(position, "only_check_for_blanks")
                                else:
                                    # if mine clicked, uncover every mine
                                    for mine in self.mine_pos:
                                        print(self.mine_pos, mine)
                                        self.uncovered[mine] = 1
                        else:
                            if check_mouse == "mark":
                                print(self.uncovered[position])
                                if self.uncovered[position] == "marked":
                                    self.uncovered[position] = 0
                                elif self.uncovered[position] == 0:
                                    self.uncovered[position] = "marked"
                                
                            if check_mouse == "clicking":
                                img = "cell_hidden_clicked"
                            elif self.uncovered[position] == "marked":
                                img = "cell_marked"
                            else:
                                img = "cell_hidden"


                    self.screen.blit(pygame.transform.scale_by(self.sprites[img], cell_sprite_size), (x, y))
                    check_mouse = self.check_mouse(x, y, cell_size_in_pixels, cell_size_in_pixels)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()

Game().game_run()