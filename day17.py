#!/usr/bin/env python3

from typing import Dict
from typing import List
from typing import Tuple

import sys
from collections import namedtuple

Cube = namedtuple('Cube', 'x y z')
HyperCube = namedtuple('HyperCube', 'x y z w')

def print_cubes(cubes: List[Cube]):
    assert len(cubes[0]) == 3

    max_x, max_y, max_z = max_dimensions(cubes)
    min_x, min_y, min_z = min_dimensions(cubes)

    # Print everything
    for z in range(min_z, max_z + 1):
        print('z={}'.format(z))
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                if (x, y, z) in cubes:
                    print('#', end = '')
                else:
                    print('.', end = '')
            print()
        print('\n')

def min_dimensions(cubes: List[Cube]) -> Tuple[int, int, int]:
    min_x = min((cube.x for cube in cubes))
    min_y = min((cube.y for cube in cubes))
    min_z = min((cube.z for cube in cubes))

    return min_x, min_y, min_z

def max_dimensions(cubes: List[Cube]) -> Tuple[int, int, int]:
    max_x = max((cube.x for cube in cubes))
    max_y = max((cube.y for cube in cubes))
    max_z = max((cube.z for cube in cubes))

    return max_x, max_y, max_z

def neighbor_cubes(cube: Cube) -> List[Cube]:
    assert len(cube) == 3

    others = []
    for z in [ cube.z, cube.z - 1, cube.z + 1 ]:
        for y in [ cube.y, cube.y - 1, cube.y + 1 ]:
            for x in [ cube.x, cube.x - 1, cube.x + 1 ]:
                others.append(Cube(x, y, z))

    # Cube is not a neighbor of itself
    others.remove(cube)

    assert len(others) == 26

    return others

def neighbor_hypercubes(cube: HyperCube) -> List[HyperCube]:
    assert len(cube) == 4

    others = []
    for w in [ cube.w, cube.w - 1, cube.w + 1 ]:
        for z in [ cube.z, cube.z - 1, cube.z + 1 ]:
            for y in [ cube.y, cube.y - 1, cube.y + 1 ]:
                for x in [ cube.x, cube.x - 1, cube.x + 1 ]:
                    others.append(HyperCube(x, y, z, w))

    # Cube is not a neighbor of itself
    others.remove(cube)

    assert len(others) == 80

    return others

def active_neighbors(cube: Cube, active_cubes: List[Cube]) -> int:
    count = 0
    for neighbor in neighbor_cubes(cube):
        if neighbor in active_cubes:
            count += 1

    return count

def read_input_file(filename) -> List[Cube]:
    cubes = []

    with open(filename, 'r') as input_file:
        content = input_file.read().split('\n')

        for y, line in enumerate(content):
            for x, char in enumerate(line):
                state = (char == '#')
                if state:
                    cubes.append(Cube(x, y, 0))

    return cubes

def cycle_cubes(cubes: List[Cube]) -> List[Cube]:
    assert len(cubes[0]) == 3

    max_x, max_y, max_z = max_dimensions(cubes)
    max_x += 1
    max_y += 1
    max_z += 1
    min_x, min_y, min_z = min_dimensions(cubes)
    min_x -= 1
    min_y -= 1
    min_z -= 1

    # Add cubes after cycle to new list
    new_cubes: List[Cube] = []

    for z in range(min_z, max_z + 1):
        for y in range(min_y, max_y + 1):
            for x in range(min_x, max_x + 1):
                current = Cube(x, y, z)
                neighbors = active_neighbors(current, cubes)

                # Check if cube is currently active
                if current in cubes:
                    # Cube is currently active
                    if neighbors in [2, 3]:
                        # Cube stays active
                        new_cubes.append(current)
                    else:
                        # Cube becomes inactive
                        pass
                else:
                    # Cube is currently inactive
                    if neighbors == 3:
                        # Cube becomes active
                        new_cubes.append(current)
                    else:
                        # Cube stays inactive
                        pass

    return new_cubes

def cycle_hypercubes(cubes: List[HyperCube]) -> List[HyperCube]:
    assert len(cubes[0]) == 4

    # Add cubes after cycle to new list
    new_cubes: List[HyperCube] = []

    # Map all neighbors (those that might become active)
    # of active nodes to their active neighbor count
    cube_neighbor: Dict[HyperCube, int] = dict()
    for current in cubes:
        for neighbor in neighbor_hypercubes(current):
            if neighbor not in cube_neighbor:
                cube_neighbor[neighbor] = 1
            else:
                cube_neighbor[neighbor] += 1

    # Cubes with 3 neighbors become active
    # Cubes with 2 neighbors only stay active
    for current, count in cube_neighbor.items():
        if count == 3:
            new_cubes.append(current)
        elif count == 2 and current in cubes:
            new_cubes.append(current)

    return new_cubes

def main():
    # Read input file
    cubes = read_input_file('day17_input.txt')


    ############ PART ONE ############

    # Cycle six times
    new_cubes = cubes
    print('Booting up experimental pocket dimension ', end = '')
    for _ in range(6):
        new_cubes = cycle_cubes(new_cubes)
        print('.', end = '')
        sys.stdout.flush()
    print('')

    print('Cubes in active state after bootup: {}'.format(len(new_cubes)))


    ############ PART TWO ############

    # Convert cubes to hypercubes
    print('Converting 3 dimensions to Hypercubes ...')
    hypercubes = [ HyperCube(cube.x, cube.y, cube.z, 0) for cube in cubes ]

    # Cycle six times
    new_hypercubes = hypercubes
    print('Booting up experimental 4D pocket dimension ', end = '')
    for _ in range(6):
        new_hypercubes = cycle_hypercubes(new_hypercubes)
        print('.', end = '')
        sys.stdout.flush()
    print('')

    print('Hypercubes in active state after bootup: {}'.format(len(new_hypercubes)))

if __name__ == '__main__':
    main()
