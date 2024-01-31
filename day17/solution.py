from typing import List
import heapq

INPUT ="input"

with open(INPUT, "r") as f:
    map = f.readlines()

PART1 = False

DEST_ROW = len(map)-1
DEST_COL = len(map[0][:-1])-1

NORTH = 0
EAST = 1
SOUTH = 2
WEST = 3

if PART1:
    MIN_BLOCKS_STRAIGHT = 0
    MAX_BLOCKS_STRAIGHT = 3
else:
    MIN_BLOCKS_STRAIGHT = 4
    MAX_BLOCKS_STRAIGHT = 10

def neighbours(pt: tuple[int, int]) -> List[tuple[tuple[int, int], int]]:
    """
    Return neighbouring points of a given point if they are in bounds

    Parameters:
    pt (tuple[int, int]): (row, col) of point

    Returns:
    List[tuple[tuple[int, int], int]]: List of neighbouring points
        tuple[int, int]: (row, col) of neighbouring point
        int: Direction moving into neighbouring point
    """
    row, col = pt
    new_pts = [((row-1, col), NORTH), ((row, col+1), EAST), ((row+1, col), SOUTH), ((row, col-1), WEST)]
    return [((row, col), dir) for (row, col), dir in new_pts if 0 <= row <= DEST_ROW and 0 <= col <= DEST_COL]

"""
Solution: Dijkstra's algo with restrictions (MIN_BLOCKS_STRAIGHT and MAX_BLOCKS_STRAIGHT)

This requires not only keeping track of the shortest path to each node, but the shortest path to each node in a given state.
State in this context is the current direction moving into that node and the number of successive nodes it has been travelling in that direction

state (tuple[tuple[int, int], tuple[int, int]]):
    (0) tuple[int, int]: (row, col) of node
    (1) tuple[int, int]: (direction, successive nodes travelled in that direction)
"""

heat_losses = {}
priority_queue = [(((0, 0), (SOUTH, 0)), 0)]

while priority_queue:
    current_state, current_heat_loss = heapq.heappop(priority_queue)
    block, (current_dir, current_same_dir_blocks) = current_state

    if (stored_heat_loss := heat_losses.get(current_state, None)) is not None and current_heat_loss > stored_heat_loss:
        continue
    
    for neighbour, dir in neighbours(block):
        if (dir-2)%4 == current_dir or (current_same_dir_blocks < MIN_BLOCKS_STRAIGHT and dir != current_dir) or (current_same_dir_blocks == MAX_BLOCKS_STRAIGHT and dir == current_dir):
            continue

        neighbour_heat_loss = int(map[neighbour[0]][neighbour[1]])
        heat_loss = current_heat_loss + neighbour_heat_loss

        if dir == current_dir:
            same_dir_blocks = current_same_dir_blocks+1
        else:
            same_dir_blocks = 1

        next_state = (neighbour, (dir, same_dir_blocks))

        if (stored_heat_loss := heat_losses.get(next_state, None)) is None or heat_loss < stored_heat_loss:
            heat_losses[next_state] = heat_loss
            heapq.heappush(priority_queue, (next_state, heat_loss))    

min_heat_loss = min([hl for state, hl in heat_losses.items() if state[0] == (DEST_ROW, DEST_COL)])
print(f"ANSWER: {min_heat_loss}")