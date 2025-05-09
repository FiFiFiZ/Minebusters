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


        self.players = [
            ["main", ""],
            ["pawn", 5]
        ] # add special attributes if needed
        self.player = []
        self.spawn_all_players()
        
        self.to_render = []

        self.uncovered = self.player[0].uncovered
        self.grid = self.player[0].grid
        self.grid_width = self.player[0].grid_width
        self.grid_height = self.player[0].grid_height
        self.mine_pos = self.player[0].mine_pos

        self.SCREEN_WIDTH = self.grid_width*15
        self.SCREEN_HEIGHT = self.grid_height*15
        self.SCREEN_WIDTH = pygame.display.Info().current_w
        self.SCREEN_HEIGHT = pygame.display.Info().current_h
        self.screen = pygame.display.set_mode((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
        pygame.display.toggle_fullscreen()
        self.clock = pygame.time.Clock()
        self.run = True
        # self.make_grid(0)
        self.initialized_game = 0
        self.quit = 0
        self.fps_cap = pygame.display.get_current_refresh_rate()
        # player attributes (this is a manually-set list, will be turned into a method of its own)

    def render_player(self, attributes, position_grid, cell_sprite_factor):
        if attributes != None:
            texture = self.sprites[attributes[0]]
            self.screen.blit(pygame.transform.scale_by(texture, cell_sprite_factor), position_grid)
            

    def spawn_all_players(self):
        idx = 0
        # create player for every player data in list
        for item in self.players:
            # every player has data and id
            self.player.append(Player(item, idx))
            idx += 1

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

    def run_grid_attributes(self, attributes):
            self.grid = attributes[1]
            self.uncovered = attributes[3]
            self.run_grid(attributes)
            attributes_to_return = self.grid, self.uncovered
            return attributes_to_return
            # make something here that allows for extracting a grid from the big grid to render only what the citizens see, maybe à partir de

    def rg__cell_covered_clicked(self, attributes):
        position = attributes[0]

        if attributes[1] == "run":
            img = "cell_hidden_clicked"
            self.uncovered[position] = 1
            # if this is the first uncovering:
            if self.initialized_game == 0:
                self.initialized_game = 1
                self.spared_initial_cells = [position]
                self.quit = 1
            # if this is not the first uncovering
            else:
                if self.grid[position] == "":
                    self.player[0].uncover_blanks_in_vicinity(position)
                elif self.grid[position] != "mine":
                    self.player[0].uncover_blanks_in_vicinity(position, "only_check_for_blanks")
                else:
                    # if mine clicked, uncover every mine
                    self.player[0].lose_uncover_mines()
        else:
            img = "cell_hidden"
                    
        return img

    def rg__cell_uncovered(self, attributes):
        position = attributes[0]
        x = attributes[1]
        y = attributes[2]
        cell_size_in_pixels = attributes[3]

        # assign image based on cell value
        cell_val = self.grid[position]
        if cell_val == 0 or cell_val == "":
            img = "cell_uncovered"
        elif cell_val == "mine":
            img = "cell_mine"
        else:
            img = "cell_" + str(cell_val)
        
        # if clicked, highlight cells around it
        if attributes[5] == "run":
            check_mouse = self.check_mouse(x, y, cell_size_in_pixels, cell_size_in_pixels)
            if check_mouse == "clicking":
                self.cells_highlighted = self.assign_numbers(position)
        
        return img

    # "for non-uncover clicks:"
    def rg__not_uc(self, attributes):
        position = attributes[0]
        check_mouse = attributes[1]
        type = attributes[2]

        # mark click:
        if type == "run":
            if check_mouse == "mark":
                self.player[0].rg__not_uc__mark(position)
                self.uncovered = self.player[0].uncovered
                print(self.uncovered)

        # left-click held:
        if check_mouse == "clicking":
            if type == "run":
                img = "cell_hidden_clicked"
                self.cells_highlighted = [position]
            else:
                img = "cell_hidden"
                                
        # no click:
        else:
            if self.uncovered[position] == "marked":
                img = "cell_marked"
            else:
                if position in self.cells_highlighted:
                    img = "cell_hidden_clicked"
                else:
                    img = "cell_hidden"
        return img

    def run_grid(self, attributes):
        # attributes: [0] - render only? // [1] - grid // [2] - grid_width // [3] - uncovered // [4] - grid_xoffs // [5] grid_yoffs

        # initialize grid info
        cell_sprite_factor = attributes[6]
        cell_size_in_pixels = int(round(self.sprites["cell_1"].get_width()*cell_sprite_factor))
        # grid_xoffs = (self.SCREEN_WIDTH-self.grid_width*cell_size_in_pixels)/2
        # grid_yoffs = (self.SCREEN_HEIGHT-self.grid_height*cell_size_in_pixels)/2
        grid_xoffs = attributes[4]
        grid_yoffs = attributes[5]
        type = attributes[0]
        player_type = attributes[7]

        # run and render cells
        for i in range (0, self.grid_height):
            for n in range (0, self.grid_width):
                position = i*self.grid_width+n

                x = grid_xoffs
                y = grid_yoffs
                x += i*cell_size_in_pixels
                y += n*cell_size_in_pixels

                # if cell uncovered:
                if self.uncovered[position] == 1:
                    img = self.rg__cell_uncovered([position, x, y, cell_size_in_pixels, cell_size_in_pixels, type])

                # if cell covered:
                else:
                    check_mouse = self.check_mouse(x, y, cell_size_in_pixels, cell_size_in_pixels)

                    # if clicked:
                    if check_mouse == "clicked":
                        img = self.rg__cell_covered_clicked([position, type])

                    # if not uncover-click:
                    else:
                        img = self.rg__not_uc([position, check_mouse, type])

                self.uncovered = self.player[0].uncovered
                self.grid = self.player[0].grid
                self.screen.blit(pygame.transform.scale_by(self.sprites[img], cell_sprite_factor), (x, y))
                check_mouse = self.check_mouse(x, y, cell_size_in_pixels, cell_size_in_pixels)

                if position in self.to_render:
                    list_index = self.to_render.index(position) + 1
                    self.render_player(self.to_render[list_index], (x, y), cell_sprite_factor)
                    self.to_render.pop(list_index-1)
                    self.to_render.pop(list_index-1)
                    	

    def game_run(self):
        while self.run:

            # reset grid (after initial click)
            if self.quit == 1:
                self.player[0].make_grid(1, self.spared_initial_cells)
                self.quit = 0
            elif self.quit == 2:
                self.player[0].make_grid(0, [])
                self.initialized_game = 0
                self.quit = 0

            self.clock.tick(self.fps_cap)
            self.key = pygame.key.get_just_pressed()
            self.key_held = pygame.key.get_pressed()
            self.mouse_jr = pygame.mouse.get_just_released()
            self.mouse_c = pygame.mouse.get_pressed()
            self.mouse_jc = pygame.mouse.get_just_pressed()
            self.mouse_pos = pygame.mouse.get_pos()

            self.screen.fill((255,255,255))
            # self.player.main()                

            # reset highlighted cells if no left click
            if self.mouse_c[0] == False:
                self.cells_highlighted = []

            if self.key[pygame.K_SPACE] == True:
                self.quit = 2
           
            for items in self.player: 
                # run every player at the end of turn
                if self.key[pygame.K_j] == True:
                    returned = items.turn_command([[self.player[0].grid, self.player[0].grid_width, self.player[0].uncovered, 0, 0, self.player[0].grid_width, self.player[0].grid_width]])

                # add player to render list
                render_returned = items.render_attributes()
                if render_returned != None:
                    # add position so that you can look up position later
                    self.to_render.append(render_returned[1])
                self.to_render.append(render_returned)

            self.run_grid_attributes(["run", self.player[0].grid, self.player[0].grid_width, self.player[0].uncovered,(self.SCREEN_WIDTH/2-self.player[0].grid_width*16*4)/2, (self.SCREEN_HEIGHT-self.player[0].grid_height*16*4)/2, 4, None])
            self.run_grid_attributes(["render-only", self.grid, self.grid_width, self.uncovered,(self.SCREEN_WIDTH/0.75-self.grid_width*16*4)/2, (self.SCREEN_HEIGHT-self.grid_height*16*4)/2, 6, "id"])
            self.grid = self.player[0].grid
            print(self.cells_highlighted)
            self.uncovered = self.player[0].uncovered

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.run = False
            pygame.display.update()


Game().game_run()




























# move grid management code to player for main grid and smaller grids alike, this way we can get to making player properties and drawing boards

# draw different boards corresponding to different extracted grids, then make player properties