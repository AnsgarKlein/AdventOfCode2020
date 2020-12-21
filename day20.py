#!/usr/bin/env python3

from typing import List
from typing import Optional

import math

class Tile:
    def __init__(self, content: List[List[str]], index: int):
        self.index = index
        self.content = content

    def __str__(self) -> str:
        txt = 'Tile {}\n'.format(self.index)
        txt += '\n'.join([ ''.join(line) for line in self.content ])
        return txt

    def __eq__(self, other):
        return self.content == other.content

    def rotate(self, number = 1) -> 'Tile':
        rotated_tile = self

        for _ in range(number):
            # Create empty array
            length = len(self.content)
            new_content = [ [''] * length for x in range(length) ]

            # Copy content as rotated
            for y, line in enumerate(self.content):
                for x, char in enumerate(line):
                    new_content[x][length - y - 1] = char

            rotated_tile = Tile(new_content, self.index)

        return rotated_tile

    def flip_h(self) -> 'Tile':
        # Create empty array
        length = len(self.content)
        new_content = [ [''] * length for x in range(length) ]

        # Flip content to new array
        for y, line in enumerate(self.content):
            for x, char in enumerate(line):
                new_content[y][abs(length - x) - 1] = char

        return Tile(new_content, self.index)

    def flip_v(self) -> 'Tile':
        # Create empty array
        length = len(self.content)
        new_content = [ [''] * length for x in range(length) ]

        # Flip content to new array
        for y, line in enumerate(self.content):
            for x, char in enumerate(line):
                new_content[abs(length - y) - 1][x] = char

        return Tile(new_content, self.index)

    def permutations(self) -> List['Tile']:
        perms = []
        perms.append(self)
        perms.append(self.rotate(1))
        perms.append(self.rotate(2))
        perms.append(self.rotate(3))
        perms.append(self.flip_h())
        perms.append(self.flip_h().rotate(1))
        perms.append(self.flip_v())
        perms.append(self.flip_v().rotate(1))
        perms.append(self.flip_h().flip_v())
        perms.append(self.flip_h().flip_v().rotate(1))
        return perms

    @property
    def top(self) -> str:
        return ''.join(self.content[0])

    @property
    def bottom(self) -> str:
        return ''.join(self.content[-1])

    @property
    def left(self) -> str:
        return ''.join([ line[0] for line in self.content ])

    @property
    def right(self) -> str:
        return ''.join([ line[-1] for line in self.content ])

    def fits_permutated_above(self, other) -> Optional['Tile']:
        for perm in other.permutations():
            if self.fits_above(perm):
                return perm
        return None

    def fits_permutated_below(self, other) -> Optional['Tile']:
        for perm in other.permutations():
            if self.fits_below(perm):
                return perm
        return None

    def fits_permutated_left(self, other) -> Optional['Tile']:
        for perm in other.permutations():
            if self.fits_left(perm):
                return perm
        return None

    def fits_permutated_right(self, other) -> Optional['Tile']:
        for perm in other.permutations():
            if self.fits_right(perm):
                return perm
        return None

    def fits_above(self, other) -> bool:
        return self.top == other.bottom

    def fits_below(self, other) -> bool:
        return self.bottom == other.top

    def fits_left(self, other) -> bool:
        return self.left == other.right

    def fits_right(self, other) -> bool:
        return self.right == other.left

def parse_input_file(filename):
    tiles = []

    with open(filename, 'r') as input_file:
        content = input_file.read().split('\n')

        txt = []

        for line in content:
            if line.strip() == '':
                # Create new tile
                index = int(''.join(txt[0]).split(' ')[1][:-1])
                content = txt[1:]
                tiles.append(Tile(content, index))
                txt = []
            else:
                txt.append(list(line))


    return tiles

def main():
    # Read input file
    tiles = parse_input_file('day20_input.txt')


    ############ PART ONE ############

    # Corner tiles have only 2 tiles that fit beside them in any permutation
    corner_tiles = []

    # Side tiles have only 3 tiles that fit beside them in any permutation
    side_tiles = []

    # Middle tiles have 4 tiles that fit all around them
    middle_tiles = []

    # Check what tiles fit next to every tile
    for tile in tiles:
        matching_tiles = 0
        for other in (t for t in tiles if t is not tile):
            if tile.fits_permutated_above(other) is not None:
                matching_tiles += 1
            if tile.fits_permutated_below(other) is not None:
                matching_tiles += 1
            if tile.fits_permutated_left(other) is not None:
                matching_tiles += 1
            if tile.fits_permutated_right(other) is not None:
                matching_tiles += 1

        print('Tile {} has {} tiles fitting next to it'.format(tile.index, matching_tiles))

        if matching_tiles == 2:
            corner_tiles.append(tile)
        elif matching_tiles == 3:
            side_tiles.append(tile)
        elif matching_tiles == 4:
            middle_tiles.append(tile)
        else:
            # If for one tile we have less than 2 matching tiles something
            # is broken.
            # If for one tile we have more than 4 matching tiles the image
            # cannot be assembled unambiguously:
            #   Multiple tiles could function as a corner tile at first look
            #   but assembly of image would not work out when inserting side
            #   and middle tiles.
            print('error')

    # There should be exactly four corner tiles
    assert len(corner_tiles) == 4
    assert len(side_tiles) == (math.sqrt(len(tiles)) -2) * 4
    assert len(middle_tiles) == len(tiles) - len(side_tiles) - len(corner_tiles)

    print('Corner Tiles: {}'.format(len(corner_tiles)))
    print('Side Tiles:   {}'.format(len(side_tiles)))
    print('Middle Tiles: {}'.format(len(middle_tiles)))

    # Print checksum of corner tiles
    checksum = 1
    for corner_tile in corner_tiles:
        checksum *= corner_tile.index
    print('Corner Checksum: {}'.format(checksum))

    # Create empty image
    root = int(math.sqrt(len(tiles)))
    image = [ [ None for x in range(root) ] for x in range(root) ]

    # Now put together image ...

if __name__ == '__main__':
    main()
