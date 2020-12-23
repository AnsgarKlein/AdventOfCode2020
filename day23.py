#!/usr/bin/env python3

from typing import List

def read_input_file(filename):
    with open(filename, 'r') as input_file:
        return [int(num) for num in input_file.read() if num != '\n']

def moves(cups: List[int], num_moves: int):
    move_id = 1
    current_id = 0
    len_cups = len(cups)

    for _ in range(num_moves):
        current = cups[current_id]

        print(f'-- move {move_id} --')
        print('cups: {}'.format(' '.join(['({})'.format(c) if c == current else str(c) for c in cups])))

        # Determine index of 3 cups after current cup
        removed_ids = [(current_id + i) % len_cups for i in range(1,4)]

        # Determine 3 cups after current cup
        removed = [cups[removed_id] for removed_id in removed_ids]

        # Pick up 3 cups after current cup
        for removed_id in sorted(removed_ids, reverse = True):
            del cups[removed_id]
            if removed_id < current_id:
                current_id -= 1

        print('pick up: {}'.format(', '.join([str(i) for i in removed])))

        # Select destination cup
        destination = current - 1
        while destination < 1 or destination > len_cups or destination in removed:
            destination = (destination - 1) % (len_cups + 1)

        print('destination: {}\n'.format(destination))

        # Put 3 picked up cups behind destination cup
        destination_id = cups.index(destination) + 1
        if destination_id - 1 < current_id:
            current_id += 3
        cups[destination_id:destination_id] = removed

        # Next cup is the one after the current cup
        current_id = (current_id + 1) % len_cups
        move_id += 1

    print('-- final --')
    print('cups: {}\n'.format(' '.join(['({})'.format(c) if c == current else str(c) for c in cups])))

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

if __name__ == '__main__':
    main()
