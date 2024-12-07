'''
--- Day 2: Rock Paper Scissors ---

The Elves begin to set up camp on the beach. To decide whose tent gets to be closest to the snack storage, a giant Rock Paper Scissors tournament is already in progress.

Rock Paper Scissors is a game between two players. Each game contains many rounds; in each round, the players each simultaneously choose one of Rock, Paper, or Scissors using a hand shape. Then, a winner for that round is selected: Rock defeats Scissors, Scissors defeats Paper, and Paper defeats Rock. If both players choose the same shape, the round instead ends in a draw.

Appreciative of your help yesterday, one Elf gives you an encrypted strategy guide (your puzzle input) that they say will be sure to help you win. "The first column is what your opponent is going to play: A for Rock, B for Paper, and C for Scissors. The second column--" Suddenly, the Elf is called away to help with someone's tent.

The second column, you reason, must be what you should play in response: X for Rock, Y for Paper, and Z for Scissors. Winning every time would be suspicious, so the responses must have been carefully chosen.

The winner of the whole tournament is the player with the highest score. Your total score is the sum of your scores for each round. The score for a single round is the score for the shape you selected (1 for Rock, 2 for Paper, and 3 for Scissors) plus the score for the outcome of the round (0 if you lost, 3 if the round was a draw, and 6 if you won).

Since you can't be sure if the Elf is trying to help you or trick you, you should calculate the score you would get if you were to follow the strategy guide.

For example, suppose you were given the following strategy guide:

A Y
B X
C Z

This strategy guide predicts and recommends the following:

    In the first round, your opponent will choose Rock (A), and you should choose Paper (Y). This ends in a win for you with a score of 8 (2 because you chose Paper + 6 because you won).
    In the second round, your opponent will choose Paper (B), and you should choose Rock (X). This ends in a loss for you with a score of 1 (1 + 0).
    The third round is a draw with both players choosing Scissors, giving you a score of 3 + 3 = 6.

In this example, if you were to follow the strategy guide, you would get a total score of 15 (8 + 1 + 6).

What would your total score be if everything goes exactly according to your strategy guide?

--- Part Two ---

The Elf finishes helping with the tent and sneaks back over to you. "Anyway, the second column says how the round needs to end: X means you need to lose, Y means you need to end the round in a draw, and Z means you need to win. Good luck!"

The total score is still calculated in the same way, but now you need to figure out what shape to choose so the round ends as indicated. The example above now goes like this:

    In the first round, your opponent will choose Rock (A), and you need the round to end in a draw (Y), so you also choose Rock. This gives you a score of 1 + 3 = 4.
    In the second round, your opponent will choose Paper (B), and you choose Rock so you lose (X) with a score of 1 + 0 = 1.
    In the third round, you will defeat your opponent's Scissors with Rock for a score of 1 + 6 = 7.

Now that you're correctly decrypting the ultra top secret strategy guide, you would get a total score of 12.

Following the Elf's instructions for the second column, what would your total score be if everything goes exactly according to your strategy guide?


'''
from pathlib import Path
from enum import IntEnum
from advent_of_code_2024.constants import DATA_DIR

EXAMPLE = DATA_DIR / '2022_day2_example.txt'
INPUT = DATA_DIR / '2022_day2_input.txt'

def ingest_data(filename: Path) -> list[list[str]]:
    with open(filename, 'r') as f:
        line_list = [line.strip('\n').split() for line in f.readlines()]
    return line_list
                
class Hand(IntEnum):
    ROCK = 1
    PAPER = 2
    SCISSORS = 3

class Result(IntEnum):
    WIN = 6
    DRAW = 3
    LOSS = 0

def process_game_part_one(game: tuple[Hand, Hand]) -> int:
    opponent_hand, player_hand = game
    if player_hand == opponent_hand:
        return player_hand + Result.DRAW
    elif player_hand == Hand.ROCK and opponent_hand == Hand.SCISSORS:
        return player_hand + Result.WIN
    elif player_hand == Hand.ROCK and opponent_hand == Hand.PAPER:
        return player_hand + Result.LOSS
    elif player_hand == Hand.SCISSORS and opponent_hand == Hand.PAPER:
        return player_hand + Result.WIN
    elif player_hand == Hand.SCISSORS and opponent_hand == Hand.ROCK:
        return player_hand + Result.LOSS
    elif player_hand == Hand.PAPER and opponent_hand == Hand.ROCK:
        return player_hand + Result.WIN
    elif player_hand == Hand.PAPER and opponent_hand == Hand.SCISSORS:
        return player_hand + Result.LOSS
    else:
        raise ValueError

def process_data_part_one(line_list: list[list[str]]) -> list[tuple[Hand, Hand]]:
    return [(translate_hand_part_one(line[0]), translate_hand_part_one(line[1])) 
            for line in line_list]

def translate_hand_part_one(hand_str: str) -> Hand:
    match hand_str:
        case 'A'|'X':
            return Hand.ROCK
        case 'B'|'Y':
            return Hand.PAPER
        case 'C'|'Z':
            return Hand.SCISSORS
        case _:
            raise ValueError    

def process_data_part_two(line_list: list[list[str]]) -> list[tuple]:
    return [(translate_game_str_part_two(line[0]), translate_game_str_part_two(line[1])) 
            for line in line_list]

def translate_game_str_part_two(game_str: str) -> Hand | Result:
    match game_str:
        case 'A':
            return Hand.ROCK
        case 'B':
            return Hand.PAPER
        case 'C':
            return Hand.SCISSORS
        case 'X':
            return Result.LOSS
        case 'Y':
            return Result.DRAW
        case 'Z':
            return Result.WIN
        case _:
            raise ValueError  

def process_game_part_two(game: tuple[Hand, Result]) -> int:
    opponent_hand, result = game
    if result == Result.DRAW:
        return opponent_hand + result
    if result == Result.WIN and opponent_hand == Hand.ROCK:
        return Hand.PAPER + result
    if result == Result.WIN and opponent_hand == Hand.PAPER:
        return Hand.SCISSORS + result
    if result == Result.WIN and opponent_hand == Hand.SCISSORS:
        return Hand.ROCK + result
    if result == Result.LOSS and opponent_hand == Hand.ROCK:
        return Hand.SCISSORS + result
    if result == Result.LOSS and opponent_hand == Hand.PAPER:
        return Hand.ROCK + result
    if result == Result.LOSS and opponent_hand == Hand.SCISSORS:
        return Hand.PAPER + result
    else:
        raise ValueError


def part_one(filename: Path) -> int:
    line_list = ingest_data(filename)
    game_list = process_data_part_one(line_list)
    answer = sum(process_game_part_one(game) for game in game_list)
    return answer
            
def part_two(filename: Path) -> int:
    line_list = ingest_data(filename)
    game_list = process_data_part_two(line_list)
    answer = sum(process_game_part_two(game) for game in game_list)
    return answer

def main():
    print(f"Part One (example):  {part_one(EXAMPLE)}") # should be 15
    print(f"Part One (input):  {part_one(INPUT)}") # 15691
    print()
    print(f"Part Two (example):  {part_two(EXAMPLE)}") # should be 12
    print(f"Part Two (input):  {part_two(INPUT)}") # 12989

if __name__ == '__main__':
    main()