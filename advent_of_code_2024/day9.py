'''
--- Day 9: Disk Fragmenter ---

Another push of the button leaves you in the familiar hallways of some friendly amphipods! Good thing you each somehow got your own personal mini submarine. The Historians jet away in search of the Chief, mostly by driving directly into walls.

While The Historians quickly figure out how to pilot these things, you notice an amphipod in the corner struggling with his computer. He's trying to make more contiguous free space by compacting all of the files, but his program isn't working; you offer to help.

He shows you the disk map (your puzzle input) he's already generated. For example:

2333133121414131402

The disk map uses a dense format to represent the layout of files and free space on the disk. The digits alternate between indicating the length of a file and the length of free space.

So, a disk map like 12345 would represent a one-block file, two blocks of free space, a three-block file, four blocks of free space, and then a five-block file. A disk map like 90909 would represent three nine-block files in a row (with no free space between them).

Each file on disk also has an ID number based on the order of the files as they appear before they are rearranged, starting with ID 0. So, the disk map 12345 has three files: a one-block file with ID 0, a three-block file with ID 1, and a five-block file with ID 2. Using one character for each block where digits are the file ID and . is free space, the disk map 12345 represents these individual blocks:

0..111....22222

The first example above, 2333133121414131402, represents these individual blocks:

00...111...2...333.44.5555.6666.777.888899

The amphipod would like to move file blocks one at a time from the end of the disk to the leftmost free space block (until there are no gaps remaining between file blocks). For the disk map 12345, the process looks like this:

0..111....22222
02.111....2222.
022111....222..
0221112...22...
02211122..2....
022111222......

The first example requires a few more steps:

00...111...2...333.44.5555.6666.777.888899
009..111...2...333.44.5555.6666.777.88889.
0099.111...2...333.44.5555.6666.777.8888..
00998111...2...333.44.5555.6666.777.888...
009981118..2...333.44.5555.6666.777.88....
0099811188.2...333.44.5555.6666.777.8.....
009981118882...333.44.5555.6666.777.......
0099811188827..333.44.5555.6666.77........
00998111888277.333.44.5555.6666.7.........
009981118882777333.44.5555.6666...........
009981118882777333644.5555.666............
00998111888277733364465555.66.............
0099811188827773336446555566..............

The final step of this file-compacting process is to update the filesystem checksum. To calculate the checksum, add up the result of multiplying each of these blocks' position with the file ID number it contains. The leftmost block is in position 0. If a block contains free space, skip it instead.

Continuing the first example, the first few blocks' position multiplied by its file ID number are 0 * 0 = 0, 1 * 0 = 0, 2 * 9 = 18, 3 * 9 = 27, 4 * 8 = 32, and so on. In this example, the checksum is the sum of these, 1928.

Compact the amphipod's hard drive using the process he requested. What is the resulting filesystem checksum? (Be careful copy/pasting the input for this puzzle; it is a single, very long line.)

--- Part Two ---

Upon completion, two things immediately become clear. First, the disk definitely has a lot more contiguous free space, just like the amphipod hoped. Second, the computer is running much more slowly! Maybe introducing all of that file system fragmentation was a bad idea?

The eager amphipod already has a new plan: rather than move individual blocks, he'd like to try compacting the files on his disk by moving whole files instead.

This time, attempt to move whole files to the leftmost span of free space blocks that could fit the file. Attempt to move each file exactly once in order of decreasing file ID number starting with the file with the highest file ID number. If there is no span of free space to the left of a file that is large enough to fit the file, the file does not move.

The first example from above now proceeds differently:

00...111...2...333.44.5555.6666.777.888899
0099.111...2...333.44.5555.6666.777.8888..
0099.1117772...333.44.5555.6666.....8888..
0099.111777244.333....5555.6666.....8888..
00992111777.44.333....5555.6666.....8888..

The process of updating the filesystem checksum is the same; now, this example's checksum would be 2858.

Start over, now compacting the amphipod's hard drive using this new method instead. What is the resulting filesystem checksum?


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

EXAMPLE = DATA_DIR / 'day9_example.txt'
INPUT = DATA_DIR / 'day9_input.txt'


def ingest_data(filename: Path) -> str:
    with open(filename, 'r') as f:
        return f.read()


@dataclass
class File():
    length: int
    id: Optional[int] = None

@dataclass
class Block():
    index: int
    id: Optional[int] = None

@dataclass
class Filesystem():
    files: list[File]
    blocks: list[Block] = field(default_factory=list)

    def populate_block_list(self):
        id_list = [file.id for file in self.files for _ in range(file.length)]
        self.blocks += [Block(i, file_id) for i, file_id in enumerate(id_list)]
            
    def compress_part_one(self):
        self.populate_block_list()
        free_blocks = [block for block in self.blocks if block.id is None]       
        for free_block in alive_it(free_blocks):
            non_free_blocks = [block for block in self.blocks if block.id is not None]
            if non_free_blocks[-1].index > free_block.index:
                self.blocks[free_block.index] = Block(free_block.index, non_free_blocks[-1].id)
                self.blocks[non_free_blocks[-1].index] = Block(non_free_blocks[-1].index, None)

    def compress_part_two(self):
        non_empty_files = [file for file in self.files if file.id is not None]
        for file in reversed(non_empty_files):
            for i, test_file in enumerate(self.files):
                if test_file.id is None and test_file.length >= file.length:
                    print(f"Moving File {file.id} to position {i}...")
                    self.files[i] = File(length=file.length,
                                         id=file.id)
                    if test_file.length > file.length:
                        self.files.insert(i+1, File(length=test_file.length - file.length,
                                                    id=None))
                    # print(self.files)
                    break
        self.populate_block_list()
            
    def clear_moved_file(self, moving_file: File):
        for file in reversed(self.files):
            if file.id == moving_file.id:
                file.id = None
            
    def calculate_checksum(self) -> int:
        total = 0
        for i, block in enumerate(self.blocks):
            total += 0 if block.id is None else i * block.id
        return total

def create_filesystem(input: str) -> Filesystem:
    file_list = []
    next_id = 0
    for i, char in enumerate(input):
        if i % 2 == 0:
            file_list.append(File(length=int(char), 
                                  id=next_id))
            next_id += 1
        else:
            file_list.append(File(length=int(char), 
                                  id=None))
        
    return Filesystem(file_list)
        
        

def part_one(filename: Path):
    input = ingest_data(filename)
    filesystem = create_filesystem(input)
    filesystem.compress_part_one()

    return filesystem.calculate_checksum()


def part_two(filename: Path):
    input = ingest_data(filename)
    filesystem = create_filesystem(input)
    print(filesystem)
    filesystem.compress_part_two()
    print(filesystem)

    return filesystem.calculate_checksum()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 1928
    # print(f"Part One (input):  {part_one(INPUT)}") # 6385338159127
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 2858
    # print(f"Part Two (input):  {part_two(INPUT)}")



    


if __name__ == '__main__':
    main()