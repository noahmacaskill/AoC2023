from typing import List

INPUT = "input"

with open(INPUT, "r") as f:
    map = f.readlines()

NUM_ROWS, NUM_COLS = len(map), len(map[0])-1

def valid_point(x: int, y: int, visited: List[List[bool]], slope: str) -> bool:
    """
    Performs validity checks for a point as follows:
        - Point is within the bounds of the map
        - Point has not yet been visited
        - Point is on a flat trail or a downward slope

    Parameters:
    x (int): x coord
    y (int): y coord
    visited (List[List[bool]]): Grid containing which tiles have been visited
    slope (str): Slope required to make the point valid (^, >, v or <)

    Returns:
    bool: Point validity    
    """
    return 0 <= x < NUM_ROWS and 0 <= y < NUM_COLS and not visited[x][y] and map[x][y] in '.'+slope

def neighbours(x, y, visited) -> List[tuple[int, int]]:
    """
    Generates valid neighbouring points of a given point

    Parameters:
    x (int): x coord
    y (int): y coord
    visited (List[List[bool]]): Grid containing which tiles have been visited

    Returns:
    List[tuple[int,  int]]: List of valid neighbours
    """
    neighbours = []
    for (dx, dy), slope in zip(zip([-1, 0, 1, 0], [0, 1, 0, -1]), ['^', '>', 'v', '<']):
        pt = (x+dx, y+dy)
        if valid_point(*pt, visited, slope):
            neighbours.append(pt)

    return neighbours

def find_longest_path(start: tuple[int, int], end: tuple[int, int]) -> int:
    """
    Identifies the longest valid path from a start position to an end position without repetition

    Method performs a DFS of possible paths

    Parameters:
    start (tuple[int, int]): coords of start point
    end (tuple[int, int]): coords of end point

    Returns:
    int: Longest path
    """
    stack = [(start, 0)]
    visited = [[False] * NUM_COLS for _ in range(NUM_ROWS)]
    current_path = [start]
    max_path_len = 0

    while stack:
        (x, y), path_len = stack.pop()

        if (x, y) == end:
            max_path_len = max(path_len, max_path_len)
            continue

        if (x, y) != current_path[-1]:
            path_head_x, path_head_y = current_path.pop()
            while (x, y) != (path_head_x, path_head_y):
                visited[path_head_x][path_head_y] = False
                path_head_x, path_head_y = current_path.pop()
            
            current_path.append((x, y))

        visited[x][y] = True

        for next_pt in neighbours(x, y, visited):
            current_path.append(next_pt)
            stack.append((next_pt, path_len+1))
    
    return max_path_len

# Identify start point
for ind, tile in enumerate(map[0]):
    if tile == '.':
        start = (0, ind)

# Identify end point
for ind, tile in enumerate(map[-1]):
    if tile == '.':
        end = (NUM_ROWS-1, ind)

longest_path = find_longest_path(start, end)

print(f"ANSWER: {longest_path}")
