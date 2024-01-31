from typing import List

INPUT = "input"

with open(INPUT, "r") as f:
    observations = f.readlines()

observations = [s.rstrip('\n') for s in observations]
observations.append([])

def equal_rows(matrix: List[str], ind1: int, ind2: int) -> bool:
    return matrix[ind1] == matrix[ind2]

def equal_cols(matrix: List[str], ind1: int, ind2: int) -> bool:
    return all(matrix[row_ind][ind1] == matrix[row_ind][ind2] for row_ind in range(len(matrix)))

def check_reflection(matrix: List[str], ind: int, row: bool) -> bool:
    """
    Checks a matrix for an axis of reflection

    Parameters:
    matrix (List[str]): 2D matrix representing mirror data
    ind (int): Index of relection (index of column to the left or row above reflection)
    row (bool): True for checking rows, false for cols

    Returns:
    bool: True if reflection found
    """
    if row:
        max = len(matrix)
    else:
        max = len(matrix[0])

    for i, j in zip(range(ind, -1, -1), range(ind+1, max)):
        if row and equal_rows(matrix, i, j):
            continue
        elif (not row) and equal_cols(matrix, i, j):
            continue

        return False
    
    return True

def find_reflection(matrix: List[str]) -> int:
    """
    Finds the reflection in a grid of mirror observation data

    Parameters:
    matrix (List[str]): 2D matrix representing mirror data

    Returns:
    int: Number of columns to the left of vertical reflection, or rows*100 above horizontal reflection
    """
    for i in range(len(matrix)-1):
        if check_reflection(matrix, i, True):
            return 100*(i+1)
    
    for i in range(len(matrix[0])-1):
        if check_reflection(matrix, i, False):
            return i+1


grid = []
summarization = 0
for line in observations:
    if not line:
        summarization += find_reflection(grid)
        grid = []
        continue

    grid.append(line)

print(f"ANSWER: {summarization}")
