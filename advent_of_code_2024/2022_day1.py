'''
--- Day 1: Calorie Counting ---

Santa's reindeer typically eat regular reindeer food, but they need a lot of magical energy to deliver presents on Christmas. For that, their favorite snack is a special type of star fruit that only grows deep in the jungle. The Elves have brought you on their annual expedition to the grove where the fruit grows.

To supply enough magical energy, the expedition needs to retrieve a minimum of fifty stars by December 25th. Although the Elves assure you that the grove has plenty of fruit, you decide to grab any fruit you see along the way, just in case.

Collect stars by solving puzzles. Two puzzles will be made available on each day in the Advent calendar; the second puzzle is unlocked when you complete the first. Each puzzle grants one star. Good luck!

The jungle must be too overgrown and difficult to navigate in vehicles or access from the air; the Elves' expedition traditionally goes on foot. As your boats approach land, the Elves begin taking inventory of their supplies. One important consideration is food - in particular, the number of Calories each Elf is carrying (your puzzle input).

The Elves take turns writing down the number of Calories contained by the various meals, snacks, rations, etc. that they've brought with them, one item per line. Each Elf separates their own inventory from the previous Elf's inventory (if any) by a blank line.

For example, suppose the Elves finish writing their items' Calories and end up with the following list:

1000
2000
3000

4000

5000
6000

7000
8000
9000

10000

This list represents the Calories of the food carried by five Elves:

    The first Elf is carrying food with 1000, 2000, and 3000 Calories, a total of 6000 Calories.
    The second Elf is carrying one food item with 4000 Calories.
    The third Elf is carrying food with 5000 and 6000 Calories, a total of 11000 Calories.
    The fourth Elf is carrying food with 7000, 8000, and 9000 Calories, a total of 24000 Calories.
    The fifth Elf is carrying one food item with 10000 Calories.

In case the Elves get hungry and need extra snacks, they need to know which Elf to ask: they'd like to know how many Calories are being carried by the Elf carrying the most Calories. In the example above, this is 24000 (carried by the fourth Elf).

Find the Elf carrying the most Calories. How many total Calories is that Elf carrying?

--- Part Two ---

By the time you calculate the answer to the Elves' question, they've already realized that the Elf carrying the most Calories of food might eventually run out of snacks.

To avoid this unacceptable situation, the Elves would instead like to know the total Calories carried by the top three Elves carrying the most Calories. That way, even if one of those Elves runs out of snacks, they still have two backups.

In the example above, the top three Elves are the fourth Elf (with 24000 Calories), then the third Elf (with 11000 Calories), then the fifth Elf (with 10000 Calories). The sum of the Calories carried by these three elves is 45000.

Find the top three Elves carrying the most Calories. How many Calories are those Elves carrying in total?


'''
from pathlib import Path
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day1_example.txt'
INPUT = DATA_DIR / '2022_day1_input.txt'
                
def ingest_data(filename: Path) -> list[str]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n') for line in f.readlines()]

    return line_list


def part_one(filename: Path) -> int:
    line_list = ingest_data(filename)
    num_list = [int(x) if x.isnumeric() else 0 for x in line_list] 
    highest_total = 0
    running_total = 0
    for num in num_list:
        if num == 0:
            running_total = 0
        else:
            running_total += num
            highest_total = running_total if running_total > highest_total else highest_total
    return highest_total
            

def part_two(filename: Path) -> int:
    line_list = ingest_data(filename)
    num_list = [int(x) if x.isnumeric() else 0 for x in line_list] 
    all_totals = []
    running_total = 0
    for num in num_list:
        if num == 0:
            all_totals.append(running_total)
            running_total = 0
        else:
            running_total += num
    all_totals.append(running_total)

    all_totals_sorted = sorted(all_totals, reverse=True)
    print(all_totals_sorted)
    answer = sum(all_totals_sorted[:3])
    return answer


def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 2400
    print(f"Part One (input):  {part_one(INPUT)}") # 75622
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 45000
    print(f"Part Two (input):  {part_two(INPUT)}") # 213159

if __name__ == '__main__':
    main()