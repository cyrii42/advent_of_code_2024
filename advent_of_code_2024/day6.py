'''
--- Day 6: Guard Gallivant ---
The Historians use their fancy device again, this time to whisk you all away to the North Pole prototype suit manufacturing lab... in the year 1518! It turns out that having direct access to history is very convenient for a group of historians.

You still have to be careful of time paradoxes, and so it will be important to avoid anyone from 1518 while The Historians search for the Chief. Unfortunately, a single guard is patrolling this part of the lab.

Maybe you can work out where the guard will go ahead of time so that The Historians can search safely?

You start by making a map (your puzzle input) of the situation. For example:

....#.....
.........#
..........
..#.......
.......#..
..........
.#..^.....
........#.
#.........
......#...

The map shows the current position of the guard with ^ (to indicate the guard is currently facing up from the perspective of the map). Any obstructions - crates, desks, alchemical reactors, etc. - are shown as #.

Lab guards in 1518 follow a very strict patrol protocol which involves repeatedly following these steps:

If there is something directly in front of you, turn right 90 degrees.
Otherwise, take a step forward.
Following the above protocol, the guard moves up several times until she reaches an obstacle (in this case, a pile of failed suit prototypes):

....#.....
....^....#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Because there is now an obstacle in front of the guard, she turns right before continuing straight in her new facing direction:

....#.....
........>#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#...

Reaching another obstacle (a spool of several very long polymers), she turns right again and continues downward:

....#.....
.........#
..........
..#.......
.......#..
..........
.#......v.
........#.
#.........
......#...

This process continues for a while, but the guard eventually leaves the mapped area (after walking past a tank of universal solvent):

....#.....
.........#
..........
..#.......
.......#..
..........
.#........
........#.
#.........
......#v..

By predicting the guard's route, you can determine which specific positions in the lab will be in the patrol path. Including the guard's starting position, the positions visited by the guard before leaving the area are marked with an X:

....#.....
....XXXXX#
....X...X.
..#.X...X.
..XXXXX#X.
..X.X.X.X.
.#XXXXXXX.
.XXXXXXX#.
#XXXXXXX..
......#X..

In this example, the guard will visit 41 distinct positions on your map.

Predict the path of the guard. How many distinct positions will the guard visit before leaving the mapped area?

--- Part Two ---
While The Historians begin working around the guard's patrol route, you borrow their fancy device and step outside the lab. From the safety of a supply closet, you time travel through the last few months and record the nightly status of the lab's guard post on the walls of the closet.

Returning after what seems like only a few seconds to The Historians, they explain that the guard's patrol area is simply too large for them to safely search the lab without getting caught.

Fortunately, they are pretty sure that adding a single new obstruction won't cause a time paradox. They'd like to place the new obstruction in such a way that the guard will get stuck in a loop, making the rest of the lab safe to search.

To have the lowest chance of creating a time paradox, The Historians would like to know all of the possible positions for such an obstruction. The new obstruction can't be placed at the guard's starting position - the guard is there right now and would notice.

In the above example, there are only 6 different positions where a new obstruction would cause the guard to get stuck in a loop. The diagrams of these six situations use O to mark the new obstruction, | to show a position where the guard moves up/down, - to show a position where the guard moves left/right, and + to show a position where the guard moves both up/down and left/right.

Option one, put a printing press next to the guard's starting position:

....#.....
....+---+#
....|...|.
..#.|...|.
....|..#|.
....|...|.
.#.O^---+.
........#.
#.........
......#...

Option two, put a stack of failed suit prototypes in the bottom right quadrant of the mapped area:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
......O.#.
#.........
......#...

Option three, put a crate of chimney-squeeze prototype fabric next to the standing desk in the bottom right quadrant:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----+O#.
#+----+...
......#...

Option four, put an alchemical retroencabulator near the bottom left corner:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
..|...|.#.
#O+---+...
......#...

Option five, put the alchemical retroencabulator a bit to the right instead:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
....|.|.#.
#..O+-+...
......#...

Option six, put a tank of sovereign glue right next to the tank of universal solvent:

....#.....
....+---+#
....|...|.
..#.|...|.
..+-+-+#|.
..|.|.|.|.
.#+-^-+-+.
.+----++#.
#+----++..
......#O..

It doesn't really matter what you choose to use as an obstacle so long as you and The Historians can put it into position without the guard noticing. The important thing is having enough options that you can find one that minimizes time paradoxes, and in this example, there are 6 different positions you could choose.

You need to get the guard stuck in a loop by adding a single new obstruction. How many different positions could you choose for this obstruction?
'''

import datetime as dt
from pathlib import Path
from rich import print
from copy import deepcopy
from typing import NamedTuple, Optional
from enum import Enum
from dataclasses import dataclass, field
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day6_example.txt'
INPUT = DATA_DIR / 'day6_input.txt'

class Point(NamedTuple):
    col: int
    row: int
    char: str

class Obstacle(Point):
    ...

class MapEdge(Point):
    ...

class Direction(Enum):
    UP = 0
    RIGHT = 1
    DOWN = 2
    LEFT = 3

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

    def get_row(self, y: int) -> MapRow:
        return self.row_list[y]

    def get_point(self, row_num: int, col_num: int) -> Point:
        row = self.row_list[row_num]
        return row.get_point(col_num)

    
@dataclass
class Guard():
    point: Point
    map: Map = field(repr=False)
    total_positions: int = field(default=1, repr=False)
    loop_found: bool = field(default=False, repr=False)
    just_avoided_obstacle: int = field(default=0, repr=False)
    positions_visited: set[Point] = field(default_factory=set, repr=False)
    positions_visited_list: list[Point] = field(default_factory=list, repr=False)

    def __post_init__(self):
        self.direction = self.get_initial_direction()
        self.positions_visited.add(self.point)

    def get_initial_direction(self) -> Direction:
        match self.point.char:
            case '^':
                return Direction.UP
            case '>':
                return Direction.RIGHT
            case 'v':
                return Direction.DOWN
            case '<':
                return Direction.LEFT
            case _:
                raise ValueError

    def rotate(self) -> int:
        try:
            new_value = (self.direction.value + 1) % 4
            self.direction = Direction(new_value)
            return 0
        except RecursionError:
            print('aaa')
            return 1

    def increment_position_counter(self, next_point: Point) -> int:
        # print(f"Incrementing counter for point {next_point}")
        if not next_point in self.positions_visited:
            self.total_positions += 1
            self.positions_visited.add(next_point)
            self.positions_visited_list.append(next_point)
            return 0
        else:
            self.positions_visited_list.append(next_point)
            if len(self.positions_visited_list) - len(self.positions_visited) > 30000:
                print(f"Found a loop @ {dt.datetime.now()}")
                return 1
            # print(f"Set length: {len(self.positions_visited)} - list length: {len(self.positions_visited_list)} @ {dt.datetime.now()}")
            return 0
        
    def find_next_point(self) -> Point:
        ''' Determine the next point based on current direction.  If next point is an obstacle, rotate and try again.'''

        current_row = self.point.row
        current_col = self.point.col
        match self.direction:
            case Direction.UP:
                next_point = self.map.get_point(current_row - 1, current_col)
            case Direction.RIGHT:
                next_point = self.map.get_point(current_row, current_col + 1)
            case Direction.DOWN:
                next_point = self.map.get_point(current_row + 1, current_col)
            case Direction.LEFT:
                next_point = self.map.get_point(current_row, current_col - 1)
                
        if isinstance(next_point, Obstacle):
            # print(f"Current position: ({self.point.row}, {self.point.col}).  Obstacle at ({next_point.row}, {next_point.col})!  Rotating...")
                if self.rotate() == 1:
                    return 1
                else:
                    return self.find_next_point()
        else:
            # print(f"Current position: ({self.point.row}, {self.point.col}).  Moving to ({next_point.row}, {next_point.col}).  (total positions: {self.total_positions})")
            result = self.increment_position_counter(next_point)
            if result == 0:
                return next_point
            else:
                return result

    def patrol(self) -> int:
        ''' If current position is an edge of the map, we're done, so return the total moves. 
        Otherwise, increment `total_positions`, move to the next position, and try again.'''
        while True:
            if isinstance(self.map.get_point(self.point.row, self.point.col), MapEdge):
                # print(f"Found exit!  Position:  ({self.point.row}, {self.point.col})")
                return self.total_positions
            else:
                result = self.find_next_point()
                if isinstance(result, int):
                    return result
                else:
                    self.point = self.find_next_point()

    def patrol_part_two(self) -> int:
        ''' If current position is an edge of the map, we're done, so return the total moves. 
        Otherwise, increment `total_positions`, move to the next position, and try again.'''
        while True:
            if isinstance(self.map.get_point(self.point.row, self.point.col), MapEdge):
                # print(f"Found exit!  Position:  ({self.point.row}, {self.point.col}) (total positions: {self.total_positions})")
                return 0
            else:
                result = self.find_next_point()
                if isinstance(result, Point):
                    self.point = result
                else:
                    return 1
                
def find_loops(first_guard: Guard, points_to_check: list[Point]) -> int:
    total = 0
    for visited_point in points_to_check:
        print(f"Checking ({visited_point.col}, {visited_point.row})")
        new_map = Map(deepcopy(first_guard.map.row_list))
        new_obstacle = Obstacle(visited_point.col, visited_point.row, '#')
        new_map.row_list[visited_point.row].point_list[visited_point.col] = new_obstacle
        # print(new_map)
        new_guard = find_guard(new_map)
        result = new_guard.patrol_part_two()
        # print(result)
        total += result
    return total
            



def find_guard(map: Map) -> Guard:
    for y, row in enumerate(map.row_list):
        for x, point in enumerate(row.point_list):
            if point.char in ['^', '>', '<', 'v']:
                return Guard(point, map)
    raise ValueError


def create_map_row(line: str, row_num: int, total_map_height: int) -> MapRow:
    total_map_width = len(line)
    point_list = []
    for col_num, char in enumerate(line):
        if char == '#':
            point_list.append(Obstacle(col_num, row_num, char))
        elif row_num == 0 or row_num == (total_map_height - 1) or col_num == 0 or col_num == (total_map_width - 1):
            point_list.append(MapEdge(col_num, row_num, char))
        else:
            point_list.append(Point(col_num, row_num, char))
            
    return MapRow(point_list, row_num, total_map_height)


def create_map(filename: Path) -> Map:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    row_list = [create_map_row(line, row_num, len(line_list)) for row_num, line in enumerate(line_list)]
        
    return Map(row_list)


def part_one(filename: Path) -> int:
    map = create_map(filename)
    guard = find_guard(map)
    answer = guard.patrol()
    return answer


def part_two(filename: Path) -> int:
    map = create_map(filename)
    guard = find_guard(map)
    guard.patrol()

    points_to_check = [point for point in guard.positions_visited if not isinstance(point, Obstacle) and point.char not in ['^', '>', '<', 'v']]
    answer = find_loops(guard, points_to_check)
    return answer


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 41
    print(f"Part One (input):  {part_one(INPUT)}") # 5162
    # print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 6
    print(f"Part Two (input):  {part_two(INPUT)}") # 1909


if __name__ == '__main__':
    main()