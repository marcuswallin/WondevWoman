import pytest
import sys
import random
from wondevwoman import GameSimulator, Cell, Game, Map, Position, Direction, MoveAndBuild

def test_simple_position_init():
    pos = Position(5, 3)
    assert pos.x == 5
    assert pos.y == 3
    assert pos.equal(Position(5, 3))

def test_simple_point_init():
    cell = Cell(Position(1,2),0)
    assert cell.pos.equal(Position(1, 2))
    assert cell.height == 0


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
    assert curr_map.get_height(Position(0,0)) == 0
    assert curr_map.get_height(Position(1,0)) == 0
    assert curr_map.get_height(Position(2,0)) == 1
    assert curr_map.get_height(Position(3,0)) == 0
    assert curr_map.get_height(Position(5,0)) == -1
    assert curr_map.get_height(Position(4,0)) == -1
    assert curr_map.get_height(Position(0,4)) == 0
    assert curr_map.get_height(Position(1,4)) == 0
    assert curr_map.get_height(Position(2,4)) == 1
    assert curr_map.get_height(Position(3,4)) == 0
    assert curr_map.get_height(Position(4,4)) == 2
    assert curr_map.get_height(Position(5,4)) == 0
    assert curr_map.get_height(Position(5,5)) == 0

    assert game_test.game.me.nr_units == 1
    assert game_test.game.opponent.nr_units == 1
    assert game_test.game.me.units[0].pos.equal(Position(1, 1))
    
    assert game_test.game.opponent.units[0].pos.equal(Position(2, 2))


def test_game_update():
    game_test = GameTest("wondev_test_files/size6unit1.txt", "wondev_test_files/loop_size6unit1.txt")
    assert game_test.game.map.size == 6
    assert game_test.game.units_per_player == 1

    game_test.update_loop_data_from_file()
    curr_map = game_test.game.map
    assert curr_map.get_height(Position(0,2)) == 0
    assert curr_map.get_height(Position(1,2)) == 0
    assert curr_map.get_height(Position(2,2)) == 1
    assert curr_map.get_height(Position(3,2)) == 0
    assert curr_map.get_height(Position(4,2)) == 0
    assert curr_map.get_height(Position(5,2)) == 0
    assert game_test.verify_correct_nr_player_units()

    game_test.new_game_loop("wondev_test_files/loop_size6unit1_2.txt")
    assert curr_map.get_height(Position(0,2)) == 1
    assert curr_map.get_height(Position(1,2)) == 0
    assert curr_map.get_height(Position(2,2)) == 2
    assert curr_map.get_height(Position(3,2)) == 0
    assert curr_map.get_height(Position(4,2)) == 1
    assert curr_map.get_height(Position(5,2)) == 0
    assert game_test.verify_correct_nr_player_units()


def test_simulator_update():
    game_test = GameTest("wondev_test_files/size6unit1.txt", "wondev_test_files/loop_size6unit1.txt")
    game_test.update_loop_data_from_file()
    simulator = GameSimulator()
    simulator.copy_map(game_test.game.map)

    assert len(simulator.map.cells) == len(game_test.game.map.cells)

    simulator.map.cells[0][0].height = 4
    simulator.map.cells[1][0].height = 4
    simulator.map.cells[2][2].height = 4
    simulator.map.size = 10
    assert simulator.map.get_height(Position(0, 0)) == 4
    assert simulator.map.get_height(Position(4, 0)) == -1
    assert simulator.map.get_height(Position(4, 4)) == 2


    assert simulator.map.size is not game_test.game.map.size
    assert (simulator.map.get_height(Position(0,0)) is not 
            game_test.game.map.get_height(Position(0,0)))
    assert (simulator.map.get_height(Position(0,1)) is not 
            game_test.game.map.get_height(Position(0,1)))
    assert (simulator.map.get_height(Position(2,2)) is not 
            game_test.game.map.get_height(Position(2,2)))


def test_player_actions():
    game_test = GameTest("wondev_test_files/size6unit1.txt", "wondev_test_files/loop_size6unit1.txt")
    game_test.update_loop_data_from_file()

    assert game_test.game.me.actions[0].unit_index == 0
    assert game_test.game.me.actions[0].move_dir.relative_movement.equal(Position(0, -1)) 
    assert game_test.game.me.actions[0].build_dir.relative_movement.equal(Position(0, 1))
    assert isinstance(game_test.game.me.actions[0], MoveAndBuild)

    assert game_test.game.me.actions[1].move_dir.relative_movement.equal(Position(1, -1)) 
    assert game_test.game.me.actions[1].build_dir.relative_movement.equal(Position(-1, 1))

    assert game_test.game.me.actions[2].move_dir.relative_movement.equal(Position(1, 0)) 
    assert game_test.game.me.actions[2].build_dir.relative_movement.equal(Position(-1, -1))


def test_direction():
    N = Direction("N")
    assert N.relative_movement .equal(Position(0, -1))
    
    NE = Direction("NE")
    assert NE.relative_movement.equal(Position(1, -1))
    
    E = Direction("E")
    assert E.relative_movement.equal(Position(1, 0))
    
    SE = Direction("SE")
    assert SE.relative_movement.equal(Position(1, 1))
    
    S = Direction("S")
    assert S.relative_movement.equal(Position(0, 1))
    
    SW = Direction("SW")
    assert SW.relative_movement.equal(Position(-1, 1))

    W = Direction("W")
    assert W.relative_movement.equal(Position(-1, 0))
    
    NW = Direction("NW")
    assert NW.relative_movement.equal(Position(-1, -1))

    p1 = Position(1,1)
    p2 = Position(2,2)
    assert p1.pos_in_direction(E).equal(Position(2,1))
    assert p1.pos_in_direction(NW).equal(Position(0,0))
    assert p2.pos_in_direction(SE).equal(Position(3,3))




    











 