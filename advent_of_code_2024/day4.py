'''
--- Day 4: Ceres Search ---
"Looks like the Chief's not here. Next!" One of The Historians pulls out a device and pushes the only button on it. After a brief flash, you recognize the interior of the Ceres monitoring station!

As the search for the Chief continues, a small Elf who lives on the station tugs on your shirt; she'd like to know if you could help her with her word search (your puzzle input). She only has to find one word: XMAS.

This word search allows words to be horizontal, vertical, diagonal, written backwards, or even overlapping other words. It's a little unusual, though, as you don't merely need to find one instance of XMAS - you need to find all of them. Here are a few ways XMAS might appear, where irrelevant characters have been replaced with .:

..X...
.SAMX.
.A..A.
XMAS.S
.X....

The actual word search will be full of letters instead. For example:

MMMSXXMASM
MSAMXMSMSA
AMXSXMAAMM
MSAMASMSMX
XMASAMXAMM
XXAMMXXAMA
SMSMSASXSS
SAXAMASAAA
MAMMMXMMMM
MXMXAXMASX

In this word search, XMAS occurs a total of 18 times; here's the same word search again, but where letters not involved in any XMAS have been replaced with .:

....XXMAS.
.SAMXMS...
...S..A...
..A.A.MS.X
XMASAMX.MM
X.....XA.A
S.S.S.S.SS
.A.A.A.A.A
..M.M.M.MM
.X.X.XMASX

Take a look at the little Elf's word search. How many times does XMAS appear?

--- Part Two ---
The Elf looks quizzically at you. Did you misunderstand the assignment?

Looking for the instructions, you flip over the word search to find that this isn't actually an XMAS puzzle; it's an X-MAS puzzle in which you're supposed to find two MAS in the shape of an X. One way to achieve that is like this:

M.S    
.A.
M.S

Irrelevant characters have again been replaced with . in the above diagram. Within the X, each MAS can be written forwards or backwards.

Here's the same example from before, but this time all of the X-MASes have been kept instead:

.M.S......
..A..MSMS.
.M.S.MAA..
..A.ASMSM.
.M.S.M....
..........
S.S.S.S.S.
.A.A.A.A..
M.M.M.M.M.
..........

In this example, an X-MAS appears 9 times.

Flip the word search from the instructions back over to the word search side and try again. How many times does an X-MAS appear?
'''

import re
import pandas as pd
import numpy as np
from pathlib import Path
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day4_example.txt'
INPUT = DATA_DIR / 'day4_input.txt'

PART_2_SQUARE_HEIGHT = 3
PART_2_SQUARE_WIDTH = 3

REGEX_PART_ONE = r'(?=(?P<forward>XMAS)|(?P<backward>SAMX))'
REGEX_PART_TWO = r'M.S.A.M.S|S.M.A.S.M|M.M.A.S.S|S.S.A.M.M'

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        
    return line_list

def get_vertical_lines(horizontal_line_list: list[str]) -> list[str]:
    num_columns = len(horizontal_line_list[0])

    output_list = []
    for i in range(num_columns):
        output_list.append(''.join(line[i] for line in horizontal_line_list))

    return output_list

def get_diagonal_lines(horizontal_line_list: list[str], vertical_line_list: list[str]) -> list[str]:
    num_columns = len(horizontal_line_list)
    num_rows = len(vertical_line_list)

    rows = [list(x) for x in horizontal_line_list]    

    output_list = []
    
    df = pd.DataFrame(rows)
    for x in range(0-num_rows, num_columns-1):
        output_list.append(''.join(x for x in np.diag(df, k=x)))

    df2 = df.iloc[::-1].reset_index(drop=True)
    for x in range(0-num_rows, num_columns-1):
        output_list.append(''.join(x for x in np.diag(df2, k=x)))

    return output_list

def regex_part_one(input: str) -> int:
    pattern = re.compile(REGEX_PART_ONE)
    matches = pattern.finditer(input)

    total = 0
    for m in matches:
        if m.group(1) is not None or m.group(2) is not None:
            total += 1

    return total

def part_one(filename: Path) -> int:   
    horizontal_line_list = ingest_data(filename)
    horizontal_total = sum(regex_part_one(line) for line in horizontal_line_list)

    vertical_line_list = get_vertical_lines(horizontal_line_list)
    vertical_total = sum(regex_part_one(line) for line in vertical_line_list)

    diagonal_line_list = get_diagonal_lines(horizontal_line_list, vertical_line_list)
    diagonal_total = sum(regex_part_one(line) for line in diagonal_line_list)

    return horizontal_total + vertical_total + diagonal_total

def regex_part_two(input: str) -> int:
    pattern = re.compile(REGEX_PART_TWO)
    matches = pattern.findall(input)

    return 1 if matches else 0  

def get_squares(horizontal_line_list: list[str], vertical_line_list: list[str]) -> list[str]:
    num_rows = len(horizontal_line_list)
    num_columns = len(vertical_line_list)

    output_list = []
    for row_num in range(num_rows - (PART_2_SQUARE_WIDTH - 1)):
        for col_num in range(num_columns - (PART_2_SQUARE_HEIGHT -1)):
            sq1 = (horizontal_line_list[row_num])[col_num] + (horizontal_line_list[row_num])[col_num+1] + (horizontal_line_list[row_num])[col_num+2]
            sq2 = (horizontal_line_list[row_num+1])[col_num] + (horizontal_line_list[row_num+1])[col_num+1] + (horizontal_line_list[row_num+1])[col_num+2]
            sq3 = (horizontal_line_list[row_num+2])[col_num] + (horizontal_line_list[row_num+2])[col_num+1] + (horizontal_line_list[row_num+2])[col_num+2]
            output_list.append(sq1 + sq2 + sq3)
    return output_list

def part_two(filename: Path) -> int:
    horizontal_line_list = ingest_data(filename)
    vertical_line_list = get_vertical_lines(horizontal_line_list)

    square_list = get_squares(horizontal_line_list, vertical_line_list)
    answer = sum(regex_part_two(square) for square in square_list)

    return answer

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}")
    print(f"Part One (input):  {part_one(INPUT)}")  # 2100 is too low!  2946 is too high!  2943 is too high!  2543 is correct!
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}")
    print(f"Part Two (input):  {part_two(INPUT)}")  # 1933 is too high!  1884 is too low!  1930 is correct!


if __name__ == '__main__':
    main()