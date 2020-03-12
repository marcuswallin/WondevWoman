import pytest
import sys
from wondevwoman import Cell, Game

def test_simple_point_init():
    cell = Cell(1,2,0)
    assert cell.x == 1
    assert cell.y == 2
    assert cell.height == 0


class GameTest:
    def __init__(self, start_input_file, loop_input_file):
        self.start_input_file = start_input_file 
        self.loop_input_file = loop_input_file

    def init_game_from_file(self):
        self.game = Game()
        self.insert_init_data_from_file_to_instream()
        self.read_game_data()
        
    def read_game_data(self):
        stdin_ = sys.stdin
        self.game.read_start_input()
        sys.stdin = stdin_ 

    def insert_init_data_from_file_to_instream(self):
        input_file = open(self.start_input_file, "r", encoding="utf-8")
        sys.stdin = input_file


def test_game_init():
    game = Game()
    assert game.size == 0
    assert game.units_per_player == 0

def test_file_init_game():
    game_test = GameTest("wondev_test_files/size6unit1.csv", "wondev_test_files/loop_data.csv")
    game_test.init_game_from_file()
    assert game_test.game.size == 6
    assert game_test.game.units_per_player == 1





 