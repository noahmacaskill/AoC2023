with open("input", "r") as f:
    observations = f.readlines()

EXPANSION_MAGNITUDE = 1000000 # 2 for part 1

galaxy_rows = []
galaxy_cols = []
for row, line in enumerate(observations):
    for col, obs in enumerate(line):
        if obs == '#':
            galaxy_rows.append(row)
            galaxy_cols.append(col)
galaxies = list(zip(galaxy_rows, galaxy_cols))

expanded_rows = []
for i in range(len(observations)):
    if i not in galaxy_rows:
        expanded_rows.append(i)

expanded_cols = []
for i in range(len(observations[-1])):
    if i not in galaxy_cols:
        expanded_cols.append(i)

def galaxy_distance(gal1: tuple[int, int], gal2: tuple[int, int], expansion_magnitude: int) -> int:
    """
    Calculates and returns the distance between two  galaxies

    Parameters:
    gal1 (tuple[int, int]): x, y coordinates of first galaxy
    gal2 (tuple[int, int]): x, y coordinates of second galaxy
    expansion_magnitude (int): The size of expansion for empty rows/cols
    
    Returns:
    int: Distance between the galaxies, including universe expansion
    """
    min_row = min(gal1[0], gal2[0])
    min_col = min(gal1[1], gal2[1])
    row_dist = abs(gal1[0] - gal2[0])
    col_dist = abs(gal1[1] - gal2[1])

    expanded_dist = 0
    for row in expanded_rows:
        if 0 < (row - min_row) < row_dist:
            expanded_dist += (expansion_magnitude-1)

    for col in expanded_cols:
        if 0 < (col - min_col) < col_dist:
            expanded_dist += (expansion_magnitude-1)
    
    return row_dist + col_dist + expanded_dist

total_distance = 0
for i in range(len(galaxies)):
    for j in range(i, len(galaxies)):
        total_distance += galaxy_distance(galaxies[i], galaxies[j], EXPANSION_MAGNITUDE)

print(f"ANSWER: {total_distance}")
