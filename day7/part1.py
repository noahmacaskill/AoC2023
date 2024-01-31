from typing import List
from functools import cmp_to_key

INPUT = "input"

with open(INPUT, "r") as f:
    camel_cards = f.readlines()

card_values = {
    '2': 0,
    '3': 1,
    '4': 2,
    '5': 3,
    '6': 4,
    '7': 5,
    '8': 6,
    '9': 7,
    'T': 8,
    'J': 9,
    'Q': 10,
    'K': 11,
    'A': 12
}

def compare_hands(hand1: tuple[str, int, List[int]], hand2: tuple[str, int, List[int]]):
    """
    Compares the strength of two hands based on the number of matches found within each
    """
    for matches1, matches2 in zip(hand1[2], hand2[2]):
        if matches1 > matches2:
            return 1
        elif matches2 > matches1:
            return -1
    
    return tiebreak_compare(hand1[0], hand2[0])


def tiebreak_compare(hand1: str, hand2: str):
    """
    Tiebreaker for hands of the same type (highest card wins starting with the leftmost position)
    """
    for c1, c2 in zip(hand1, hand2):
        if card_values[c1] > card_values[c2]:
            return 1
        elif card_values[c2] > card_values[c1]:
            return -1
    
    return 0

def find_matches(hand: str) -> List[int]:
    """
    Finds the number of matches in a hand

    Parameters:
    hand (str): Cards in the hand

    Returns:
    List[int]: List containing the number of matches in the hand, sorted highest to lowest
        e.g. three of a kind & a pair = [3, 2]
    """
    card_counter = [0]*13

    for card in hand:
        card_counter[card_values[card]] += 1
    
    return sorted([x for x in card_counter if x > 0], reverse=True)

hands = [line.split()[0] for line in camel_cards]
bids = [int(line.split()[1]) for line in camel_cards]
camel_cards = list(zip(hands, bids, map(find_matches, hands)))

camel_cards = sorted(camel_cards, key=cmp_to_key(compare_hands))

tot_winnings = 0
for multiplier, hand in enumerate(camel_cards):
    tot_winnings += (multiplier+1)*hand[1]

print(f"ANSWER: {tot_winnings}")

