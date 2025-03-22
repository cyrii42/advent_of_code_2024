'''--- Day 8: Treetop Tree House ---
The expedition comes across a peculiar patch of tall trees all planted carefully in a grid. The Elves explain that a previous expedition planted these trees as a reforestation effort. Now, they're curious if this would be a good location for a tree house.

First, determine whether there is enough tree cover here to keep a tree house hidden. To do this, you need to count the number of trees that are visible from outside the grid when looking directly along a row or column.

The Elves have already launched a quadcopter to generate a map with the height of each tree (your puzzle input). For example:

30383
25512
65332
33549
35390

Each tree is represented as a single digit whose value is its height, where 0 is the shortest and 9 is the tallest.

A tree is visible if all of the other trees between it and an edge of the grid are shorter than it. Only consider trees in the same row or column; that is, only look up, down, left, or right from any given tree.

All of the trees around the edge of the grid are visible - since they are already on the edge, there are no trees to block the view. In this example, that only leaves the interior nine trees to consider:

The top-left 5 is visible from the left and top. (It isn't visible from the right or bottom since other trees of height 5 are in the way.)
The top-middle 5 is visible from the top and right.
The top-right 1 is not visible from any direction; for it to be visible, there would need to only be trees of height 0 between it and an edge.
The left-middle 5 is visible, but only from the right.
The center 3 is not visible from any direction; for it to be visible, there would need to be only trees of at most height 2 between it and an edge.
The right-middle 3 is visible from the right.
In the bottom row, the middle 5 is visible, but the 3 and 4 are not.
With 16 trees visible on the edge and another 5 visible in the interior, a total of 21 trees are visible in this arrangement.

Consider your map; how many trees are visible from outside the grid?

--- Part Two ---
Content with the amount of tree cover available, the Elves just need to know the best spot to build their tree house: they would like to be able to see a lot of trees.

To measure the viewing distance from a given tree, look up, down, left, and right from that tree; stop if you reach an edge or at the first tree that is the same height or taller than the tree under consideration. (If a tree is right on the edge, at least one of its viewing distances will be zero.)

The Elves don't care about distant trees taller than those found by the rules above; the proposed tree house has large eaves to keep it dry, so they wouldn't be able to see higher than the tree house anyway.

In the example above, consider the middle 5 in the second row:

30373
25512
65332
33549
35390

Looking up, its view is not blocked; it can see 1 tree (of height 3).
Looking left, its view is blocked immediately; it can see only 1 tree (of height 5, right next to it).
Looking right, its view is not blocked; it can see 2 trees.
Looking down, its view is blocked eventually; it can see 2 trees (one of height 3, then the tree of height 5 that blocks its view).
A tree's scenic score is found by multiplying together its viewing distance in each of the four directions. For this tree, this is 4 (found by multiplying 1 * 1 * 2 * 2).

However, you can do even better: consider the tree of height 5 in the middle of the fourth row:

30373
25512
65332
33549
35390

Looking up, its view is blocked at 2 trees (by another tree with a height of 5).
Looking left, its view is not blocked; it can see 2 trees.
Looking down, its view is also not blocked; it can see 1 tree.
Looking right, its view is blocked at 2 trees (by a massive tree of height 9).
This tree's scenic score is 8 (2 * 2 * 1 * 2); this is the ideal spot for the tree house.

Consider each tree on your map. What is the highest scenic score possible for any tree?

'''

import math
from copy import deepcopy
from enum import Enum
from dataclasses import dataclass, field
from pathlib import Path
from typing import Literal, NamedTuple, Optional, Self

from alive_progress import alive_it
from rich import print

from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day8_example.txt'
INPUT = DATA_DIR / '2022_day8_input.txt'
       

def ingest_data(filename: Path):
    with open(filename) as f:
        line_list = [line.strip('\n') for line in f.readlines()]
    return line_list

def make_column_lists(row_list: list[str]) -> list[str]:
    output_list = []
    for x in range(len(row_list)):
        output_list.append(''.join(row[x] for row in row_list))
        
    return output_list

class Direction(Enum):
    LEFT = 1
    RIGHT = 2
    UP = 3
    DOWN = 4

@dataclass
class Tree():
    row: int
    col: int
    num: int

@dataclass
class Map():
    tree_list: list[Tree]

    @property
    def height(self) -> int:
        return max(tree.row for tree in self.tree_list)

    @classmethod
    def create_map(cls, line_list: list[str]) -> Self:
        tree_list = []
        for i, line in enumerate(line_list):
            for j, char in enumerate(line):
                tree_list.append(Tree(row=i, col=j, num=int(char)))
        
        return cls(tree_list)

    def get_adjacent_trees(self, tree: Tree, direction: Direction) -> list[Tree]:
        match direction:
            case Direction.LEFT:
                return sorted([test_tree for test_tree in self.tree_list 
                               if test_tree.row == tree.row and test_tree.col < tree.col],
                              key=lambda tree: tree.col, reverse=True)
            case Direction.RIGHT:
                return sorted([test_tree for test_tree in self.tree_list 
                               if test_tree.row == tree.row and test_tree.col > tree.col],
                              key=lambda tree: tree.col, reverse=False)
            case Direction.UP: 
                return sorted([test_tree for test_tree in self.tree_list 
                               if test_tree.col == tree.col and test_tree.row < tree.row],
                              key=lambda tree: tree.row, reverse=True)
            case Direction.DOWN:
                return sorted([test_tree for test_tree in self.tree_list 
                               if test_tree.col == tree.col and test_tree.row > tree.row],
                              key=lambda tree: tree.row, reverse=False)

    def check_tree(self, tree: Tree) -> bool:
        if tree.row == 0 or tree.row == self.height or tree.col == 0 or tree.col == self.height:
            return True
        if all(test_tree.num < tree.num for test_tree in self.get_adjacent_trees(tree, Direction.LEFT)):
            return True
        if all(test_tree.num < tree.num for test_tree in self.get_adjacent_trees(tree, Direction.RIGHT)):
            return True
        if all(test_tree.num < tree.num for test_tree in self.get_adjacent_trees(tree, Direction.UP)):
            return True
        return all(test_tree.num < tree.num for test_tree in self.get_adjacent_trees(tree, Direction.DOWN))

    def get_scenic_score(self, tree: Tree) -> int:
        if tree.row == 0 or tree.col == 0:
            return 0
        
        score_list = []
        for direction in Direction:
            score = 0
            for adjacent_tree in self.get_adjacent_trees(tree, direction):
                score += 1
                if adjacent_tree.num >= tree.num:
                    break
            score_list.append(score)
            
        return math.prod(score_list)
        
    def get_part_one_answer(self) -> int:
        tree_checks = [self.check_tree(tree) for tree in self.tree_list]
        return len([x for x in tree_checks if x])

    def get_part_two_answer(self) -> int:
        return max(self.get_scenic_score(tree) for tree in self.tree_list)

def part_one(filename: Path):
    line_list = ingest_data(filename)
    map = Map.create_map(line_list)
    return map.get_part_one_answer()

def part_two(filename: Path):
    line_list = ingest_data(filename)
    map = Map.create_map(line_list)
    return map.get_part_two_answer()

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # 21
    print(f"Part One (input):  {part_one(INPUT)}") # 1801
    
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # 8
    print(f"Part Two (input):  {part_two(INPUT)}") # 209880

    # random_tests()


def random_tests():
    ...

if __name__ == '__main__':
    main()





