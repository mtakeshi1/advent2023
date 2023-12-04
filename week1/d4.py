import re

input = """Card 1: 41 48 83 86 17 | 83 86  6 31 17  9 48 53
Card 2: 13 32 20 16 61 | 61 30 68 82 17 32 24 19
Card 3:  1 21 53 59 44 | 69 82 63 72 16 21 14  1
Card 4: 41 92 73 84 69 | 59 84 76 51 58  5 54 83
Card 5: 87 83 26 28 32 | 88 30 70 12 93 22 82 36
Card 6: 31 18 13 56 72 | 74 77 10 23 35 67 36 11"""


def nums(line: str):
    return set(re.findall(r"\d+", line))


def parse(line: str):
    num, rest = line.strip().split(":")
    winning = nums(rest.strip().split('|')[0])
    have = nums(rest.strip().split('|')[1])
    num = re.findall(r"\d+", num)[0]
    return num, winning, have


def score(game, winning: set[int], haves: set[int]):
    inter = len(haves.intersection(winning))
    if not inter:
        return 0
    return 1 << inter - 1


with open('d4.txt') as file:
    all_lines = list(file.readlines())
    scores = [score(*parse(line)) for line in all_lines]
    print(sum(scores))
    all_games = [parse(line) for line in all_lines]
    matching = [len(w.intersection(h)) for (g, w, h) in all_games]
    all_cards = [1 for line in all_lines]
    for i, num_cards in enumerate(all_cards):
        s = matching[i]
        for c in range(i + 1, i + 1 + s):
            all_cards[c] += num_cards
    print(sum(all_cards))
