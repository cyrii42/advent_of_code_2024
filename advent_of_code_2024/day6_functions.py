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
'''

from pathlib import Path
from rich import print
from advent_of_code_2024.constants import DATA_DIR
from advent_of_code_2024.day6_classes import Point, Obstacle, MapEdge, Direction, Guard, Map, MapRow

EXAMPLE = DATA_DIR / 'day6_example.txt'
INPUT = DATA_DIR / 'day6_input.txt'
                



def get_direction(str_value: str) -> Direction:
        match str_value:
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

def find_guard(map: Map) -> Guard:
    for y, row in enumerate(map.row_list):
        for x, point in enumerate(row.point_list):
            if point.char in ['^', '>', '<', 'v']:
                return Guard(x, y, map, get_direction(point.char))
    raise ValueError


def create_map_row(line: str, row_num: int) -> MapRow:
    point_list = []
    for x, char in enumerate(line):
        if x == 0 or x == (len(line) - 1):
            point_list.append(MapEdge(x=x, y=row_num, char=char))       ##### THIS NEEDS TO BE FIXED
        if char == '#':
            point_list.append(Obstacle(x=x, y=row_num, char=char))
        else:
            point_list.append(Point(x=x, y=row_num, char=char))
            
    return MapRow(point_list)


def create_map(filename: Path) -> Map:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    row_list = []
    for row_num, line in enumerate(line_list):
        row_list.append(create_map_row(line, row_num))
        
    return Map(row_list)



def part_one(filename: Path) -> int:
    map = create_map(filename)
    guard = find_guard(map)
    print(map)
    print(guard)


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