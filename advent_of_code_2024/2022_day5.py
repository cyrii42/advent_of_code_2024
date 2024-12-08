'''
--- Day 5: Supply Stacks ---

The expedition can depart as soon as the final supplies have been unloaded from the ships. Supplies are stored in stacks of marked crates, but because the needed supplies are buried under many other crates, the crates need to be rearranged.

The ship has a giant cargo crane capable of moving crates between stacks. To ensure none of the crates get crushed or fall over, the crane operator will rearrange them in a series of carefully-planned steps. After the crates are rearranged, the desired crates will be at the top of each stack.

The Elves don't want to interrupt the crane operator during this delicate procedure, but they forgot to ask her which crate will end up where, and they want to be ready to unload them as soon as possible so they can embark.

They do, however, have a drawing of the starting stacks of crates and the rearrangement procedure (your puzzle input). For example:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

move 1 from 2 to 1
move 3 from 1 to 3
move 2 from 2 to 1
move 1 from 1 to 2

In this example, there are three stacks of crates. Stack 1 contains two crates: crate Z is on the bottom, and crate N is on top. Stack 2 contains three crates; from bottom to top, they are crates M, C, and D. Finally, stack 3 contains a single crate, P.

Then, the rearrangement procedure is given. In each step of the procedure, a quantity of crates is moved from one stack to a different stack. In the first step of the above rearrangement procedure, one crate is moved from stack 2 to stack 1, resulting in this configuration:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

In the second step, three crates are moved from stack 1 to stack 3. Crates are moved one at a time, so the first crate to be moved (D) ends up below the second and third crates:

        [Z]
        [N]
    [C] [D]
    [M] [P]
 1   2   3

Then, both crates are moved from stack 2 to stack 1. Again, because crates are moved one at a time, crate C ends up below crate M:

        [Z]
        [N]
[M]     [D]
[C]     [P]
 1   2   3

Finally, one crate is moved from stack 1 to stack 2:

        [Z]
        [N]
        [D]
[C] [M] [P]
 1   2   3

The Elves just need to know which crate will end up on top of each stack; in this example, the top crates are C in stack 1, M in stack 2, and Z in stack 3, so you should combine these together and give the Elves the message CMZ.

After the rearrangement procedure completes, what crate ends up on top of each stack?

--- Part Two ---

As you watch the crane operator expertly rearrange the crates, you notice the process isn't following your prediction.

Some mud was covering the writing on the side of the crane, and you quickly wipe it away. The crane isn't a CrateMover 9000 - it's a CrateMover 9001.

The CrateMover 9001 is notable for many new and exciting features: air conditioning, leather seats, an extra cup holder, and the ability to pick up and move multiple crates at once.

Again considering the example above, the crates begin in the same configuration:

    [D]    
[N] [C]    
[Z] [M] [P]
 1   2   3 

Moving a single crate from stack 2 to stack 1 behaves the same as before:

[D]        
[N] [C]    
[Z] [M] [P]
 1   2   3 

However, the action of moving three crates from stack 1 to stack 3 means that those three moved crates stay in the same order, resulting in this new configuration:

        [D]
        [N]
    [C] [Z]
    [M] [P]
 1   2   3

Next, as both crates are moved from stack 2 to stack 1, they retain their order as well:

        [D]
        [N]
[C]     [Z]
[M]     [P]
 1   2   3

Finally, a single crate is still moved from stack 1 to stack 2, but now it's crate C that gets moved:

        [D]
        [N]
        [Z]
[M] [C] [P]
 1   2   3

In this example, the CrateMover 9001 has put the crates in a totally different order: MCD.

Before the rearrangement process finishes, update your simulation so that the Elves know where they should stand to be ready to unload the final supplies. After the rearrangement procedure completes, what crate ends up on top of each stack?


'''

from pathlib import Path
from rich import print
from copy import deepcopy
from dataclasses import dataclass
from typing import NamedTuple
from alive_progress import alive_it
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day5_example.txt'
INPUT = DATA_DIR / '2022_day5_input.txt'

def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]
        
    return line_list

def process_drawing(line_list: list[str]) -> list[list[str]]:
    labels = [int(x) for x in line_list[-1].split()]
    num_stacks = len(labels)
    stack_row_list = line_list[:-1]

    stack_list_by_row = []
    for row in stack_row_list:
        inner_list = []
        for x in range(0, num_stacks):
            inner_list.append(row[1 + x*4])
        stack_list_by_row.append(inner_list)

    output_list = []
    for x in range(num_stacks):
        output_list.append([row[x] for row in stack_list_by_row if row[x] != ' '])
    
    return output_list

@dataclass
class Stack():
    num: int
    contents: list[str]

    @property
    def top_crate(self) -> str:
        return self.contents[0]

    def pop(self) -> str:
        return self.contents.pop(0)

    def push(self, item: str) -> None:
        self.contents.insert(0, item)

def create_stacks(stack_list_raw: list[list[str]]) -> list[Stack]:
    output_list = []
    for i, raw_stack in enumerate(stack_list_raw, start=1):
        output_list.append(Stack(i, raw_stack))
    return output_list

def get_stack(stack_list: list[Stack], num: int) -> Stack:
    return [stack for stack in stack_list if stack.num == num][0]

class Procedure(NamedTuple):
    origin: int
    destination: int
    quantity: int

def parse_procedure_list(procedure_str_list: list[str]) -> list[Procedure]:
    output_list = []
    for procedure_str in procedure_str_list:
        procedure_str_split = procedure_str.split()
        output_list.append(Procedure(
                            origin=int(procedure_str_split[3]),
                            destination=int(procedure_str_split[5]),
                            quantity=int(procedure_str_split[1])
                            ))
    return output_list

def execute_procedure_list(procedure_list: list[Procedure], stack_list: list[Stack]) -> list[Stack]:
    for procedure in procedure_list:
        origin_stack = get_stack(stack_list, procedure.origin)
        destination_stack = get_stack(stack_list, procedure.destination)
        for _ in range(procedure.quantity):
            destination_stack.push(origin_stack.pop())
    return stack_list

def execute_procedure_list_part_two(procedure_list: list[Procedure], stack_list: list[Stack]) -> list[Stack]:
    for procedure in procedure_list:
        origin_stack = get_stack(stack_list, procedure.origin)
        destination_stack = get_stack(stack_list, procedure.destination)
        crates = origin_stack.contents[0:procedure.quantity]
        for _ in range(procedure.quantity):
            origin_stack.pop()
        crates += (destination_stack.contents)
        destination_stack.contents = crates
    return stack_list

def part_one(filename: Path) -> str:
    line_list = ingest_data(filename)
    procedure_str_list = [line for line in line_list if 'move' in line]
    stack_list_raw = process_drawing([line for line in line_list if 'move' not in line and line != ''])
    stack_list = create_stacks(stack_list_raw)
    procedure_list = parse_procedure_list(procedure_str_list)
    new_stack_list = execute_procedure_list(procedure_list, stack_list)
    return(''.join(stack.top_crate for stack in new_stack_list))

def part_two(filename: Path) -> str:
    line_list = ingest_data(filename)
    procedure_str_list = [line for line in line_list if 'move' in line]
    stack_list_raw = process_drawing([line for line in line_list if 'move' not in line and line != ''])
    stack_list = create_stacks(stack_list_raw)
    procedure_list = parse_procedure_list(procedure_str_list)
    new_stack_list = execute_procedure_list_part_two(procedure_list, stack_list)
    return(''.join(stack.top_crate for stack in new_stack_list))

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # CMZ
    print(f"Part One (input):  {part_one(INPUT)}") # MQSHJMWNH
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # MCD
    print(f"Part Two (input):  {part_two(INPUT)}") # LLWJRBHVZ

if __name__ == '__main__':
    main()