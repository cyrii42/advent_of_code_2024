'''
--- Day 7: Bridge Repair ---

The Historians take you to a familiar rope bridge over a river in the middle of a jungle. The Chief isn't on this side of the bridge, though; maybe he's on the other side?

When you go to cross the bridge, you notice a group of engineers trying to repair it. (Apparently, it breaks pretty frequently.) You won't be able to cross until it's fixed.

You ask how long it'll take; the engineers tell you that it only needs final calibrations, but some young elephants were playing nearby and stole all the operators from their calibration equations! They could finish the calibrations if only someone could determine which test values could possibly be produced by placing any combination of operators into their calibration equations (your puzzle input).

For example:

190: 10 19
3267: 81 40 27
83: 17 5
156: 15 6
7290: 6 8 6 15
161011: 16 10 13
192: 17 8 14
21037: 9 7 18 13
292: 11 6 16 20

Each line represents a single equation. The test value appears before the colon on each line; it is your job to determine whether the remaining numbers can be combined with operators to produce the test value.

Operators are always evaluated left-to-right, not according to precedence rules. Furthermore, numbers in the equations cannot be rearranged. Glancing into the jungle, you can see elephants holding two different types of operators: add (+) and multiply (*).

Only three of the above equations can be made true by inserting operators:

    190: 10 19 has only one position that accepts an operator: between 10 and 19. Choosing + would give 29, but choosing * would give the test value (10 * 19 = 190).
    3267: 81 40 27 has two positions for operators. Of the four possible configurations of the operators, two cause the right side to match the test value: 81 + 40 * 27 and 81 * 40 + 27 both equal 3267 (when evaluated left-to-right)!
    292: 11 6 16 20 can be solved in exactly one way: 11 + 6 * 16 + 20.

The engineers just need the total calibration result, which is the sum of the test values from just the equations that could possibly be true. In the above example, the sum of the test values for the three equations listed above is 3749.

Determine which equations could possibly be true. What is their total calibration result?

--- Part Two ---

The engineers seem concerned; the total calibration result you gave them is nowhere close to being within safety tolerances. Just then, you spot your mistake: some well-hidden elephants are holding a third type of operator.

The concatenation operator (||) combines the digits from its left and right inputs into a single number. For example, 12 || 345 would become 12345. All operators are still evaluated left-to-right.

Now, apart from the three equations that could be made true using only addition and multiplication, the above example has three more equations that can be made true by inserting operators:

    156: 15 6 can be made true through a single concatenation: 15 || 6 = 156.
    7290: 6 8 6 15 can be made true using 6 * 8 || 6 * 15.
    192: 17 8 14 can be made true using 17 || 8 + 14.

Adding up all six test values (the three that could be made before using only + and * plus the new three that can now be made by also using ||) produces the new total calibration result of 11387.

Using your new knowledge of elephant hiding spots, determine which equations could possibly be true. What is their total calibration result?


'''

from pathlib import Path
from rich import print
from copy import deepcopy
import itertools
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / 'day7_example.txt'
INPUT = DATA_DIR / 'day7_input.txt'

OPERATORS_PART_ONE = ['+', '*']
OPERATORS_PART_TWO = ['+', '*', '||']

def ingest_data(filename: Path) -> list[tuple[int, list[int]]]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n').split(':') for line in f.readlines()]
        output_list = [(int(test_value), [int(x) for x in numbers.split()]) for test_value, numbers in line_list]
        
    return output_list

def find_operator_combos(number_list: list[int], potential_operators: list[str]) -> list[list[str]]:
    num_gaps = len(number_list) - 1
    operator_combos = itertools.product(potential_operators, repeat=num_gaps)
    operator_combo_list = [list(x) for x in list(operator_combos)]
    return operator_combo_list

def validate_equation(test_value: int, number_list: list[int], operator_combo_list: list[list[str]]) -> bool:
    for operator_list in operator_combo_list:
        result = parse_operator_list(deepcopy(number_list), deepcopy(operator_list))
        if result == test_value:
            return True

    return False
        
def parse_operator_list(number_list: list[int], operator_list: list[str]) -> int:
    if len(number_list) == 1:
        return number_list[0]

    num_1 = number_list.pop(0)
    num_2 = number_list.pop(0)
    operator = operator_list.pop(0)
    result = perform_calculation(num_1, num_2, operator)
    number_list.insert(0, result)
    return parse_operator_list(number_list, operator_list)

def perform_calculation(num_1: int, num_2: int, operator: str) -> int:
    match operator:
        case '+': return num_1 + num_2
        case '*': return num_1 * num_2
        case '||': return int(f"{num_1}{num_2}")
        case _: raise ValueError
    
def find_calibration_result(filename: Path, operator_list: list[str]) -> int:
    input_data = ingest_data(filename)

    valid_equations = list()
    for equation_input in alive_it(input_data):
        test_value, number_list = equation_input
        operator_combos = find_operator_combos(number_list, operator_list)
        if validate_equation(test_value, number_list, operator_combos):
            valid_equations.append(test_value)
        
    return sum(valid_equations)

def part_one(filename: Path) -> int:
    return find_calibration_result(filename, OPERATORS_PART_ONE)

def part_two(filename: Path) -> int:
    return find_calibration_result(filename, OPERATORS_PART_TWO)

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 3749
    print(f"Part One (input):  {part_one(INPUT)}") # 1038838357795
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 11387
    print(f"Part Two (input):  {part_two(INPUT)}") # 254136560217241

if __name__ == '__main__':
    main()