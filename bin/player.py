import pygame
from math import*
from random import*
from assets import Assets

class Player(pygame.sprite.Sprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.assets = Assets()
        self.grid = []
        self.grid_width = 8
        self.grid_height = 8
        self.mine_n = 6

        # make an empty grid
        for i in range (0, self.grid_width*self.grid_height):
            self.grid.append("")
        # print(len(self.grid))

        # add mines to the grid randomly
        mine_pos = []
        for i in range (self.mine_n):
            # add mine position and make sure to not repeat positions
            new_mine_position = randint(0, self.grid_width*self.grid_height-1)
            while new_mine_position in mine_pos:
                new_mine_position = (new_mine_position + 1) % len(self.grid)
            mine_pos.append(new_mine_position)
            self.grid[mine_pos[i]] = "mine" # ITS SOMETIMES IndexError: list assignment index out of range

        # assign numbers to cells (only check cells that are around a mine, and don't check cells more than once)
        checked_cells = []

        # for every mine in the grid
        for i in range (self.mine_n):
            # get the positions around the mine
            check_positions_around_mine = self.assign_numbers(mine_pos[i], self.grid_width, self.grid_height)
            # for every position around the mine
            for items in check_positions_around_mine:
                # if that cell wasn't already checked
                if items not in checked_cells and self.grid[items] != "mine":
                    # get list of positions around cell
                    check_positions_around_cell = self.assign_numbers(items, self.grid_width, self.grid_height)
                    # check mines at every position, assign number to cell
                    self.grid[items] = self.check_mines_around_cell(items, check_positions_around_cell)
                    # register that the cell has been checked
                    checked_cells.append(items)


    def check_mines_around_cell(self, n, positions_to_check):
        number = 0
        for items in positions_to_check:
            if self.grid[items] == "mine":
                number += 1
        return number

    def assign_numbers(self, n, w, h):
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
                if floor(items/self.grid_width) == line_list[idx]:
                    positions_to_check.append(items)
                
        return positions_to_check

    def main(self):
        # print(self.grid)
        pass