'''
--- Day 3: Mull It Over ---
"Our computers are having issues, so I have no idea if we have any Chief Historians in stock! You're welcome to check the warehouse, though," says the mildly flustered shopkeeper at the North Pole Toboggan Rental Shop. The Historians head out to take a look.

The shopkeeper turns to you. "Any chance you can see why our computers are having issues again?"

The computer appears to be trying to run a program, but its memory (your puzzle input) is corrupted. All of the instructions have been jumbled up!

It seems like the goal of the program is just to multiply some numbers. It does that with instructions like mul(X,Y), where X and Y are each 1-3 digit numbers. For instance, mul(44,46) multiplies 44 by 46 to get a result of 2024. Similarly, mul(123,4) would multiply 123 by 4.

However, because the program's memory has been corrupted, there are also many invalid characters that should be ignored, even if they look like part of a mul instruction. Sequences like mul(4*, mul(6,9!, ?(12,34), or mul ( 2 , 4 ) do nothing.

For example, consider the following section of corrupted memory:

xmul(2,4)%&mul[3,7]!@^do_not_mul(5,5)+mul(32,64]then(mul(11,8)mul(8,5))

Only the four highlighted sections are real mul instructions. Adding up the result of each instruction produces 161 (2*4 + 5*5 + 11*8 + 8*5).

Scan the corrupted memory for uncorrupted mul instructions. What do you get if you add up all of the results of the multiplications?

--- Part Two ---
As you scan through the corrupted memory, you notice that some of the conditional statements are also still intact. If you handle some of the uncorrupted conditional statements in the program, you might be able to get an even more accurate result.

There are two new instructions you'll need to handle:

The do() instruction enables future mul instructions.
The don't() instruction disables future mul instructions.
Only the most recent do() or don't() instruction applies. At the beginning of the program, mul instructions are enabled.

For example:

xmul(2,4)&mul[3,7]!^don't()_mul(5,5)+mul(32,64](mul(11,8)undo()?mul(8,5))

This corrupted memory is similar to the example from before, but this time the mul(5,5) and mul(11,8) instructions are disabled because there is a don't() instruction before them. The other mul instructions function normally, including the one at the end that gets re-enabled by a do() instruction.

This time, the sum of the results is 48 (2*4 + 8*5).

Handle the new instructions; what do you get if you add up all of the results of just the enabled multiplications?
'''

import re
from pathlib import Path
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE_PART_ONE = DATA_DIR / 'day3_example.txt'
EXAMPLE_PART_TWO = DATA_DIR / 'day3_part2_example.txt'
INPUT = DATA_DIR / 'day3_input.txt'

REGEX_PART_ONE = r"mul\([0-9]{1,3}\,[0-9]{1,3}\)"

MUL_PATTERN = r"(?P<muls>mul\([0-9]{1,3}\,[0-9]{1,3}\))"
DO_PATTERN = r"(?P<do>do\(\))"
DONT_PATTERN = r"(?P<dont>don't\(\))"
REGEX_PART_TWO = MUL_PATTERN + '|' + DO_PATTERN + '|' + DONT_PATTERN

def ingest_data(filename: Path) -> str:
    with open(filename, 'r') as f:
        text = f.read()
    return text

def parse_mul(text: str) -> int:
    num1, num2 = text.removeprefix('mul(').removesuffix(')').split(',')
    return int(num1) * int(num2)

def part_one(filename: Path) -> int:
    text = ingest_data(filename)
    pattern = re.compile(REGEX_PART_ONE)
    muls = pattern.findall(text)
    return sum([parse_mul(mul) for mul in muls])

def part_two(filename: Path) -> int:
    text = ingest_data(filename)
    pattern = re.compile(REGEX_PART_TWO)
    matches = pattern.finditer(text)

    total = 0
    enabled = True
    for m in matches:
        text = m.group(0)

        match text:
            case "do()":
                enabled = True
            case "don't()":
                enabled = False
            case _ if enabled:
                total += parse_mul(text)

    return total


def main():
    print(f"Part One (example):  {part_one(EXAMPLE_PART_ONE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print(f"Part Two (example):  {part_two(EXAMPLE_PART_TWO)}")
    print(f"Part Two (input):  {part_two(INPUT)}")


if __name__ == '__main__':
    main()