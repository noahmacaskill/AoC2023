with open("input", "r") as f:
    dig_plan = f.readlines()

# Translate numeric direction to more readable alphabet character
get_dir = {
    '0': 'R',
    '1': 'D',
    '2': 'L',
    '3': 'U'
}

"""
Solution: Can't use ray casting algorithm here, far too slow with a polygon this massive. Shoelace algorithm is used instead which runs in linear time
relative to the number of digs (corners of the polygon). Since we aren't initially given vertices of the polygon, but instead the blocks inside the shape that make
up its edge, we can't be sure of which corner of each block represents the vertice required for shoelace (it is dependant if we are turning L/R and if we're
traversing the polygon in a CW or CCW fashion).

We first do the shoelace algorithm using the coordinates of each block, which tells us if we have traversed the polygon CW (negative shoelace value) or CCW (positive
shoelace value). As we do so, we keep track of what the vertice at each block would be if we were traversing in each of a CW/CCW fashion. Lastly, we calculate the area
by running the shoelace algo once again, this time on the corresponding vertices
"""

def get_vertices(pt: tuple[int, int], turn: str) -> tuple[tuple[int, int], tuple[int, int]]:
    """
    Gets the vertice of a block in both CW/CCW given the turn taken at this block (e.g. RD = Right -> Down)
    There are eight types of turns, but turns out the vertices are the same for opposite turns (e.g. RD vertices == DR vertices)
    Thus the input is filtered before passing to the function to ensure R/L comes before U/D
    
    Parameters:
    pt tuple[int, int]: Corner point in the polygon
    turn (str): The turn occuring at this corner (i.e. RD)

    Returns:
    tuple[tuple[int, int], tuple[int, int]]: The potential vertices in (CW, CCW) order
    """
    if turn == 'RD':
        return ((pt[0], pt[1]+1), (pt[0]+1, pt[1]))
    elif turn == 'RU':
        return (pt, (pt[0]+1, pt[1]+1))
    elif turn == 'LD':
        return ((pt[0]+1, pt[1]+1), pt)
    else: # LU
        return ((pt[0]+1, pt[1]), (pt[0], pt[1]+1))

def get_point(pt: tuple[int, int], dir: str, length: int) -> tuple[int, int]:
    """
    Gets the next corner block

    Parameters:
    pt (tuple[int, int]): Corner point in the polygon
    dir (str): Direction to travel (U, D, L, R)
    length (int): Length of dig to next corner block

    Returns:
    tuple[int, int]: Next corner block
    """
    if dir == 'U':
        return (pt[0]-length, pt[1])
    elif dir == 'R':
        return (pt[0], pt[1]+length)
    if dir == 'D':
        return (pt[0]+length, pt[1])
    if dir == 'L':
        return (pt[0], pt[1]-length)

# Shoelace formula calculation
shoelace = lambda x1, y1, x2, y2: (x1*y2 - x2*y1)/2

num_vertices = len(dig_plan)
dig = dig_plan[0].split()[2]
dir = get_dir[dig[-2]]
length = int(dig[2:-2], 16)
point, next_point = get_point((0, 0), dir, length), None
shoelace_total = 0
vertices = []
for i in range(1, num_vertices+1):
    next_dig = dig_plan[i%num_vertices].split()[2]
    next_dir, next_length = get_dir[next_dig[-2]], int(next_dig[2:-2], 16)
    next_point = get_point(point, next_dir, next_length)

    shoelace_total += shoelace(*point, *next_point)
    vertices.append(get_vertices(point, ''.join(c for c in 'RLDU' if c in dir+next_dir)))

    point, dir = next_point, next_dir

if shoelace_total < 0: # Traversed CW
    vert_index = 0
else: # Travered CCW
    vert_index = 1

area = 0
for i in range(num_vertices):
    area += shoelace(*vertices[i][vert_index], *vertices[(i+1)%num_vertices][vert_index])

print(f"ANSWER: {abs(area)}")