#!/usr/bin/env python3

from typing import List

import sys

def read_input_file(filename):
    with open(filename, 'r') as input_file:
        return [int(num) for num in input_file.read() if num != '\n']

def moves(cups: List[int], num_moves: int, verbose = True):
    move_id = 1
    current_id = 0
    len_cups = len(cups)

    if not verbose:
        print('Move: 0', end = '')

    for _ in range(num_moves):
        current = cups[current_id]

        if verbose:
            print(f'-- move {move_id} --')
            print('cups: {}'.format(' '.join(['({})'.format(c) if c == current else str(c) for c in cups])))
        else:
            print(f'\rMove: {move_id}', end = '')
            sys.stdout.flush()

        # Determine index of 3 cups after current cup
        removed_ids = [(current_id + i) % len_cups for i in range(1,4)]

        # Determine 3 cups after current cup
        removed = [cups[removed_id] for removed_id in removed_ids]

        # Pick up 3 cups after current cup
        for removed_id in sorted(removed_ids, reverse = True):
            del cups[removed_id]
            if removed_id < current_id:
                current_id -= 1

        if verbose:
            print('pick up: {}'.format(', '.join([str(i) for i in removed])))

        # Select destination cup
        destination = current - 1
        while destination < 1 or destination > len_cups or destination in removed:
            destination = (destination - 1) % (len_cups + 1)

        if verbose:
            print('destination: {}\n'.format(destination))

        # Put 3 picked up cups behind destination cup
        destination_id = cups.index(destination) + 1
        if destination_id - 1 < current_id:
            current_id += 3
        cups[destination_id:destination_id] = removed

        # Next cup is the one after the current cup
        current_id = (current_id + 1) % len_cups
        move_id += 1

    if verbose:
        print('-- final --')
        print('cups: {}\n'.format(' '.join(['({})'.format(c) if c == current else str(c) for c in cups])))
    else:
        print()

def main():
    ############ PART ONE ############

    # Read input file
    cups = read_input_file('day23_input.txt')

    # Play 100 moves
    moves(cups, 100)

    # Print checksum
    checksum = cups.copy()
    while checksum[0] != 1:
        checksum.append(checksum.pop(0))
    print('Checksum: {}\n'.format(''.join((str(e) for e in checksum if e != 1))))


    ############ PART TWO ############

    # Read input again
    cups = read_input_file('day23_input.txt')

    # Extend cups to one million cups
    cups.extend(list(range(max(cups) + 1, 1_000_000 + 1)))
    assert len(cups) == 1_000_000

    # Play ten million moves
    # This works but depending on CPU takes more
    # than 20 hours to finish.
    moves(cups, 10_000_000, False)

    # Print checksum of two cups after cup 1
    c1 = cups[(cups.index(1)  + 1) % len(cups)]
    c2 = cups[(cups.index(c1) + 1) % len(cups)]
    print('Checksum: {} ({}, {})'.format(c1 * c2, c1, c2))

if __name__ == '__main__':
    main()
