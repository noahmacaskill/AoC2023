INPUT = "input"
NUM_STEPS = 64

with open(INPUT) as f:
    map = f.readlines()

MAX_ROW = len(map)
MAX_COL = len(map[0][:-1])

rocks = []
start = None

move_north = lambda row, col: (row-1, col)
move_east = lambda row, col: (row, col+1)
move_south = lambda row, col: (row+1, col)
move_west = lambda row, col: (row, col-1)

# Returns coords of 4 points surrounding given point
def next_positions(pt: tuple[int, int]):
    return [move_north(*pt), move_east(*pt), move_south(*pt), move_west(*pt)]

for i, line in enumerate(map):
    line = line.strip()

    for j, plot in enumerate(line):
        if plot == '#':
            rocks.append((i, j))
        elif plot == 'S':
            start = (i, j)

# Keeps track of points points reached at each step
# Note alternating parities (possible plots alternate in checkerboard pattern)
cur_parity_plts, last_parity_plts = set([start]), set()
cur_plts, last_plts = set(), set([start])
for i in range(NUM_STEPS):
    cur_parity_plts, last_parity_plts = last_parity_plts, cur_parity_plts

    for plt in last_plts:
        for next_plt in next_positions(plt):
            if next_plt not in rocks and 0 <= next_plt[0] <= MAX_ROW and 0 <= next_plt[1] <= MAX_COL and next_plt not in cur_parity_plts:
                cur_plts.add(next_plt)
    
    cur_parity_plts.update(cur_plts)
    cur_plts, last_plts = set(), cur_plts

print(f"ANSWER: {len(cur_parity_plts)}")
