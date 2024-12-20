'''
--- Day 8: Resonant Collinearity ---

You find yourselves on the roof of a top-secret Easter Bunny installation.

While The Historians do their thing, you take a look at the familiar huge antenna. Much to your surprise, it seems to have been reconfigured to emit a signal that makes people 0.1% more likely to buy Easter Bunny brand Imitation Mediocre Chocolate as a Christmas gift! Unthinkable!

Scanning across the city, you find that there are actually many such antennas. Each antenna is tuned to a specific frequency indicated by a single lowercase letter, uppercase letter, or digit. You create a map (your puzzle input) of these antennas. For example:

............
........0...
.....0......
.......0....
....0.......
......A.....
............
............
........A...
.........A..
............
............

The signal only applies its nefarious effect at specific antinodes based on the resonant frequencies of the antennas. In particular, an antinode occurs at any point that is perfectly in line with two antennas of the same frequency - but only when one of the antennas is twice as far away as the other. This means that for any pair of antennas with the same frequency, there are two antinodes, one on either side of them.

So, for these two antennas with frequency a, they create the two antinodes marked with #:

..........
...#......
..........
....a.....
..........
.....a....
..........
......#...
..........
..........

Adding a third antenna with the same frequency creates several more antinodes. It would ideally add four antinodes, but two are off the right side of the map, so instead it adds only two:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......#...
..........
..........

Antennas with different frequencies don't create antinodes; A and a count as different frequencies. However, antinodes can occur at locations that contain antennas. In this diagram, the lone antenna with frequency capital A creates no antinodes but has a lowercase-a-frequency antinode at its location:

..........
...#......
#.........
....a.....
........a.
.....a....
..#.......
......A...
..........
..........

The first example has antennas with two different frequencies, so the antinodes they create look like this, plus an antinode overlapping the topmost A-frequency antenna:

......#....#
...#....0...
....#0....#.
..#....0....
....0....#..
.#....A.....
...#........
#......#....
........A...
.........A..
..........#.
..........#.

Because the topmost A-frequency antenna overlaps with a 0-frequency antinode, there are 14 total unique locations that contain an antinode within the bounds of the map.

Calculate the impact of the signal. How many unique locations within the bounds of the map contain an antinode?

'''

from pathlib import Path
from rich import print
from copy import deepcopy
from typing import NamedTuple, Protocol
from enum import Enum
from dataclasses import dataclass
from string import ascii_letters
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day8_example.txt'
INPUT = DATA_DIR / 'day8_input.txt'


@dataclass
class MapRow():
    string: str
    row_num: int

    @property
    def width(self) -> int:
        return len(self.string)

    def get_point(self, col_num: int) -> str:
        return self.string[col_num]

@dataclass
class MapColumn():
    string: str
    col_num: int

    @property
    def height(self) -> int:
        return len(self.string)

    def get_point(self, row_num: int) -> str:
        return self.string[row_num]

@dataclass
class MapDiagonal():
    string: str

    def get_point(self, num: int) -> str:
        return self.string[num]


@dataclass
class Map():
    row_list: list[MapRow]

    @property
    def height(self) -> int:
        return len(self.row_list)

    @property
    def width(self) -> int:
        return self.row_list[0].width

    @property
    def col_list(self) -> list[MapColumn]:
        output_list = []
        for i, row in enumerate(self.row_list):
            output_list.append(MapColumn(
                                string=''.join(row.string[i] for row in self.row_list),
                                col_num=i
                            ))
        return output_list

    @property
    def diagonal_list(self) -> list[MapDiagonal]:
        num_columns = self.width
        num_rows = self.height 

        row_strings = [list(row.string) for row in self.row_list]

        output_list = []
        
        df = pd.DataFrame(row_strings)
        for x in range(0-num_rows, num_columns-1):
            output_list.append(MapDiagonal(string=''.join(x for x in np.diag(df, k=x))))

        df2 = df.iloc[::-1].reset_index(drop=True)
        for x in range(0-num_rows, num_columns-1):
            output_list.append(MapDiagonal(string=''.join(x for x in np.diag(df, k=x))))

        return output_list
        
    def get_row(self, row_num: int) -> MapRow:
        return self.row_list[row_num]

    def get_column(self, col_num: int) -> MapColumn:
        return self.col_list[col_num]

    def get_point(self, row_num: int, col_num: int) -> str:
        row = self.row_list[row_num]
        return row.get_point(col_num)

    def find_antinodes(self):
        for row in self.row_list:
            antennas = [char for char in row.string if char.isalnum()]
            repeated_antennas = [char for char in antennas if antennas.count(char) > 1]
            print(repeated_antennas)

        for col in self.col_list:
            antennas = [char for char in col.string if char.isalnum()]
            repeated_antennas = [char for char in antennas if antennas.count(char) > 1]
            print(repeated_antennas)

        for diag in self.diagonal_list:
            antennas = [char for char in diag.string if char.isalnum()]
            repeated_antennas = [char for char in antennas if antennas.count(char) > 1]
            print(repeated_antennas)

def create_map_row(line: str, row_num: int) -> MapRow:
    return MapRow(line, row_num)

def create_map(filename: Path) -> Map:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    row_list = [create_map_row(line, row_num) for row_num, line in enumerate(line_list)]
        
    return Map(row_list)

def part_one(filename: Path) -> int:
    map = create_map(filename)
    print(map.row_list)
    print(map.col_list)
    print(map.diagonal_list)
    map.find_antinodes()

def part_two(filename: Path) -> int:
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    # print(f"Part One (input):  {part_one(INPUT)}")
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}")
    # print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()