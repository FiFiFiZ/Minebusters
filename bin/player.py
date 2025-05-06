import pygame
from math import*
from random import*
from assets import Assets

# defining methods that can be called individually from the main script could be more efficient than running a main for every single one

class Player(pygame.sprite.Sprite):
    def __init__(self, attributes, *groups):
        super().__init__(*groups)
        self.assets = Assets()
        self.type = attributes[0]
        self.pos = attributes[1]
        
        # if main grid manager:
        if self.type == "main":
            self.grid_width = 6
            self.grid_height = 6
            self.mine_n = 10
            self.spared_initial_cells = []
            self.mine_pos = []
            self.make_grid(0, [])

    def rg__not_uc__mark(self, n):
        if self.uncovered[n] == "marked":
            self.uncovered[n] = 0
        elif self.uncovered[n] == 0:
            self.uncovered[n] = "marked"


    def lose_uncover_mines(self):
        for mine in self.mine_pos:
            self.uncovered[mine] = 1

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

    # make_grid: add mines to grid
    def make_grid__add_mines(self):
        mine_pos = []
        for i in range (self.mine_n):
            # add mine position and make sure to not repeat positions
            new_mine_position = randint(0, self.grid_width*self.grid_height-1)
            while new_mine_position in mine_pos or new_mine_position in self.spared_initial_cells:
                new_mine_position = (new_mine_position + 1) % len(self.grid)
            mine_pos.append(new_mine_position)
            self.grid[mine_pos[i]] = "mine"
        self.mine_pos = mine_pos

    # setup grid
    def make_grid(self, call, spared_init):
        self.spared_initial_cells = spared_init

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

            # make "uncovered status" list
            for item in self.spared_initial_cells:
                self.uncovered[item] = 1

            # add mines to the grid randomly
            self.make_grid__add_mines()

            # assign numbers to cells (only check cells that are around a mine, and don't check cells more than once)
            checked_cells = []

            # for every mine in the grid
            for i in range (self.mine_n):
                # get the positions around the mine
                check_positions_around_mine = self.assign_numbers(self.mine_pos[i])
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

    # extract grid from main grid that shows citizen pov 
    def extract_grid(self, grid, grid_width, uncovered, x, y, xw, yw):
        extracted_grid = []
        extracted_uncovered = []
        for i in range(yw-1):
            for n in range(xw-1):
                pos = x+n+(y+i)*grid_width
                extracted_grid.append(grid[pos])
                extracted_uncovered.append(uncovered[pos])

        return extracted_grid, extracted_uncovered
