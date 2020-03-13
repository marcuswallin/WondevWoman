import sys
import math
import random
import copy
from array import array
from enum import Enum

#TODO change inte 2D enums
class Dir(Enum):
    N = 1
    NE = 2
    E = 3 
    SE = 4
    S = 5 
    SW = 6 
    W = 7 
    NW = 8
    
    def to_string(self):
        return self.name

    @classmethod
    def convert_direction_string_to_enum(cls, direction):
        if direction == 'N':
            return_dir = cls.N
        elif direction == 'NE':
            return_dir = cls.NE
        elif direction == 'E':
            return_dir = cls.E
        elif direction == 'SE':
            return_dir = cls.SE
        elif direction == 'S':
            return_dir = cls.S
        elif direction == 'SW':
            return_dir = cls.SW
        elif direction == 'W':
            return_dir = cls.W
        else:
            return_dir = cls.NW
        return return_dir


class Position:
    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y
    
    def equal(self, pos):
        return self.x == pos.x and self.y == pos.y

class Cell:
    def __init__(self, init_pos, map_input):
        self.pos = init_pos
        self.height = self.convert_input_to_integer(map_input)
    
    def convert_input_to_integer(self, map_input):
        try:
            height = int(map_input)
        except ValueError:
            height = -1
        return height

    def is_walkable(self):
        return self.height >= 0
    
#TODO SMART WAY OF STORING ACTION VALUES
class Action:
    def __init__(self, unit_index, move_dir, build_dir):
        self.unit_index = int(unit_index)
        self.move_dir = Dir.convert_direction_string_to_enum(move_dir)
        self.build_dir = Dir.convert_direction_string_to_enum(build_dir)


class MoveAndBuild(Action):
    def __init__(self, unit_index, move_dir, build_dir):
        super().__init__(unit_index, move_dir, build_dir)
    
    #I feel like this is unnecessary duplication
    def to_string(self):
        return f'MOVE&BUILD {self.unit_index} ' + \
        f'{self.move_dir.to_string()} {self.build_dir.to_string()}'


class Unit:
    def __init__(self, init_pos):
        self.pos = init_pos

class Player:
    def __init__(self):
        self.nr_units = 0
        self.units = []
        self.actions = []
    
    def clean(self):
        self.units = []
        self.actions = []

class Map:
    def __init__(self, size):
        self.size = size
        self.cells = []
    
    def clean(self):
        self.cells = []

    def get_height(self, position):
        return self.cells[position.y][position.x].height
    
    def update_data(self):
        for y_index in range(self.size):
            row = input().split()
            self.cells.append([])
            for x_index, cell_val in enumerate(row):
                self.cells[y_index].append(Cell(Position(x_index, y_index), cell_val))
    
    def print(self):
        for row in self.cells:
            for cell in row:
                print(cell, end = ' ', file=sys.stderr)
            print("", file=sys.stderr)

class Game:
    def __init__(self):
        self.map = Map(0)
        self.units_per_player = 0
        self.me = Player()
        self.opponent = Player()
    
    def read_start_input(self):
        self.map.size = int(input())
        self.units_per_player = int(input())
        self.me.nr_units = self.units_per_player
        self.opponent.nr_units = self.units_per_player

    def read_game_data(self):
        self.map.update_data()
        self.read_player_data(self.me)
        self.read_player_data(self.opponent)
        self.read_legal_actions()

    def read_player_data(self, player):
        for i in range(self.units_per_player):
            unit_x, unit_y = [int(j) for j in input().split()]
            player.units.append(Unit(Position(unit_x,unit_y)))

    def read_legal_actions(self):
        legal_actions = int(input())
        for i in range(legal_actions):
            atype, index, dir_1, dir_2 = input().split()
            index = int(index)
            if atype == "MOVE&BUILD":
                self.me.actions.append(MoveAndBuild(index, dir_1, dir_2))

    def clean_old_data(self):
        self.me.clean()
        self.opponent.clean()
        self.map.clean()

class GameSimulator:
    
    def __init__(self):
        self.map = Map(0)
    
    def copy_map(self, map):
        self.map.size = map.size
        self.map.cells = []
        for y, row in enumerate(map.cells):
            self.map.cells.append([])
            for cell in row:
                self.map.cells[y].append(copy.deepcopy(cell))  


    
    def move_up_or_random(self, player):
        current_height = self.map.get_height(player.units[0].position)

        return random.choice(player.actions)



def main():
    game = Game()
    simulator = GameSimulator()
    game.read_start_input()

    while True:
        game.clean_old_data()
        game.read_game_data()
        simulator.copy_map(game.map)
        action = simulator.move_up_or_random(game.me)
        print(action.to_string())

if __name__ == '__main__':
    main()
