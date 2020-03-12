import sys
import math

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

class Game:
    def __init__(self):
        self.size = 0
        self.units_per_player = 0
    
    def read_start_input(self):
        self.size = int(input())
        self.units_per_player = int(input())

#TODO split function into smaller ones function
    def read_game_data(self):
        for i in range(self.size):
            row = input()
            print(row, file=sys.stderr)
        for i in range(self.units_per_player):
            unit_x, unit_y = [int(j) for j in input().split()]
            print(str(unit_x) +" "+str(unit_y), file=sys.stderr)
        for i in range(self.units_per_player):
            other_x, other_y = [int(j) for j in input().split()]
            print(str(other_x)+" "+str(other_y), file=sys.stderr)
        legal_actions = int(input())
        for i in range(legal_actions):
            atype, index, dir_1, dir_2 = input().split()
            index = int(index)
            print(f'{atype} {index} {dir_1} {dir_2}', file=sys.stderr)

def main():
    game = Game()
    game.read_start_input()

    while True:
        game.read_game_data()
        print("MOVE&BUILD 0 N S")



if __name__ == '__main__':
    main()
