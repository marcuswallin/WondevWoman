import pytest
import sys
import random
from wondevwoman import Cell, Game, Map


class GameTest:
    def __init__(self, start_input_file, loop_input_file):
        self.start_input_file = start_input_file 
        self.loop_input_file = loop_input_file
        self.init_game_from_file()

    def init_game_from_file(self):
        self.game = Game()
        self.insert_data_from_file_to_instream(self.start_input_file)
        self.read_game_data()
        
    def read_game_data(self):
        stdin_ = sys.stdin
        self.game.read_start_input()
        sys.stdin = stdin_ 
    
    def update_loop_data_from_file(self):
        self.insert_data_from_file_to_instream(self.loop_input_file)
        self.read_loop_data_from_stream()

    def insert_data_from_file_to_instream(self, file_name):
        input_file = open(file_name, "r", encoding="utf-8")
        sys.stdin = input_file

    def read_loop_data_from_stream(self):
        stdin_ = sys.stdin
        self.game.read_game_data()
        sys.stdin = stdin_ 
    
    def verify_correct_nr_player_units(self):
        units_equal_me = self.game.me.nr_units == len(self.game.me.units)
        units_equal_opp = self.game.opponent.nr_units == len(self.game.opponent.units)
        return units_equal_me and units_equal_opp

    def new_game_loop(self, new_file):
        self.game.clean_old_data()
        self.loop_input_file = new_file
        self.update_loop_data_from_file()

def test_simple_point_init():
    cell = Cell(1,2,0)
    assert cell.x == 1
    assert cell.y == 2
    assert cell.height == 0


def test_game_init():
    game = Game()
    assert game.map.size == 0
    assert game.units_per_player == 0

def test_file_init_game_simple():
    game_test = GameTest("wondev_test_files/size6unit1.txt", "wondev_test_files/loop_size6unit1.txt")
    assert game_test.game.map.size == 6
    assert game_test.game.units_per_player == 1

    game_test.update_loop_data_from_file()
    curr_map = game_test.game.map
    assert curr_map.get_height(0,0) == 0
    assert curr_map.get_height(1,0) == 0
    assert curr_map.get_height(2,0) == 1
    assert curr_map.get_height(3,0) == 0
    assert curr_map.get_height(4,0) == -1
    assert curr_map.get_height(5,0) == -1
    assert curr_map.get_height(0,4) == 0
    assert curr_map.get_height(1,4) == 0
    assert curr_map.get_height(2,4) == 1
    assert curr_map.get_height(3,4) == 0
    assert curr_map.get_height(4,4) == 2
    assert curr_map.get_height(5,4) == 0
    assert curr_map.get_height(5,5) == 0

    assert game_test.game.me.nr_units == 1
    assert game_test.game.opponent.nr_units == 1
    assert game_test.game.me.units[0].x == 1
    assert game_test.game.me.units[0].y == 1
    
    assert game_test.game.opponent.units[0].x == 2
    assert game_test.game.opponent.units[0].y == 2


def test_game_update():
    game_test = GameTest("wondev_test_files/size6unit1.txt", "wondev_test_files/loop_size6unit1.txt")
    assert game_test.game.map.size == 6
    assert game_test.game.units_per_player == 1

    game_test.update_loop_data_from_file()
    curr_map = game_test.game.map
    assert curr_map.get_height(0,2) == 0
    assert curr_map.get_height(1,2) == 0
    assert curr_map.get_height(2,2) == 1
    assert curr_map.get_height(3,2) == 0
    assert curr_map.get_height(4,2) == 0
    assert curr_map.get_height(5,2) == 0
    assert game_test.verify_correct_nr_player_units()

    game_test.new_game_loop("wondev_test_files/loop_size6unit1_2.txt")
    assert curr_map.get_height(0,2) == 1
    assert curr_map.get_height(1,2) == 0
    assert curr_map.get_height(2,2) == 2
    assert curr_map.get_height(3,2) == 0
    assert curr_map.get_height(4,2) == 1
    assert curr_map.get_height(5,2) == 0
    assert game_test.verify_correct_nr_player_units()
    











 