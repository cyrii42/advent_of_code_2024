'''
--- Day 10: Hoof It ---

You all arrive at a Lava Production Facility on a floating island in the sky. As the others begin to search the massive industrial complex, you feel a small nose boop your leg and look down to discover a reindeer wearing a hard hat.

The reindeer is holding a book titled "Lava Island Hiking Guide". However, when you open the book, you discover that most of it seems to have been scorched by lava! As you're about to ask how you can help, the reindeer brings you a blank topographic map of the surrounding area (your puzzle input) and looks up at you excitedly.

Perhaps you can help fill in the missing hiking trails?

The topographic map indicates the height at each position using a scale from 0 (lowest) to 9 (highest). For example:

0123
1234
8765
9876

Based on un-scorched scraps of the book, you determine that a good hiking trail is as long as possible and has an even, gradual, uphill slope. For all practical purposes, this means that a hiking trail is any path that starts at height 0, ends at height 9, and always increases by a height of exactly 1 at each step. Hiking trails never include diagonal steps - only up, down, left, or right (from the perspective of the map).

You look up from the map and notice that the reindeer has helpfully begun to construct a small pile of pencils, markers, rulers, compasses, stickers, and other equipment you might need to update the map with hiking trails.

A trailhead is any position that starts one or more hiking trails - here, these positions will always have height 0. Assembling more fragments of pages, you establish that a trailhead's score is the number of 9-height positions reachable from that trailhead via a hiking trail. In the above example, the single trailhead in the top left corner has a score of 1 because it can reach a single 9 (the one in the bottom left).

This trailhead has a score of 2:

...0...
...1...
...2...
6543456
7.....7
8.....8
9.....9

(The positions marked . are impassable tiles to simplify these examples; they do not appear on your actual topographic map.)

This trailhead has a score of 4 because every 9 is reachable via a hiking trail except the one immediately to the left of the trailhead:

..90..9
...1.98
...2..7
6543456
765.987
876....
987....

This topographic map contains two trailheads; the trailhead at the top has a score of 1, while the trailhead at the bottom has a score of 2:

10..9..
2...8..
3...7..
4567654
...8..3
...9..2
.....01

Here's a larger example:

89010123
78121874
87430965
96549874
45678903
32019012
01329801
10456732

This larger example has 9 trailheads. Considering the trailheads in reading order, they have scores of 5, 6, 5, 3, 1, 3, 5, 3, and 5. Adding these scores together, the sum of the scores of all trailheads is 36.

The reindeer gleefully carries over a protractor and adds it to the pile. What is the sum of the scores of all trailheads on your topographic map?

'''

from pathlib import Path
from rich import print
from pprint import pprint
from copy import deepcopy
from typing import NamedTuple, Protocol, Optional
from enum import Enum
from dataclasses import dataclass, field
from string import ascii_letters
import itertools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day10_example.txt'
INPUT = DATA_DIR / 'day10_input.txt'

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3
    
@dataclass(frozen=True)
class Position():
    row_num: int
    col_num: int
    height: int

@dataclass(frozen=True)
class Trailhead(Position):
    ...

@dataclass
class MapRow():
    row_num: int
    position_list: list[Position]
    total_map_height: int = field(repr=False)

    @property
    def width(self):
        return len(self.position_list)

    def get_position(self, col_num: int) -> Position | None:
        if col_num >= self.total_map_height:
            return None
        else:
            return self.position_list[col_num]

@dataclass
class Map():
    row_list: list[MapRow]

    @property
    def height(self):
        return len(self.row_list)

    @property
    def width(self):
        return self.row_list[0].width

    @property
    def positions(self):
        return [position for row in self.row_list for position in row.position_list]

    @property
    def trailheads(self):
        return [position for position in self.positions if isinstance(position, Trailhead)]

    def get_row(self, row_num: int) -> MapRow:
        return self.row_list[row_num]

    def get_position(self, row_num: int, col_num: int) -> Position | None:
        if row_num >= self.width or col_num >= self.height:
            return None
        else:
            row = self.row_list[row_num]
            return row.get_position(col_num)

    def find_hiking_trails(self) -> int:
        total = 0
        for trailhead in self.trailheads:
            total += self.score_trailhead(trailhead)
        return total

    def score_trailhead(self, trailhead: Trailhead) -> int:
        hiker = Hiker(trailhead, self)
        hiker.find_trails()
        trailhead_score = hiker.hiking_trails_found
        print(f"Trailhead score: {trailhead_score}")
        return trailhead_score

@dataclass
class Hiker():
    position: Position
    map: Map = field(repr=False)
    positions_visited: set[Position] = field(default_factory=set, repr=False)
    hiking_trails_found: int = 0
        
    def find_next_position(self, direction: Direction) -> Position | None:
        ''' Determine the next position based on input direction.'''
        current_row = self.position.row_num
        current_col = self.position.col_num
        
        match direction:
            case Direction.UP:
                next_position = self.map.get_position(current_row - 1, current_col)
            case Direction.RIGHT:
                next_position = self.map.get_position(current_row, current_col + 1)
            case Direction.DOWN:
                next_position = self.map.get_position(current_row + 1, current_col)
            case Direction.LEFT:
                next_position = self.map.get_position(current_row, current_col - 1)
                
        return next_position
 
    def find_trails(self) -> bool:
        for direction in Direction:
            next_position = self.find_next_position(direction)
            if next_position is None:
                # print("hit a wall")
                continue
            elif self.position.height == 8 and next_position.height == 9:
                # print("Found a trail!")
                self.hiking_trails_found += 1
                # return True  # we found a valid trail!
            elif self.position.height + 1 == next_position.height:
                self.position = next_position
                return self.find_trails()
            # else:
                # print("booop")
                # return False
        return False

def create_map_row(line: str, row_num: int, total_map_height: int) -> MapRow:
    position_list = []
    for col_num, char in enumerate(line):
        if char == '0':
            position_list.append(Trailhead(row_num, col_num, int(char)))
        else:
            position_list.append(Position(row_num, col_num, int(char)))
    return MapRow(row_num, position_list, total_map_height)


def create_map(filename: Path) -> Map:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    row_list = [create_map_row(line, row_num, len(line_list)) for row_num, line in enumerate(line_list)]
    return Map(row_list)

def part_one(filename: Path):
    map = create_map(filename)
    return map.find_hiking_trails()


def part_two(filename: Path):
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 
    # print(f"Part One (input):  {part_one(INPUT)}") # 
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") # 
    # print(f"Part Two (input):  {part_two(INPUT)}") # 




    


if __name__ == '__main__':
    main()