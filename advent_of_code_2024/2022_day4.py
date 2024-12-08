'''
--- Day 4: Camp Cleanup ---

Space needs to be cleared before the last supplies can be unloaded from the ships, and so several Elves have been assigned the job of cleaning up sections of the camp. Every section has a unique ID number, and each Elf is assigned a range of section IDs.

However, as some of the Elves compare their section assignments with each other, they've noticed that many of the assignments overlap. To try to quickly find overlaps and reduce duplicated effort, the Elves pair up and make a big list of the section assignments for each pair (your puzzle input).

For example, consider the following list of section assignment pairs:

2-4,6-8
2-3,4-5
5-7,7-9
2-8,3-7
6-6,4-6
2-6,4-8

For the first few pairs, this list means:

    Within the first pair of Elves, the first Elf was assigned sections 2-4 (sections 2, 3, and 4), while the second Elf was assigned sections 6-8 (sections 6, 7, 8).
    The Elves in the second pair were each assigned two sections.
    The Elves in the third pair were each assigned three sections: one got sections 5, 6, and 7, while the other also got 7, plus 8 and 9.

This example list uses single-digit section IDs to make it easier to draw; your actual list might contain larger numbers. Visually, these pairs of section assignments look like this:

.234.....  2-4
.....678.  6-8

.23......  2-3
...45....  4-5

....567..  5-7
......789  7-9

.2345678.  2-8
..34567..  3-7

.....6...  6-6
...456...  4-6

.23456...  2-6
...45678.  4-8

Some of the pairs have noticed that one of their assignments fully contains the other. For example, 2-8 fully contains 3-7, and 6-6 is fully contained by 4-6. In pairs where one assignment fully contains the other, one Elf in the pair would be exclusively cleaning sections their partner will already be cleaning, so these seem like the most in need of reconsideration. In this example, there are 2 such pairs.

In how many assignment pairs does one range fully contain the other?

--- Part Two ---

It seems like there is still quite a bit of duplicate work planned. Instead, the Elves would like to know the number of pairs that overlap at all.

In the above example, the first two pairs (2-4,6-8 and 2-3,4-5) don't overlap, while the remaining four pairs (5-7,7-9, 2-8,3-7, 6-6,4-6, and 2-6,4-8) do overlap:

    5-7,7-9 overlaps in a single section, 7.
    2-8,3-7 overlaps all of the sections 3 through 7.
    6-6,4-6 overlaps in a single section, 6.
    2-6,4-8 overlaps in sections 4, 5, and 6.

So, in this example, the number of overlapping assignment pairs is 4.

In how many assignment pairs do the ranges overlap?


'''

from pathlib import Path
from rich import print
from copy import deepcopy
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day4_example.txt'
INPUT = DATA_DIR / '2022_day4_input.txt'

def ingest_data(filename: Path) -> list[tuple[range, range]]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        range_pair_list = [x for x in [line.split(',') for line in line_list]]
        
    output_list = []
    for range_pair in range_pair_list:
        inner_list = []
        for range_str in range_pair:
            range_int_list = list(map(int, range_str.split('-')))
            range_obj = range(range_int_list[0], range_int_list[1]+1)
            inner_list.append(range_obj)
        output_list.append(inner_list)
    return output_list

def find_overlap(range_pair: tuple[range, range]) -> bool:
    range_1, range_2 = range_pair
    set1 = set(range_1)
    set2 = set(range_2)
    result = len(set1-set2) == 0 or len(set2-set1) == 0
    return result

def find_intersection(range_pair: tuple[range, range]) -> bool:
    range_1, range_2 = range_pair
    set1 = set(range_1)
    set2 = set(range_2)
    result = len(set1.intersection(set2)) > 0 or len(set2.intersection(set1)) > 0
    return result

def part_one(filename: Path) -> int:
    range_pair_list = ingest_data(filename)
    answer = len([x for x in range_pair_list if find_overlap(x)])
    return answer

def part_two(filename: Path) -> int:
    range_pair_list = ingest_data(filename)
    answer = len([x for x in range_pair_list if find_intersection(x)])
    return answer

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 2
    print(f"Part One (input):  {part_one(INPUT)}") # 567
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 4
    print(f"Part Two (input):  {part_two(INPUT)}") # 907

if __name__ == '__main__':
    main()