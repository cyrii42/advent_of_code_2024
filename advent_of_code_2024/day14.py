'''
--- Day 14: Restroom Redoubt ---
One of The Historians needs to use the bathroom; fortunately, you know there's a bathroom near an unvisited location on their list, and so you're all quickly teleported directly to the lobby of Easter Bunny Headquarters.

Unfortunately, EBHQ seems to have "improved" bathroom security again after your last visit. The area outside the bathroom is swarming with robots!

To get The Historian safely to the bathroom, you'll need a way to predict where the robots will be in the future. Fortunately, they all seem to be moving on the tile floor in predictable straight lines.

You make a list (your puzzle input) of all of the robots' current positions (p) and velocities (v), one robot per line. For example:

p=0,4 v=3,-3
p=6,3 v=-1,-3
p=10,3 v=-1,2
p=2,0 v=2,-1
p=0,0 v=1,3
p=3,0 v=-2,-2
p=7,6 v=-1,-3
p=3,0 v=-1,-2
p=9,3 v=2,3
p=7,3 v=-1,2
p=2,4 v=2,-3
p=9,5 v=-3,-3

Each robot's position is given as p=x,y where x represents the number of tiles the robot is from the left wall and y represents the number of tiles from the top wall (when viewed from above). So, a position of p=0,0 means the robot is all the way in the top-left corner.

Each robot's velocity is given as v=x,y where x and y are given in tiles per second. Positive x means the robot is moving to the right, and positive y means the robot is moving down. So, a velocity of v=1,-2 means that each second, the robot moves 1 tile to the right and 2 tiles up.

The robots outside the actual bathroom are in a space which is 101 tiles wide and 103 tiles tall (when viewed from above). However, in this example, the robots are in a space which is only 11 tiles wide and 7 tiles tall.

The robots are good at navigating over/under each other (due to a combination of springs, extendable legs, and quadcopters), so they can share the same tile and don't interact with each other. Visually, the number of robots on each tile in this example looks like this:

1.12.......
...........
...........
......11.11
1.1........
.........1.
.......1...

These robots have a unique feature for maximum bathroom security: they can teleport. When a robot would run into an edge of the space they're in, they instead teleport to the other side, effectively wrapping around the edges. Here is what robot p=2,4 v=2,-3 does for the first few seconds:

Initial state:
...........
...........
...........
...........
..1........
...........
...........

After 1 second:
...........
....1......
...........
...........
...........
...........
...........

After 2 seconds:
...........
...........
...........
...........
...........
......1....
...........

After 3 seconds:
...........
...........
........1..
...........
...........
...........
...........

After 4 seconds:
...........
...........
...........
...........
...........
...........
..........1

After 5 seconds:
...........
...........
...........
.1.........
...........
...........
...........

The Historian can't wait much longer, so you don't have to simulate the robots for very long. Where will the robots be after 100 seconds?

In the above example, the number of robots on each tile after 100 seconds has elapsed looks like this:

......2..1.
...........
1..........
.11........
.....1.....
...12......
.1....1....

To determine the safest area, count the number of robots in each quadrant after 100 seconds. Robots that are exactly in the middle (horizontally or vertically) don't count as being in any quadrant, so the only relevant robots are:

..... 2..1.
..... .....
1.... .....
           
..... .....
...12 .....
.1... 1....

In this example, the quadrants contain 1, 3, 4, and 1 robot. Multiplying these together gives a total safety factor of 12.

Predict the motion of the robots in your list within a space which is 101 tiles wide and 103 tiles tall. What will the safety factor be after exactly 100 seconds have elapsed?

--- Part Two ---
During the bathroom break, someone notices that these robots seem awfully similar to ones built and used at the North Pole. If they're the same type of robots, they should have a hard-coded Easter egg: very rarely, most of the robots should arrange themselves into a picture of a Christmas tree.

What is the fewest number of seconds that must elapse for the robots to display the Easter egg?
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

EXAMPLE = DATA_DIR / 'day14_example.txt'
INPUT = DATA_DIR / 'day14_input.txt'

SPACE_WIDTH = 101
SPACE_HEIGHT = 103

@dataclass
class Robot():
    px: int
    py: int
    vx: int
    vy: int

    @property
    def quadrant(self) -> int:
        midpoint_x = SPACE_WIDTH // 2
        midpoint_y = SPACE_HEIGHT // 2
        if self.px < midpoint_x and self.py < midpoint_y:
            return 1
        if self.px > midpoint_x and self.py < midpoint_y:
            return 2
        if self.px < midpoint_x and self.py > midpoint_y:
            return 3
        if self.px > midpoint_x and self.py > midpoint_y:
            return 4
        return 0

    def move(self, moves: int) -> None:
        for _ in range(moves):
            self.px = (self.px + self.vx) % SPACE_WIDTH
            self.py = (self.py + self.vy) % SPACE_HEIGHT
        

def ingest_data(filename: Path) -> list[Robot]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    return [process_robot_data(data) for data in line_list]

def process_robot_data(data: str) -> Robot:
    position_str = data.split(' ')[0].removeprefix('p=')
    position_ints = [int(x) for x in position_str.split(',')]
        
    velocity_str = data.split(' ')[1].removeprefix('v=')
    velocity_ints = [int(x) for x in velocity_str.split(',')]

    return Robot(position_ints[0], position_ints[1], velocity_ints[0], velocity_ints[1])

def determine_safety_factor(robot_list: list[Robot]) -> int:
    quadrant_1 = len([robot for robot in robot_list if robot.quadrant == 1])
    quadrant_2 = len([robot for robot in robot_list if robot.quadrant == 2])
    quadrant_3 = len([robot for robot in robot_list if robot.quadrant == 3])
    quadrant_4 = len([robot for robot in robot_list if robot.quadrant == 4])

    return quadrant_1 * quadrant_2 * quadrant_3 * quadrant_4

def find_christmas_tree(robot_list: list[Robot]) -> int:
    ...
        

def part_one(filename: Path):
    robot_list = ingest_data(filename)
    for robot in robot_list:
        robot.move(100)
    return determine_safety_factor(robot_list)
    


def part_two(filename: Path):
    ...


def main():
    # print(f"Part One (example):  {part_one(EXAMPLE)}") # 12
    print(f"Part One (input):  {part_one(INPUT)}") # 226236192
    # print()
    # print(f"Part Two (example):  {part_two(EXAMPLE)}") # 
    # print(f"Part Two (input):  {part_two(INPUT)}") # 

    # random_tests()



def random_tests():
    print(101 // 2)


       


if __name__ == '__main__':
    main()