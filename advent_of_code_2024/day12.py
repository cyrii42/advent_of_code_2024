'''
--- Day 12: Garden Groups ---

Why not search for the Chief Historian near the gardener and his massive farm? There's plenty of food, so The Historians grab something to eat while they search.

You're about to settle near a complex arrangement of garden plots when some Elves ask if you can lend a hand. They'd like to set up fences around each region of garden plots, but they can't figure out how much fence they need to order or how much it will cost. They hand you a map (your puzzle input) of the garden plots.

Each garden plot grows only a single type of plant and is indicated by a single letter on your map. When multiple garden plots are growing the same type of plant and are touching (horizontally or vertically), they form a region. For example:

AAAA
BBCD
BBCC
EEEC

This 4x4 arrangement includes garden plots growing five different types of plants (labeled A, B, C, D, and E), each grouped into their own region.

In order to accurately calculate the cost of the fence around a single region, you need to know that region's area and perimeter.

The area of a region is simply the number of garden plots the region contains. The above map's type A, B, and C plants are each in a region of area 4. The type E plants are in a region of area 3; the type D plants are in a region of area 1.

Each garden plot is a square and so has four sides. The perimeter of a region is the number of sides of garden plots in the region that do not touch another garden plot in the same region. The type A and C plants are each in a region with perimeter 10. The type B and E plants are each in a region with perimeter 8. The lone D plot forms its own region with perimeter 4.

Visually indicating the sides of plots in each region that contribute to the perimeter using - and |, the above map's regions' perimeters are measured as follows:

+-+-+-+-+
|A A A A|
+-+-+-+-+     +-+
              |D|
+-+-+   +-+   +-+
|B B|   |C|
+   +   + +-+
|B B|   |C C|
+-+-+   +-+ +
          |C|
+-+-+-+   +-+
|E E E|
+-+-+-+

Plants of the same type can appear in multiple separate regions, and regions can even appear within other regions. For example:

OOOOO
OXOXO
OOOOO
OXOXO
OOOOO

The above map contains five regions, one containing all of the O garden plots, and the other four each containing a single X plot.

The four X regions each have area 1 and perimeter 4. The region containing 21 type O plants is more complicated; in addition to its outer edge contributing a perimeter of 20, its boundary with each X region contributes an additional 4 to its perimeter, for a total perimeter of 36.

Due to "modern" business practices, the price of fence required for a region is found by multiplying that region's area by its perimeter. The total price of fencing all regions on a map is found by adding together the price of fence for every region on the map.

In the first example, region A has price 4 * 10 = 40, region B has price 4 * 8 = 32, region C has price 4 * 10 = 40, region D has price 1 * 4 = 4, and region E has price 3 * 8 = 24. So, the total price for the first example is 140.

In the second example, the region with all of the O plants has price 21 * 36 = 756, and each of the four smaller X regions has price 1 * 4 = 4, for a total price of 772 (756 + 4 + 4 + 4 + 4).

Here's a larger example:

RRRRIICCFF
RRRRIICCCF
VVRRRCCFFF
VVRCCCJFFF
VVVVCJJCFE
VVIVCCJJEE
VVIIICJJEE
MIIIIIJJEE
MIIISIJEEE
MMMISSJEEE

It contains:

    A region of R plants with price 12 * 18 = 216.
    A region of I plants with price 4 * 8 = 32.
    A region of C plants with price 14 * 28 = 392.
    A region of F plants with price 10 * 18 = 180.
    A region of V plants with price 13 * 20 = 260.
    A region of J plants with price 11 * 20 = 220.
    A region of C plants with price 1 * 4 = 4.
    A region of E plants with price 13 * 18 = 234.
    A region of I plants with price 14 * 22 = 308.
    A region of M plants with price 5 * 12 = 60.
    A region of S plants with price 3 * 8 = 24.

So, it has a total price of 1930.

What is the total price of fencing all regions on your map?

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
import functools
import pandas as pd
import numpy as np
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day12_example.txt'
INPUT = DATA_DIR / 'day12_input.txt'

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        return f.read().split()

class EdgeType(Enum):
    NON_EDGE = 0
    SINGLE_EDGE = 1
    UPPER_RIGHT_CORNER = 2
    UPPER_LEFT_CORNER = 3
    LOWER_RIGHT_CORNER = 4
    LOWER_LEFT_CORNER = 5
    PENINSULA = 6
    SINGLE_POINT_PLOT = 7

@dataclass
class Point():
    row_num: int
    col_num: int
    char: str
    up: Optional[str] = None
    right: Optional[str] = None
    down: Optional[str] = None
    left: Optional[str] = None
    edge_count: Optional[int] = None
    edge_type: Optional[EdgeType] = None

    @property
    def all_neighbor_chars(self) -> list[str | None]:
        return [self.up, self.right, self.down, self.left]

    def get_edge_type(self) -> EdgeType:
        if self.edge_count == 4:
            return EdgeType.SINGLE_POINT_PLOT
        if self.edge_count == 3:
            return EdgeType.PENINSULA
        if self.edge_count == 2:
            if (self.up is None or self.up != self.char) and (self.right is None or self.right != self.char):
                return EdgeType.UPPER_RIGHT_CORNER
            if (self.up is None or self.up != self.char) and (self.left is None or self.left != self.char):
                return EdgeType.UPPER_LEFT_CORNER
            if (self.down is None or self.down != self.char) and (self.right is None or self.right != self.char):
                return EdgeType.LOWER_RIGHT_CORNER
            if (self.down is None or self.down != self.char) and (self.left is None or self.left != self.char):
                return EdgeType.LOWER_LEFT_CORNER
            else:
                return EdgeType.SINGLE_EDGE
        if self.edge_count == 1:
            return EdgeType.SINGLE_EDGE
        if self.edge_count == 0:
            return EdgeType.NON_EDGE
        else:
            raise ValueError(f"{self}")
        


@dataclass(frozen=True)
class GardenPlot():
    point_list: list[Point]

    @property
    def total_edges(self) -> int:
        return sum(point.edge_count for point in self.point_list if point.edge_count is not None)

    @property
    def area(self) -> int:
        return len(self.point_list)

    @property
    def total_price(self) -> int:
        return self.area * self.total_edges

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

@dataclass
class MapRow():
    point_list: list[Point]
    row_num: int

    @property
    def width(self):
        return len(self.point_list)

    def get_point(self, col_num: int) -> Point:
        return self.point_list[col_num]


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
    def all_points(self) -> list[Point]:
        return [point for row in self.row_list for point in row.point_list]

    @property
    def all_plant_types(self) -> list[str]:
        return sorted(list(set([point.char for point in self.all_points])))

    @property
    def total_edges(self) -> int:
        return sum(point.edge_count for point in self.all_points if point.edge_count is not None)

    @property
    def total_price(self) -> int:
        return self.total_edges * len(self.all_points)

    def __post_init__(self):
        self.find_neighbors()

    def get_row(self, col_num: int) -> MapRow:
        return self.row_list[col_num]

    def get_point(self, row_num: int, col_num: int) -> Point | None:
        if row_num < 0 or col_num < 0:
            return None
        if row_num >= self.width or col_num >= self.height:
            return None
        row = self.row_list[row_num]
        return row.get_point(col_num)

    def find_neighbors(self) -> None:
        for point in self.all_points:
            current_row = point.row_num
            current_col = point.col_num
            
            up = self.get_point(current_row - 1, current_col)
            right = self.get_point(current_row, current_col + 1)
            down = self.get_point(current_row + 1, current_col)
            left = self.get_point(current_row, current_col - 1)
                    
            point.up = up.char if up is not None else None
            point.right = right.char if right is not None else None
            point.down = down.char if down is not None else None
            point.left = left.char if left is not None else None

            all_neighbors = [up, right, down, left]
            point.edge_count = len([neighbor for neighbor in all_neighbors if neighbor is None or neighbor.char != point.char])
            point.edge_type = point.get_edge_type()
            # if any(x is None for x in all_neighbors):
            #     point.plot_edge = True
            # elif any(x.char != up.char for x in all_neighbors): # type: ignore
            #     point.plot_edge = True
            # else:
            #     point.plot_edge = False


    def calculate_total_price(self) -> int:
        ...

@dataclass
class PlotFinder():
    current_point: Point
    map: Map = field(repr=False)
    plots_found: set[GardenPlot]
    points_visited: list[Point]
        
    def find_next_point(self, direction: Direction) -> Point | None:
        ''' Determine the next point based on input direction.'''
        current_row = self.current_point.row_num
        current_col = self.current_point.col_num
        
        match direction:
            case Direction.UP:
                next_point = self.map.get_point(current_row - 1, current_col)
            case Direction.RIGHT:
                next_point = self.map.get_point(current_row, current_col + 1)
            case Direction.DOWN:
                next_point = self.map.get_point(current_row + 1, current_col)
            case Direction.LEFT:
                next_point = self.map.get_point(current_row, current_col - 1)

        if next_point is None:
            return None
        else:
            return next_point
 
    def find_plots(self) -> None:
        next_points = [self.find_next_point(direction) for direction in Direction]
        for point in next_points:
            if not point:
                continue

            self.points_visited.append(point)
                
            if not any(x == self.current_point.char for x in [point.all_neighbor_chars]):
                ...
                
            self.current_point = point
            self.points_visited.append(point)
            self.find_plots()
        return None


def create_map_row(line: str, row_num: int, total_map_height: int) -> MapRow:
    total_map_width = len(line)
    point_list = []
    
    for col_num, char in enumerate(line):
        if row_num == 0 or row_num == (total_map_height - 1) or col_num == 0 or col_num == (total_map_width - 1):
            point_list.append(Point(row_num=row_num, 
                                    col_num=col_num, 
                                    char=char))
        else:
            point_list.append(Point(row_num=row_num, 
                                    col_num=col_num, 
                                    char=char))
            
    return MapRow(point_list, row_num)


def create_map(filename: Path) -> Map:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    row_list = [create_map_row(line, row_num, len(line_list)) for row_num, line in enumerate(line_list)]
        
    return Map(row_list)


def part_one(filename: Path):
    map = create_map(filename)
    print(map)
    print(map.all_plant_types)
    print(map.total_price)
    print(map.all_points)
    for point in map.all_points:
        print(point.edge_type, point.char)


def part_two(filename: Path):
    ...


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 1930
    # print(f"Part One (input):  {part_one(INPUT)}") # 
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") # 
    # print(f"Part Two (input):  {part_two(INPUT)}") # 

    # random_tests()


def random_tests():
    ...



       


if __name__ == '__main__':
    main()