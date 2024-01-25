import dataclasses
import enum


class HandType(enum.IntEnum):
    FIVE = 7
    FOUR = 6
    FULL_HOUSE = 5
    THREE = 4
    TWO_PAIRS = 3
    ONE_PAIR = 2
    HIGH_CARD = 1


def determine_type(hand: list[int]) -> HandType:
    freqs = dict()
    for card in hand:
        freqs[card] = freqs.get(card, 0) + 1
    if 5 in freqs.values():
        return HandType.FIVE
    if 4 in freqs.values():
        return HandType.FOUR
    if 3 in freqs.values():
        return HandType.FULL_HOUSE if 2 in freqs.values() else HandType.THREE
    if 2 in freqs.values():
        if list(freqs.values()).count(2) > 1:
            return HandType.TWO_PAIRS
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


def determine_type_b(hand: list[int]) -> HandType:
    freqs = dict()
    for card in hand:
        if card != 0:
            freqs[card] = freqs.get(card, 0) + 1
    jokers = hand.count(0)

    if 5 in freqs.values():
        return HandType.FIVE
    if 4 in freqs.values():
        return HandType.FOUR if jokers == 0 else HandType.FIVE
    if 3 in freqs.values():
        if jokers == 2:
            return HandType.FIVE
        if jokers == 1:
            return HandType.FOUR
        return HandType.FULL_HOUSE if 2 in freqs.values() else HandType.THREE
    if 2 in freqs.values():
        if list(freqs.values()).count(2) > 1:
            if jokers > 0:
                return HandType.FULL_HOUSE
            return HandType.TWO_PAIRS
        if jokers == 3:
            return HandType.FIVE
        if jokers == 2:
            return HandType.FOUR
        if jokers == 1:
            return HandType.THREE
        return HandType.ONE_PAIR
    if jokers == 4 or jokers == 5:
        return HandType.FIVE
    if jokers == 3:
        return HandType.FOUR
    if jokers == 2:
        return HandType.THREE
    if jokers == 1:
        return HandType.ONE_PAIR
    return HandType.HIGH_CARD


def card_to_int(card: str):
    if card == 'A':
        return 14
    if card == 'K':
        return 13
    if card == 'Q':
        return 12
    if card == 'J':
        return 11
    if card == 'T':
        return 10
    return ord(card) - ord('2') + 2


def card_to_int_b(card: str):
    if card == 'A':
        return 14
    if card == 'K':
        return 13
    if card == 'Q':
        return 12
    if card == 'J':
        return 0
    if card == 'T':
        return 10
    return ord(card) - ord('2') + 2


@dataclasses.dataclass(order=True)
class Hand:
    hand_type: HandType
    hand: list[int]

    @staticmethod
    def from_str(h: str):
        hh = [card_to_int(c) for c in h]
        return Hand(determine_type(hh), hh)

    @staticmethod
    def from_str_b(h: str):
        hh = [card_to_int_b(c) for c in h]
        return Hand(determine_type_b(hh), hh)


def solve(lines: list[str]):
    all_hands = []
    for line in lines:
        if line.strip():
            hand, score = line.strip().split(' ')
            from_str = Hand.from_str(hand)
            # print(from_str)
            all_hands.append((from_str, int(score)))

    all_hands.sort(key=lambda x: x[0])
    # print(all_hands)
    score = 0
    for ((_, sc), rank) in zip(all_hands, range(1, len(all_hands) + 1)):
        score += sc * rank
    return score


def solve_b(lines: list[str]):
    all_hands = []
    for line in lines:
        if line.strip():
            hand, score = line.strip().split(' ')
            from_str = Hand.from_str_b(hand)
            print(from_str)
            all_hands.append((from_str, int(score)))

    all_hands.sort(key=lambda x: x[0])
    print(all_hands)
    score = 0
    for ((_, sc), rank) in zip(all_hands, range(1, len(all_hands) + 1)):
        score += sc * rank
    return score


if __name__ == '__main__':
    sample = """32T3K 765
T55J5 684
KK677 28
JJJJJ 220
QQQJA 483"""
    print(solve_b(sample.split('\n')))
    with open('d7.txt', 'r') as file:
        print(solve_b(file.readlines()))
