from typing import List
from collections import deque

INPUT = "input"

with open(INPUT, "r") as f:
    pipe_grid = f.readlines()

pipe_grid = [s.rstrip('\n') for s in pipe_grid]
pipe_grid = [list(string) for string in pipe_grid]

"""
Functions to move to adjacent pipe (north, south, east or west)

Parameters:
pt (tuple[int, int]): Pipe location in grid

Returns:
tuple[int, int]: The adjacent pipe
"""
def move_north(pt: tuple[int, int]): return (pt[0]-1, pt[1])
def move_east(pt: tuple[int, int]): return (pt[0], pt[1]+1)
def move_south(pt: tuple[int, int]): return (pt[0]+1, pt[1])
def move_west(pt: tuple[int, int]): return (pt[0], pt[1]-1)

"""
Functions to move to next pipe according to pipe shape

Parameters:
x (tuple[int, int, str]):
    - int: row location of pipe
    - int: col location of pipe
    - str: incoming direction into pipe ('N', 'S', 'E' or 'W')

Returns:
tuple[int, int, str]: Next pipe (same tuple format as above)
"""
pipe_functions = {
    '|': lambda x: move_north((x[0], x[1])) + ('S',) if x[2] == 'S' else move_south((x[0], x[1])) + ('N',) if x[2] == 'N' else -1,
    '-': lambda x: move_east((x[0], x[1])) + ('W',) if x[2] == 'W' else move_west((x[0], x[1])) + ('E',) if x[2] == 'E' else -1,
    'L': lambda x: move_north((x[0], x[1])) + ('S',) if x[2] == 'E' else move_east((x[0], x[1])) + ('W',) if x[2] == 'N' else -1,
    'J': lambda x: move_north((x[0], x[1])) + ('S',) if x[2] == 'W' else move_west((x[0], x[1])) + ('E',) if x[2] == 'N' else -1,
    '7': lambda x: move_south((x[0], x[1])) + ('N',) if x[2] == 'W' else move_west((x[0], x[1])) + ('E',) if x[2] == 'S' else -1,
    'F': lambda x: move_south((x[0], x[1])) + ('N',) if x[2] == 'E' else move_east((x[0], x[1])) + ('W',) if x[2] == 'S' else -1,
    '.': lambda _: -1
}

"""
Dictionary representing whether the pipe has turned left or right

First level key (str): Pipe shape
Second level key (str): Incoming direction into pipe

-1: Left turn
1: Right turn
"""
pipe_turn = {
    'L': {'N': -1, 'E': 1},
    'J': {'N': 1, 'W': -1},
    '7': {'S': -1, 'W': 1},
    'F': {'S': 1, 'E': -1},
}

"""
Dictionary representing the right side(s) of each pipe shape depending on incoming pipe direction
Used to determine which values are "inside the pipe" vs "outside the pipe"

First level key (str): Pipe shape
Second level key (str): Incoming direction into pipe
"""
pipe_right_sides = {
    '|': {'N': ['W'], 'S': ['E']},
    '-': {'E': ['N'], 'W': ['S']},
    'L': {'N': ['W', 'S'], 'E': []},
    'J': {'N': [], 'W': ['S', 'E']},
    '7': {'S': ['E', 'N'], 'W': []},
    'F': {'S': [], 'E': ['N', 'W']}
}

def enclosed(right_loop: bool, pipe_shape: str, pipe_direction: str, approach_direction: str) -> bool:
    """
    Determines whether a section is enclosed by the pipe loop
    
    Parameters:
    right_loop (bool): True if more right hand turns are taken along the loop than left, else false
    pipe_shape (str): Shape of the pipe (i.e. 7, F, etc.)
    pipe_direction (str): Incoming direction into the pipe (N, E, S or W)
    approach_direction (str): Direction from which section is approaching loop (N, E, S or W)

    Returns:
    bool: Whether section is enclosed by pipe loop

    LOGIC: If the pipe loop takes more right hand turns than left hand turns, then sections of non-loop tiles
    that approach the pipe from the right will be enclosed by the loop, and from the left outside the loop.
    The inverse is true if more left hand turns are taken than right.
    """

    pipe_right_approaches = pipe_right_sides[pipe_shape][pipe_direction]
    right_approach = approach_direction in pipe_right_approaches

    return right_loop == right_approach

def flood_fill(x: int, y: int, pipe_cycle: List[tuple[int, int]]) -> tuple[tuple[tuple[int, int], str], int]:
    """
    Identififes a section of the grid, filling until boundaries are met (pipe cycle or outer boundary)

    Parameters:
    x (int): Starting x coordinate
    y (int): Starting y coordinate
    pipe_cycle (List[tuple[int, int]]): Locations containing pipes in cycle

    Returns:
    tuple[tuple[tuple[int, int], str], int]:
        tuple[tuple[int, int], str]: pipe cycle tile bordering the section
            tuple[int, int]: x, y coordinates of tile
            str: incoming direction to tile (N, E, S, W)
        int: Section size (number of tiles)
    """
    queue = deque([((x, y), None)])
    border = None
    section_size = 0

    while queue:
        (x, y), dir = queue.popleft()

        if 0 <= x < len(pipe_grid) and 0 <= y < len(pipe_grid[0]) and pipe_grid[x][y] != '*':
            if (x, y) in pipe_cycle:
                if pipe_grid[x][y] != 'S':
                    border = ((x, y), dir)
            else:
                pipe_grid[x][y] = '*'
                section_size += 1

                for dir, func in zip(['S', 'W', 'N', 'E'], [move_north, move_east, move_south, move_west]):
                    new_x, new_y,  = func((x, y))
                    queue.append(((new_x, new_y), dir))
    
    return (border, section_size)

# 1. Find Start tile
start = None
for row, line in enumerate(pipe_grid):
    for col, pipe in enumerate(line[:-1]):
        if pipe == 'S':
            start = (row, col)
            break
    
    if start is not None:
        break

# 2. Identfify pipe cycle
# Pipe convention used (tuple[int, int, str]): x coordinate, y coordinate, incoming direction (N, E, S, W)
pipe_starts = [move_north(start) + ('S',), move_east(start) + ('W',), move_south(start) + ('N',), move_west(start) + ('E',)]
pipe_ends = []
last_pipe = None
pipe_cycle = {}
turn_tally = 0
for pipe in pipe_starts:
    if pipe_cycle != {}:
        break
    if pipe[:-1] in pipe_ends:
        continue

    while pipe[:-1] != start:
        pipe_cycle[(pipe[0], pipe[1])] = pipe[2]
        last_pipe = pipe
        pipe_shape = pipe_grid[pipe[0]][pipe[1]]
        turn_tally += pipe_turn.get(pipe_shape, {}).get(pipe[2], 0)
        pipe = pipe_functions[pipe_shape](pipe)
        if pipe == -1:
            pipe_cycle = {}
            turn_tally = 0
            break

    if pipe != -1:
        pipe_ends.append(last_pipe[:-1])
        pipe_cycle[start] = pipe[2]

# 3. Identify connected sections of tiles, determine whether they are enclosed by the loop or not
pipe_cycle_locations = list(pipe_cycle.keys())
enclosed_tiles = 0
for x in range(len(pipe_grid)):
    for y in range(len(pipe_grid[0])):
        if pipe_grid[x][y] != '*' and (x, y) not in pipe_cycle_locations:
            border, section_size = flood_fill(x, y, pipe_cycle_locations)

            if enclosed(turn_tally>0, pipe_grid[border[0][0]][border[0][1]], pipe_cycle[border[0]], border[1]):
                enclosed_tiles += section_size

print(f"ANSWER: {enclosed_tiles}")
