'''--- Day 15: Warehouse Woes ---
You appear back inside your own mini submarine! Each Historian drives their mini submarine in a different direction; maybe the Chief has his own submarine down here somewhere as well?

You look up to see a vast school of lanternfish swimming past you. On closer inspection, they seem quite anxious, so you drive your mini submarine over to see if you can help.

Because lanternfish populations grow rapidly, they need a lot of food, and that food needs to be stored somewhere. That's why these lanternfish have built elaborate warehouse complexes operated by robots!

These lanternfish seem so anxious because they have lost control of the robot that operates one of their most important warehouses! It is currently running amok, pushing around boxes in the warehouse with no regard for lanternfish logistics or lanternfish inventory-management strategies.

Right now, none of the lanternfish are brave enough to swim up to an unpredictable robot so they could shut it off. However, if you could anticipate the robot's movements, maybe they could find a safe option.

The lanternfish already have a map of the warehouse and a list of movements the robot will attempt to make (your puzzle input). The problem is that the movements will sometimes fail as boxes are shifted around, making the actual movements of the robot difficult to predict.

For example:

##########
#..O..O.O#
#......O.#
#.OO..O.O#
#..O@..O.#
#O#..O...#
#O..O..O.#
#.OO.O.OO#
#....O...#
##########

<vv>^<v^>v>^vv^v>v<>v^v<v<^vv<<<^><<><>>v<vvv<>^v^>^<<<><<v<<<v^vv^v>^
vvv<<^>^v^^><<>>><>^<<><^vv^^<>vvv<>><^^v>^>vv<>v<<<<v<^v>^<^^>>>^<v<v
><>vv>v^v^<>><>>>><^^>vv>v<^^^>>v^v^<^^>v^^>v^<^v>v<>>v^v^<v>v^^<^^vv<
<<v<^>>^^^^>>>v^<>vvv^><v<<<>^^^vv^<vvv>^>v<^^^^v<>^>vvvv><>>v^<<^^^^^
^><^><>>><>^^<<^^v>>><^<v>^<vv>>v>>>^v><>^v><<<<v>>v<v<v>vvv>^<><<>^><
^>><>^v<><^vvv<^^<><v<<<<<><^v<<<><<<^^<v<^^^><^>>^<v^><<<^>>^v<v^v<v^
>^>>^v>vv>^<<^v<>><<><<v<<v><>v<^vv<<<>^^v^>^^>>><<^v>>v^v><^^>>^<>vv^
<><^^>^^^<><vvvvv^v<v<<>^v<v>v<<^><<><<><<<^^<<<^<<>><<><^^^>^^<>^>v<>
^^>vv<^v^v<vv>^<><v<^v>^^^>>>^^vvv^>vvv<>>>^<^>>>>>^<<^v>^vvv<>^<><<v>
v^^>>><<^^<>>^v^<v^vv<>v^<<>^<^v^v><^<<<><<^<v><v<>vv>>v><v^<vv<>v^<<^

As the robot (@) attempts to move, if there are any boxes (O) in the way, the robot will also attempt to push those boxes. However, if this action would cause the robot or a box to move into a wall (#), nothing moves instead, including the robot. The initial positions of these are shown on the map at the top of the document the lanternfish gave you.

The rest of the document describes the moves (^ for up, v for down, < for left, > for right) that the robot will attempt to make, in order. (The moves form a single giant sequence; they are broken into multiple lines just to make copy-pasting easier. Newlines within the move sequence should be ignored.)

Here is a smaller example to get started:

########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

<^^>>>vv<v>>v<<

Were the robot to attempt the given sequence of moves, it would push around the boxes as follows:

Initial state:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move <:
########
#..O.O.#
##@.O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move ^:
########
#.@O.O.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#..@OO.#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move >:
########
#...@OO#
##..O..#
#...O..#
#.#.O..#
#...O..#
#......#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##..@..#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.@...#
#...O..#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#..@O..#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#...@O.#
#.#.O..#
#...O..#
#...O..#
########

Move >:
########
#....OO#
##.....#
#....@O#
#.#.O..#
#...O..#
#...O..#
########

Move v:
########
#....OO#
##.....#
#.....O#
#.#.O@.#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

Move <:
########
#....OO#
##.....#
#.....O#
#.#O@..#
#...O..#
#...O..#
########

The larger example has many more moves; after the robot has finished those moves, the warehouse would look like this:

##########
#.O.O.OOO#
#........#
#OO......#
#OO@.....#
#O#.....O#
#O.....OO#
#O.....OO#
#OO....OO#
##########

The lanternfish use their own custom Goods Positioning System (GPS for short) to track the locations of the boxes. The GPS coordinate of a box is equal to 100 times its distance from the top edge of the map plus its distance from the left edge of the map. (This process does not stop at wall tiles; measure all the way to the edges of the map.)

So, the box shown below has a distance of 1 from the top edge of the map and 4 from the left edge of the map, resulting in a GPS coordinate of 100 * 1 + 4 = 104.

#######
#...O..
#......
The lanternfish would like to know the sum of all boxes' GPS coordinates after the robot finishes moving. In the larger example, the sum of all boxes' GPS coordinates is 10092. In the smaller example, the sum is 2028.

Predict the motion of the robot and boxes in the warehouse. After the robot is finished moving, what is the sum of all boxes' GPS coordinates?
'''

import math
from pathlib import Path
from rich import print
from pprint import pprint
from copy import deepcopy
from typing import NamedTuple, Protocol, Optional
from enum import Enum, IntEnum
from dataclasses import dataclass, field
from string import ascii_letters
import itertools
import functools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day15_example.txt'
INPUT = DATA_DIR / 'day15_input.txt'

class Point(NamedTuple):
    row: int
    col: int
    char: str

class Box(Point):
    ...

class Wall(Point):
    ...

class Direction(Enum):
    UP = '^'
    RIGHT = '>'
    DOWN = 'v'
    LEFT = '<'

@dataclass
class MapRow():
    point_list: list[Point]
    row_num: int
    total_map_height: int

    @property
    def width(self):
        return len(self.point_list)

    def get_point(self, col_num: int) -> Point:
        return self.point_list[col_num]


@dataclass
class Map():
    row_list: list[MapRow]

    @property
    def height(self):
        return len(self.row_list)

    @property
    def width(self):
        return self.row_list[0].width

    def print(self) -> None:
        for row in self.row_list:
            print(''.join(point.char for point in row.point_list))

    def get_row(self, y: int) -> MapRow:
        return self.row_list[y]

    def get_point(self, row_num: int, col_num: int) -> Point:
        row = self.row_list[row_num]
        return row.get_point(col_num)

    def replace_point(self, old_point: Point, new_point: Point) -> None:
        row_num = old_point.row
        col_num = old_point.col
        self.row_list[row_num].point_list[col_num] = new_point

@dataclass
class Robot():
    point: Point
    map: Map = field(repr=False)
    moves_str: str = field(repr=False)
    moves_count: int = 0

    def make_next_move(self) -> None:
        if self.moves_count == len(self.moves_str):
            print('Done!')
            return None
        
        current_row = self.point.row
        current_col = self.point.col
        next_move_str = self.moves_str[self.moves_count]
        next_direction = Direction(next_move_str)

        print()
        self.map.print()
        
        match next_direction:
            case Direction.UP:
                next_point = self.map.get_point(current_row - 1, current_col)
            case Direction.RIGHT:
                next_point = self.map.get_point(current_row, current_col + 1)
            case Direction.DOWN:
                next_point = self.map.get_point(current_row + 1, current_col)
            case Direction.LEFT:
                next_point = self.map.get_point(current_row, current_col - 1)

        if isinstance(next_point, Wall):
            self.moves_count += 1
            self.make_next_move()
        elif isinstance(next_point, Box):
            print('found a box')
            match next_direction:
                case Direction.UP:
                    next_next_point = self.map.get_point(next_point.row - 1, next_point.col)
                case Direction.RIGHT:
                    next_next_point = self.map.get_point(next_point.row, next_point.col + 1)
                case Direction.DOWN:
                    next_next_point = self.map.get_point(next_point.row + 1, next_point.col)
                case Direction.LEFT:
                    next_next_point = self.map.get_point(next_point.row, next_point.col - 1)
            if isinstance(next_next_point, Wall):
                self.moves_count += 1
                self.make_next_move()
            else:
                self.map.replace_point(self.point, Point(self.point.row, self.point.col, '.'))
                self.map.replace_point(next_point, Point(next_point.row, next_point.col, '@'))
                self.map.replace_point(next_next_point, Box(next_next_point.row, next_next_point.col, 'O'))
                self.moves_count += 1
                self.point = next_point
                self.make_next_move()
        else:
            self.moves_count += 1
            self.point = next_point
            self.make_next_move()


def ingest_data(filename: Path) -> tuple[Map, str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    map_lines = [line for line in line_list if line.startswith('#')]
    move_lines = [line for line in line_list if line != '' and not line.startswith('#')]
    moves_str = ''.join(line for line in move_lines)

    return (create_map(map_lines), moves_str)

def create_map_row(line: str, row_num: int, total_map_height: int) -> MapRow:
    point_list = []
    
    for col_num, char in enumerate(line):
        if char == '#':
            point_list.append(Wall(col_num, row_num, char))
        elif char == 'O':
            point_list.append(Box(col_num, row_num, char))
        else:
            point_list.append(Point(col_num, row_num, char))
            
    return MapRow(point_list, row_num, total_map_height)

def create_map(line_list: list[str]) -> Map:
    row_list = [create_map_row(line, row_num, len(line_list)) for row_num, line in enumerate(line_list)]
        
    return Map(row_list)

def find_robot(map: Map, moves_str: str) -> Robot:
    for row in map.row_list:
        for point in row.point_list:
            if point.char == '@':
                return Robot(point, map, moves_str)
    raise ValueError("Could not find a robot position in map.")


def part_one(filename: Path):
    map, moves_str = ingest_data(filename)
    # map.print()
    robot = find_robot(map, moves_str)
    robot.make_next_move()
    # robot.map.print()


def part_two(filename: Path):
    ...


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 10092
    # print(f"Part One (input):  {part_one(INPUT)}") # 
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") # 
    # print(f"Part Two (input):  {part_two(INPUT)}") # 

    # random_tests()



def random_tests():
    print(Direction('v'))


       


if __name__ == '__main__':
    main()