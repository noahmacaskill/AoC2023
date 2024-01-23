with open("input", "r") as f:
    grid = f.readlines()

MAX_ROW = len(grid) - 1
MAX_COL = len(grid[0][:-1]) - 1

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

EMPTY = '.'
UP_MIRROR = '/'
DOWN_MIRROR = '\\'
HOR_SPLITTER = '-'
VER_SPLITTER = '|'

def track_light(start_point: tuple[tuple[int, int], int]) -> set[tuple[int, int]]:
    """
    Follows the light path, keeping track of energized tiles

    Parameters:
    start_point (tuple[tuple[int, int], int]):
        tuple[int, int]:
            int: row of current point
            int: col of current point
        int: Direction from which light entered point
    
    Returns:
    set[tuple[int, int]]: Energized point (row, col)
    """
    energized_tiles = set()
    visited_pts = []
    current_pts = [start_point]

    while current_pts:
        energized_tiles.update(pt[0] for pt in current_pts)
        visited_pts += current_pts
        current_pts = sum(map(next_point, current_pts), [])
        current_pts = [pt for pt in current_pts if pt not in visited_pts and pt is not None]
    
    return energized_tiles

def next_point(point: tuple[tuple[int, int], int]) -> tuple[tuple[int, int], int]:
    """
    Determine the next tile that the light traverses across

    Parameters:
    point (tuple[tuple[int, int], int]):
        tuple[int, int]:
            int: row of current point
            int: col of current point
        int: Direction from which light entered point
    
    returns:
    tuple[tuple[int, int], int]: Next point in same format as parameter
    """
    (row, col), dir = point
    tile = grid[row][col]

    if tile == EMPTY or (tile == HOR_SPLITTER and dir in (EAST, WEST)) or (tile == VER_SPLITTER and dir in (NORTH, SOUTH)):
        return [move_point(row, col, (dir+2)%4)]
    elif tile == UP_MIRROR:
        if dir%2 == 0:
            return [move_point(row, col, (dir-1)%4)]
        else:
            return [move_point(row, col, (dir+1)%4)]
    elif tile == DOWN_MIRROR:
        if dir%2 == 0:
            return [move_point(row, col, dir+1)]
        else:
            return [move_point(row, col, dir-1)]
    elif tile == HOR_SPLITTER:
        return [move_point(row, col, EAST), move_point(row, col, WEST)]
    else: # splitting vertically
        return [move_point(row, col, NORTH), move_point(row, col, SOUTH)]

def move_point(row: int, col: int, dir: int) -> tuple[tuple[int, int], int]:
    """
    Moves a point according to a given direction

    Parameters:
    row (int): row of incoming point
    col (int): col of incoming point
    dir (int): Direction to follow to next point

    Returns:
    (tuple((int, int), int)): Next point after shifting dir, or None if point is out of grid bounds
    """
    if dir == NORTH and row > 0:
        return ((row-1, col), SOUTH)
    elif dir == EAST and col < MAX_COL:
        return ((row, col+1), WEST)
    elif dir == SOUTH and row < MAX_ROW:
        return ((row+1, col), NORTH)
    elif dir == WEST and col > 0:
        return ((row, col-1), EAST)
    
    return None

start_point = ((0, 0), WEST)
energized_tiles = track_light(start_point)
num_energized = len(energized_tiles)

print(f"ANSWER: {num_energized}")
