#!/usr/bin/env python3

from typing import List
from typing import Set
from typing import Tuple

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

def play_recursive_combat(deck1: List[int], deck2: List[int], game_id = 1):
    previous: Set[Tuple[Tuple[int, ...], Tuple[int, ...]]] = set()

    # Printing of status slows down execution significantly
    verbose = False

    if verbose:
        print('=== Game {} ===\n'.format(game_id))

    # Play until someone wins
    round_id = 0
    while True:
        round_id += 1
        round_winner = None

        if verbose:
            print('-- Round {:2} (Game {}) --'.format(round_id, game_id))
            print('Player 1\'s deck: {}'.format(', '.join((str(i) for i in deck1))))
            print('Player 2\'s deck: {}'.format(', '.join((str(i) for i in deck2))))

        # If there was a previous round in this game that had exactly
        # the same cards in the same order in the same players' decks,
        # THE GAME instantly ends in a win for player1
        if (tuple(deck1), tuple(deck2)) in previous:
            # Player 1 wins
            if verbose:
                print('Deck configuration already happened - Player 1 wins game!\n')
            return 1
        previous.add((tuple(deck1), tuple(deck2)))

        # Draw cards
        card1 = deck1.pop(0)
        card2 = deck2.pop(0)

        if verbose:
            print('Player 1 plays: {:2}'.format(card1))
            print('Player 2 plays: {:2}'.format(card2))

        if len(deck1) >= card1 and len(deck2) >= card2:
            # If both players have at least as many cards in their deck
            # as the value of the card they drew - winner of round is determined
            # by playing new game of recursive combat.

            deck1_recurse = deck1.copy()[:card1]
            deck2_recurse = deck2.copy()[:card2]

            if verbose:
                print('Playing a sub-game to determine the winner ...\n')

            round_winner_id = play_recursive_combat(deck1_recurse, deck2_recurse, game_id + 1)
            round_winner = deck1 if round_winner_id == 1 else deck2

            if verbose:
                print(f'\nback to game {game_id}\n')
        else:
            # At least one player has not enough cards to recurse.
            # The winner is the player with the higher-value card.
            round_winner = deck1 if card1 > card2 else deck2

        # Now that we have a winner of this round, add the cards to
        # the winner in the proper order
        if verbose:
            print('Winner of round {} (game {}) is Player {}\n'.format(
                round_id,
                game_id,
                '1' if round_winner == deck1 else '2'))

        if round_winner is deck1:
            deck1.append(card1)
            deck1.append(card2)
        elif round_winner is deck2:
            deck2.append(card2)
            deck2.append(card1)

        # If a player collects all cards they win
        if not deck1:
            if verbose:
                print('Player 1 has no cards left - Player 2 wins game!\n')
            return 2
        if not deck2:
            if verbose:
                print('Player 2 has no cards left - Player 1 wins game!\n')
            return 1

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
    ############ PART ONE ############

    # Read input file
    player1, player2 = read_input_file('day22_input.txt')

    play_combat(player1, player2)
    winner = player1 if len(player2) == 0 else player2
    print('Score from game of Combat: {}'.format(calculate_score(winner)))


    ############ PART TWO ############

    # Read original deck state again
    player1, player2 = read_input_file('day22_input.txt')

    winner_id = play_recursive_combat(player1, player2)
    winner = player1 if winner_id == 1 else player2
    print('Score from game of recursive Combat: {}'.format(calculate_score(winner)))

if __name__ == '__main__':
    main()
