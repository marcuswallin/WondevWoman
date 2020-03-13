import sys
import math
from array import array
from enum import Enum

class Dir(Enum):
    N = 1
    NE = 2
    E = 3 
    SE = 4
    S = 5 
    SW = 6 
    W = 7 
    NW = 8 

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
        self.unit_index = unit_index
        self.move_dir = move_dir
        self.build_dir = build_dir

class MoveAndBuild(Action):
  def __init__(self, unit_index, move_dir, build_dir):
    super().__init__(unit_index, move_dir, build_dir)

class Unit:
    def __init__(self, init_pos):
        self.pos = init_pos

class Player:
    def __init__(self):
        self.nr_units = 0
        self.units = []

class Map:
    def __init__(self, size):
        self.size = size
        self.cells = []

    def get_height(self, x, y):
        return self.cells[y][x].height
    
    def throw_and_update_map_data(self):
        self.cells = []
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
        self.read_map_data()
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

    def read_map_data(self):
        self.map.throw_and_update_map_data()


def main():
    game = Game()
    game.read_start_input()

    while True:
        game.read_game_data()
        print("MOVE&BUILD 0 N S")

if __name__ == '__main__':
    main()
