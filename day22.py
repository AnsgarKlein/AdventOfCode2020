#!/usr/bin/env python3

from typing import List

import re

def read_input_file(filename):
    decks: List[List[int]] = []

    with open(filename, 'r') as input_file:
        content = input_file.read().split('\n')

        current_deck: List[int] = []

        for line in content:
            if re.search('Player [0-9]:.*', line) is not None:
                # Start of deck
                pass
            elif line.strip() == '':
                # End of deck
                decks.append(current_deck)
                current_deck = []
            else:
                # Content of deck
                current_deck.append(int(line))

    return decks[0], decks[1]

def draw(deck: List[int]):
    if len(deck) == 0:
        return None
    return deck.pop(0)

def play_combat_round(deck1: List[int], deck2: List[int]) -> None:
    card1 = draw(deck1)
    card2 = draw(deck2)

    winner = deck1 if card1 > card2 else deck2
    winner.append(max((card1, card2)))
    winner.append(min((card1, card2)))

def play_combat(deck1: List[int], deck2: List[int]) -> None:
    rounds_played = 0

    # Play until someone wins
    while len(deck1) > 0 and len(deck2) > 0:
        rounds_played += 1
        play_combat_round(deck1, deck2)

        #print('Round: {}'.format(rounds_played))
        #print('Player 1: {}'.format(', '.join('{}'.format(n) for n in deck1)))
        #print('Player 2: {}'.format(', '.join('{}'.format(n) for n in deck2)))
        #print()

def calculate_score(deck: List[int]) -> int:
    score = 0
    #print('Score')
    #print('   0')
    for i, card in enumerate(reversed(deck)):
        #print('+ {:2} * {:2}'.format(card, i + 1))
        score += card * (i + 1)
    #print('----')
    #print(f'Score: {score}')

    return score

def main():
    # Read input file
    player1, player2 = read_input_file('day22_input.txt')

    ############ PART ONE ############

    play_combat(player1, player2)
    winner = player1 if len(player2) == 0 else player2
    print('Score from game of Combat: {}'.format(calculate_score(winner)))

if __name__ == '__main__':
    main()
