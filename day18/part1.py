with open("input", "r") as f:
    dig_plan = f.readlines()

dig_directions = {
    'U': (-1, 0),
    'R': (0, 1),
    'D': (1, 0),
    'L': (0, -1)
}

"""
Solution: Ray casting algorithm. Allow ray to pass horizontally from a point, if it crosses the edge of the polygon an odd amount of times, it is inside the polygon,
else it is outside.
"""

edge = {}
point = (0, 0)

# First trace the path of the polygon
for line in dig_plan:
    dig = line.split()
    dir, length, color = dig[0], int(dig[1]), dig[2][1:8]
    mv_point = dig_directions[dir]

    if dir in 'UD':
        edge[point] = dir

    for i in range(length):
        point = (point[0] + mv_point[0], point[1] + mv_point[1])
        edge[point] = dir

min_x = min(pt[0] for pt in edge)
max_x = max(pt[0] for pt in edge)
min_y = min(pt[1] for pt in edge)
max_y = max(pt[1] for pt in edge)

# Ray casting algo to calculate the area
area = len(edge)
for x in range(min_x, max_x+1):
    group_size = 0
    inner_pt = False
    edge_dir = None
    for y in range(min_y, max_y+1):
        if (x, y) in edge:
            if edge[(x, y)] not in 'UD':
                continue

            if inner_pt:
                area += group_size
            
            if edge_dir == None:
                edge_dir = edge[(x, y)]
                inner_pt = not inner_pt
            else:
                if edge_dir != edge[(x, y)]:
                    inner_pt = not inner_pt
                edge_dir = None
            
            group_size = 0
            continue

        group_size += 1
        edge_dir = None

print(f"ANSWER: {area}")