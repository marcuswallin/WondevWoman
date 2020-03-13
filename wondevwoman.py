import sys
import math
import random
from array import array

class Cell:
    def __init__(self, x, y, map_input):
        self.x = x
        self.y = y
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
    def __init__(self, action_type, unit_index, move_dir, build_dir):
        self.action_type = action_type
        self.unit_index = unit_index
        self.move_dir = move_dir
        self.build_dir = build_dir

class Unit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

class Player:
    def __init__(self):
        self.nr_units = 0
        self.units = []
    
    def clean(self):
        self.units = []

class Map:
    def __init__(self, size):
        self.size = size
        self.cells = []
    
    def clean(self):
        self.cells = []

    def get_height(self, x, y):
        return self.cells[y][x].height
    
    def update_data(self):
        for y_index in range(self.size):
            row = input().split()
            self.cells.append([])
            for x_index, cell_val in enumerate(row):
                self.cells[y_index].append(Cell(x_index, y_index, cell_val))
    
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
            player.units.append(Unit(unit_x,unit_y))

    def read_legal_actions(self):
        legal_actions = int(input())
        for i in range(legal_actions):
            atype, index, dir_1, dir_2 = input().split()
            index = int(index)

    def clean_old_data(self):
        self.me.clean()
        self.opponent.clean()
        self.map.clean()
        #self.actionlist.clean()

class GameSimulator:
    
    def return_random_valid_action(self, player):
        try:
            return random.choice(player.actions)
        except IndexError:
            print("I CAN NOT MOVE", file=sys.stderr)
       #     return 


def main():
    game = Game()
    simulator = GameSimulator()
    game.read_start_input()

    while True:
        game.clean_old_data()
        game.read_game_data()
        action = simulator.return_random_valid_action(game.me)
        print("MOVE&BUILD 0 N S")

if __name__ == '__main__':
    main()
