'''
'''

from pathlib import Path
from rich import print
from copy import deepcopy
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day8_example.txt'
INPUT = DATA_DIR / 'day8_input.txt'

def ingest_data(filename: Path) -> :
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        
    return line_list

def part_one(filename: Path) -> int:
    ...

def part_two(filename: Path) -> int:
    ...

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")

if __name__ == '__main__':
    main()