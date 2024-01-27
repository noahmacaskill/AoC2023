import numpy as np

INPUT = "input"
PART1 = True

NUM_STEPS = 26501365

with open(INPUT) as f:
    map = f.readlines()

# Grid is square
MAX_DIM = len(map)

rocks = []
start = None

move_north = lambda row, col: ((row-1), col)
move_east = lambda row, col: (row, (col+1))
move_south = lambda row, col: ((row+1), col)
move_west = lambda row, col: (row, (col-1))

# Projects a point from neighbouring grids into initial grid point to check for rocks
project_point = lambda row, col: (row%MAX_DIM, col%MAX_DIM)

# Returns coords of 4 points surrounding given point
def next_positions(pt: tuple[int, int]):
    return [move_north(*pt), move_east(*pt), move_south(*pt), move_west(*pt)]

"""
Note that this solution works for this specific input as it happens to work in a quadratic cycle at steps (MAX_DIM-1/2) + n*MAX_DIM

This is due to our starting point being exactly in the middle of the grid, and the relatively few number of rocks allowing for
nice diamond formations to be made at each cycle interval
"""

for i, line in enumerate(map):
    line = line.strip()

    for j, plot in enumerate(line):
        if plot == '#':
            rocks.append((i, j))
        elif plot == 'S':
            start = (i, j)

cur_parity_plts, last_parity_plts = set([start]), set()
cur_plts, last_plts = set(), set([start])
last_same_parity = set()
cycle_steps = []
steps = 0
while len(cycle_steps) < 3:
    cur_parity_plts, last_parity_plts = last_parity_plts, cur_parity_plts

    for plt in last_plts:
        for next_plt in next_positions(plt):
            if project_point(*next_plt) not in rocks and next_plt not in last_same_parity:
                cur_plts.add(next_plt)
    
    cur_parity_plts.update(cur_plts)
    cur_plts, last_plts, last_same_parity = set(), cur_plts, last_plts
    steps += 1

    # Record step count at instance of quadratic repetition
    if (steps-((MAX_DIM-1)/2))%MAX_DIM == 0:
        cycle_steps.append((steps, len(cur_parity_plts)))

# Determine the general form of the quadratic cycle
cycle1, cycle2, cycle3 = tuple(cs[0] for cs in cycle_steps)
A = np.array([
    [cycle1**2, cycle1, 1],
    [cycle2**2, cycle2, 1],
    [cycle3**2, cycle3, 1]
])

B = np.array([cycle_steps[0][1], cycle_steps[1][1], cycle_steps[2][1]])
a, b, c = np.linalg.solve(A, B)

num_possibilities = a*(NUM_STEPS**2) + b*NUM_STEPS + c

print(f"ANSWER: {num_possibilities}")
