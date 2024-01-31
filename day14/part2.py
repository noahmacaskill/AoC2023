from typing import List
import bisect

INPUT = "input"

with open(INPUT, "r") as f:
    platform = f.readlines()

# Length and width are equivalent
DIMENSION = len(platform)
NUM_CYCLES = 1000000000

cube_rock_cols = [[] for _ in  range(DIMENSION)]
cube_rock_rows = [[] for _ in  range(DIMENSION)]
reversed_cube_rock_cols = [[] for _ in  range(DIMENSION)]
reversed_cube_rock_rows = [[] for _ in  range(DIMENSION)]
north_distances = [[] for _ in  range(DIMENSION)]

for i, row in enumerate(platform):
    for j, space in enumerate(row):
        if space == 'O':
            north_distances[j].append(i)
        elif space == '#':
            bisect.insort(cube_rock_cols[j], i)
            bisect.insort(reversed_cube_rock_rows[DIMENSION-i-1], j)
            bisect.insort(reversed_cube_rock_cols[DIMENSION-j-1], DIMENSION-i-1)
            bisect.insort(cube_rock_rows[i], DIMENSION-j-1)

def complete_cycle(distances: List[List[int]]) -> List[List[int]]:
    """
    Completes one spin cycle by tilting north, west, south, then east

    Parameters:
    distances (List[List[int]]): Distances of rounded rocks from the edge for which the platform will be tilted
        - Each individual list represents one column of rocks    
    
    Returns:
    List[List[int]]: Distances of rounded rocks from the north edge

    """
    distances = tilt(distances, cube_rock_cols)
    distances = tilt(distances, reversed_cube_rock_rows)
    distances = tilt(distances, reversed_cube_rock_cols)
    distances = tilt(distances, cube_rock_rows)

    return distances

def tilt(distances: List[List[int]], cube_rocks: List[List[int]]) -> List[List[int]]:
    """
    Tilts platform

    Parameters:
    distances (List[List[int]]): Distances of rounded rocks from the edge for which the platform will be tilted
        - Each individual list represents one row or column of rocks
    cube_rocks(List[List[int]]): Distances of cube rocks from the edge for which the platform will be tilted
        - Each individual list represents one row or column of rocks
    
    Returns:
    List[List[int]]: Distances of rounded rocks from the next edge for which the platform will be tilted
    """
    next_distances = [[] for _ in range(DIMENSION)]
    for ind, axis in enumerate(distances):
        cube_iterator = iter(cube_rocks[ind])
        fall_ind = 0
        cube = next(cube_iterator, None)
        for rock in axis:
            if cube == None or rock < cube:
                next_distances[DIMENSION-fall_ind-1].append(ind)
                fall_ind += 1
            else:
                prev_cube = None
                while cube != None and cube < rock:
                    prev_cube = cube
                    cube = next(cube_iterator, None)
                    
                next_distances[DIMENSION-(prev_cube+1)-1].append(ind)
                fall_ind = prev_cube+2
    
    return next_distances

def calculate_load(distances: List[List[int]]) -> int:
    """
    Calculates the total load on the north support beams

    Parameters:
    distances (List[List[int]]): Distances of rounded rocks from the edge for which the platform will be tilted
        - Each individual list represents one row or column of rocks

    Returns:
    int: The total load on teh north support beams        
    """
    load = 0
    for rock in [rock for axis in distances for rock in axis]:
        load += DIMENSION-rock

    return load

distances = {}
cycles = 0
while cycles < (NUM_CYCLES):
    north_distances = complete_cycle(north_distances)
    cycles += 1

    repeat_cycles = distances.get(tuple(tuple(axis) for axis in north_distances))
    if repeat_cycles is not None:
        cycles = NUM_CYCLES - ((NUM_CYCLES-cycles) % (cycles-repeat_cycles))

    distances[tuple(tuple(axis) for axis in north_distances)] = cycles

total_load = calculate_load(north_distances)

print(f"ANSWER: {total_load}")

