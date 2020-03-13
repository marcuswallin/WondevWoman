import sys
import math
from array import array

# Auto-generated code below aims at helping you parse
# the standard input according to the problem statement.

#TODO use abstract class to define cells that can not be entered (holes).
class Cell:
    def __init__(self, x, y, height):
        self.x = x
        self.y = y
        self.height = height

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

class Map:
    def __init__(self, size):
        self.size = size
        self.cells = []

    def get_height(self, x, y):
        return self.cells[y][x]
    
    def print(self):
        for row in self.cells:
            for cell in row:
                print(cell, end = ' ', file=sys.stderr)
            print("", file=sys.stderr)

class Game:
    def __init__(self):
        self.map = Map(0)
        self.units_per_player = 0
    
    def read_start_input(self):
        self.map.size = int(input())
        self.units_per_player = int(input())


#TODO split function into smaller ones function
    def read_game_data(self):
        self.read_map_data()

        #TODO currently dummy input, should be Player objects
        self.read_player_data(1)
        self.read_player_data(2)

        self.read_legal_actions()

    def read_player_data(self, player):
        for i in range(self.units_per_player):
            unit_x, unit_y = [int(j) for j in input().split()]

    def read_legal_actions(self):
        legal_actions = int(input())
        for i in range(legal_actions):
            atype, index, dir_1, dir_2 = input().split()
            index = int(index)

    #TODO should let map object to most work
    #TODO Cells should really be cells, not strings as they are now
    def read_map_data(self):
        for i in range(self.map.size):
            row = input().split()
            self.map.cells.append([])
            for cell in row:
                self.map.cells[i].append(cell)


def main():
    game = Game()
    game.read_start_input()

    while True:
        game.read_game_data()
        print("MOVE&BUILD 0 N S")



if __name__ == '__main__':
    main()
