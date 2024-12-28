'''
--- Day 13: Claw Contraption ---

Next up: the lobby of a resort on a tropical island. The Historians take a moment to admire the hexagonal floor tiles before spreading out.

Fortunately, it looks like the resort has a new arcade! Maybe you can win some prizes from the claw machines?

The claw machines here are a little unusual. Instead of a joystick or directional buttons to control the claw, these machines have two buttons labeled A and B. Worse, you can't just put in a token and play; it costs 3 tokens to push the A button and 1 token to push the B button.

With a little experimentation, you figure out that each machine's buttons are configured to move the claw a specific amount to the right (along the X axis) and a specific amount forward (along the Y axis) each time that button is pressed.

Each machine contains one prize; to win the prize, the claw must be positioned exactly above the prize on both the X and Y axes.

You wonder: what is the smallest number of tokens you would have to spend to win as many prizes as possible? You assemble a list of every machine's button behavior and prize location (your puzzle input). For example:

Button A: X+94, Y+34
Button B: X+22, Y+67
Prize: X=8400, Y=5400

Button A: X+26, Y+66
Button B: X+67, Y+21
Prize: X=12748, Y=12176

Button A: X+17, Y+86
Button B: X+84, Y+37
Prize: X=7870, Y=6450

Button A: X+69, Y+23
Button B: X+27, Y+71
Prize: X=18641, Y=10279

This list describes the button configuration and prize location of four different claw machines.

For now, consider just the first claw machine in the list:

    Pushing the machine's A button would move the claw 94 units along the X axis and 34 units along the Y axis.
    Pushing the B button would move the claw 22 units along the X axis and 67 units along the Y axis.
    The prize is located at X=8400, Y=5400; this means that from the claw's initial position, it would need to move exactly 8400 units along the X axis and exactly 5400 units along the Y axis to be perfectly aligned with the prize in this machine.

The cheapest way to win the prize is by pushing the A button 80 times and the B button 40 times. This would line up the claw along the X axis (because 80*94 + 40*22 = 8400) and along the Y axis (because 80*34 + 40*67 = 5400). Doing this would cost 80*3 tokens for the A presses and 40*1 for the B presses, a total of 280 tokens.

For the second and fourth claw machines, there is no combination of A and B presses that will ever win a prize.

For the third claw machine, the cheapest way to win the prize is by pushing the A button 38 times and the B button 86 times. Doing this would cost a total of 200 tokens.

So, the most prizes you could possibly win is two; the minimum tokens you would have to spend to win all (two) prizes is 480.

You estimate that each button would need to be pressed no more than 100 times to win a prize. How else would someone be expected to play?

Figure out how to win as many prizes as possible. What is the fewest tokens you would have to spend to win all possible prizes?

'''

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

EXAMPLE = DATA_DIR / 'day13_example.txt'
INPUT = DATA_DIR / 'day13_input.txt'


@dataclass
class Machine():
    button_a: tuple[int, int]
    button_b: tuple[int, int]
    prize_location: tuple[int, int]

def ingest_data(filename: Path) -> list[Machine]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        line_list = [line for line in line_list if line != '']

    data_list = []
    for x in range(0, len(line_list), 3):
        machine_data = line_list[x:x+3]
        data_list.append(machine_data)

    return [process_machine_data(data) for data in data_list]

def process_machine_data(data: list[str]) -> Machine:
    line_1 = data[0].removeprefix('Button A: ').replace(' ', '').replace('X+', '').replace('Y+', '').split(',')
    button_a = (int(line_1[0]), int(line_1[1]))

    line_2 = data[1].removeprefix('Button B: ').replace(' ', '').replace('X+', '').replace('Y+', '').split(',')
    button_b = (int(line_2[0]), int(line_2[1]))

    line_3 = data[2].removeprefix('Prize: ').replace(' ', '').replace('X=', '').replace('Y=', '').split(',')
    prize_location = (int(line_3[0]), int(line_3[1]))

    return Machine(button_a, button_b, prize_location)
        

def part_one(filename: Path):
    machine_list = ingest_data(filename)
    print(machine_list)


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