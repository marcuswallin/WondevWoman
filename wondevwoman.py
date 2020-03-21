import sys
import math
import random
import copy
from array import array
from enum import Enum



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
            self.me.add_action(atype, index, dir_1, dir_2)

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
        best_action = player.get_action_with_highest_pos(self.map)
        return best_action


class Map:
    def __init__(self, size):
        self.size = size
        self.cells = []

    def clean(self):
        self.cells = []

    def get_cell(self, pos):
        return self.cells[pos.y][pos.x]

    def get_height(self, pos):
        return self.get_cell(pos).height

    def update_data(self):
        for y_index in range(self.size):
            row = list(input())
            self.cells.append([])
            for x_index, cell_val in enumerate(row):
                self.cells[y_index].append(Cell(Position(x_index, y_index), cell_val))

    def print(self):
        for row in self.cells:
            for cell in row:
                print(cell.description, end = ' ', file=sys.stderr)
            print("", file=sys.stderr)


class Player:
    def __init__(self):
        self.nr_units = 0
        self.units = []

    def clean(self):
        self.units = []

    def get_action_with_highest_pos(self, map):
        highest_cell = None
        best_action = None
        for action in self.actions:
            move_to_cell = map.get_cell(self.units[0].pos.pos_in_direction(action.move_dir))
            if move_to_cell > highest_cell:
                highest_cell = move_to_cell
                best_action = action
        return best_action

    def add_action(self, atype, index, dir_1, dir_2):
        if atype == "MOVE&BUILD":
            self.units[index].actions.append(MoveAndBuild(index, dir_1, dir_2))



class Direction():

    def __init__(self, direction: str):
        self.name = direction
        self.relative_movement = self.convert_direction_string_to_point(direction)

    def to_string(self):
        return self.name

    def convert_direction_string_to_point(self,direction):
        if direction == 'N':
            return_dir = Position(0, -1)
        elif direction == 'NE':
            return_dir =  Position(1, -1)
        elif direction == 'E':
            return_dir =  Position(1, 0)
        elif direction == 'SE':
            return_dir =  Position(1, 1)
        elif direction == 'S':
            return_dir =  Position(0, 1)
        elif direction == 'SW':
            return_dir =  Position(-1, 1)
        elif direction == 'W':
            return_dir =  Position(-1, 0)
        elif direction == 'NW':
            return_dir = Position(-1, -1)
        return return_dir


class Position:
    def __init__(self, init_x, init_y):
        self.x = init_x
        self.y = init_y

    def equal(self, pos):
        return self.x == pos.x and self.y == pos.y

    def to_string(self):
        return f'{self.x} {self.y}'

    def __add__(self, o):
        return Position(self.x+o.x, self.y+o.y)

    def pos_in_direction(self, dir: Direction):
        return self + dir.relative_movement



class Cell:
    def __init__(self, init_pos, map_input):
        self.pos = init_pos
        self.height = self.convert_input_to_integer(map_input)
        self.description = map_input

    def convert_input_to_integer(self, map_input):
        try:
            height = int(map_input)
        except ValueError:
            height = -1
        return height

    def is_walkable(self):
        return self.height >= 0

    def __gt__(self, o):
        return (not o or self.height > o.height)


class Action:
    def __init__(self, unit_index, move_dir, build_dir):
        self.unit_index = int(unit_index)
        self.move_dir = Direction(move_dir)
        self.build_dir = Direction(build_dir)


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
        self.actions = []


if __name__ == '__main__':
    main()
