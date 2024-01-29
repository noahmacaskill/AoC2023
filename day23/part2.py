from typing import Dict, List

INPUT = "input"

with open(INPUT, "r") as f:
    map = f.readlines()

NUM_ROWS, NUM_COLS = len(map), len(map[0])-1

def valid_point(x: int, y: int, visited: List[List[bool]]) -> bool:
    """
    Performs validity checks for a point as follows:
        - Point is within the bounds of the map
        - Point has not yet been visited
        - Point is on a trail

    Parameters:
    x (int): x coord
    y (int): y coord
    visited (List[List[bool]]): Grid containing which tiles have been visited

    Returns:
    bool: Point validity    
    """
    return 0 <= x < NUM_ROWS and 0 <= y < NUM_COLS and not visited[x][y] and map[x][y] != '#'

def neighbours(x: int, y: int, visited: List[List[bool]]) -> List[tuple[int, int]]:
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
    for dx, dy in zip([-1, 0, 1, 0], [0, 1, 0, -1]):
        pt = (x+dx, y+dy)
        if valid_point(*pt, visited):
            neighbours.append(pt)

    return neighbours

def find_node_connections(start: tuple[int, int]) -> Dict[tuple[int, int], List[tuple[tuple[int, int], int]]]:
    """
    Find Connections between all nodes to their neighbouring nodes
    A node is a tile for which there are multiple branch offs (i.e. multiple valid neighbouring tiles)

    Parameters:
    start (tuple[int,int]): Start point

    Returns:
    Dict[tuple[int, int], List[tuple[tuple[int, int], int]]]: Mapping from node to connected nodes, incl. distance between them
        key (tuple[int, int]): Start node
        value (List[tuple[tuple[int, int], int]]):
            tuple[int, int]: End node
            int: Distance between start and end node
    """
    def find_connections(x: int, y: int) -> List[tuple[tuple[int, int], int]]:
        nonlocal connection_pts
        
        connections = []
        visited = [[False] * NUM_COLS for _ in range(NUM_ROWS)]
        visited[x][y] = True
        for path in neighbours(x, y, visited):
            distance = 1
            visited[path[0]][path[1]] = True
            curr_pt = path            
            while len(next_pts := neighbours(*curr_pt, visited)) == 1:
                curr_pt = next_pts[0]
                visited[curr_pt[0]][curr_pt[1]] = True
                distance += 1

            connections.append((curr_pt, distance))
            if curr_pt not in node_connections and curr_pt not in connection_pts:
                connection_pts.append(curr_pt)
        
        return connections

    node_connections = {}
    connection_pts = [start]
    while connection_pts:
        conn_pt = connection_pts.pop()
        node_connections[conn_pt] = find_connections(*conn_pt)

    return node_connections

def find_longest_path(start: tuple[int, int], end: tuple[int, int], node_connections: Dict[tuple[int, int], List[tuple[tuple[int, int], int]]]) -> int:
    """
    Identifies the longest valid path from a start position to an end position without repetition

    Method performs a DFS of possible paths, jumping from node point to node point

    Parameters:
    start (tuple[int, int]): coords of start point
    end (tuple[int, int]): coords of end point
    node_connections (Dict[tuple[int, int], List[tuple[tuple[int, int], int]]]): Mapping from node to connected nodes, incl. distance between them
        key (tuple[int, int]): Start node
        value (List[tuple[tuple[int, int], int]]):
            tuple[int, int]: End node
            int: Distance between start and end node

    Returns:
    int: Longest path
    """
    stack = [(None, start, 0)]
    visited_nodes = [start]
    max_path_len = 0

    while stack:
        last_node, node, path_len = stack.pop()

        if node == end:
            max_path_len = max(path_len, max_path_len)
            continue

        if node != visited_nodes[-1]:
            head_node = visited_nodes.pop()
            while last_node != head_node:
                head_node = visited_nodes.pop()
            
            visited_nodes.append(head_node)
            visited_nodes.append(node)

        for next_node, length in node_connections[node]:
            if next_node not in visited_nodes:
                stack.append((node, next_node, path_len+length))
        
        visited_nodes.append(next_node)

    return max_path_len

# Identify start point
for ind, tile in enumerate(map[0]):
    if tile == '.':
        start = (0, ind)

# Identify end point
for ind, tile in enumerate(map[-1]):
    if tile == '.':
        end = (NUM_ROWS-1, ind)

node_connections = find_node_connections(start)
longest_path = find_longest_path(start, end, node_connections)

print(f"ANSWER: {longest_path}")
