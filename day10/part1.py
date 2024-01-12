with open("input", "r") as f:
    pipe_grid = f.readlines()

pipe_grid = [line[:-1] for line in pipe_grid]

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

start = None
for row, line in enumerate(pipe_grid):
    for col, pipe in enumerate(line[:-1]):
        if pipe == 'S':
            start = (row, col)
    
    if start is not None:
        break

pipe_starts = [move_north(start) + ('S',), move_east(start) + ('W',), move_south(start) + ('N',), move_west(start) + ('E',)]
pipe_ends = []
last_pipe = None
pipe_length = 1
for pipe in pipe_starts:
    if pipe[:-1] in pipe_ends:
        continue

    pipe_shape = pipe_grid[pipe[0]][pipe[1]]
    pipe = pipe_functions[pipe_shape](pipe)
    
    if pipe == -1:
        continue

    pipe_length += 1
    while pipe[:-1] != start:
        last_pipe = pipe
        pipe_shape = pipe_grid[pipe[0]][pipe[1]]
        pipe = pipe_functions[pipe_shape](pipe)
        pipe_length += 1
    
    pipe_ends.append(last_pipe[:-1])

print(f"ANSWER: {int(pipe_length/2)}")