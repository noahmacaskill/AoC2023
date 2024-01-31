from typing import List

INPUT = "input"

with open(INPUT, "r") as f:
    observations = f.readlines()

observations = [s.rstrip('\n') for s in observations]
observations.append([])

def row_differences(matrix: List[str], ind1: int, ind2: int) -> List[int]:
    num_differences = 0
    
    for i in range(len(matrix[0])):
        if matrix[ind1][i] != matrix[ind2][i]:
            num_differences += 1

    return num_differences

def col_differences(matrix: List[str], ind1: int, ind2: int) -> int:
    num_differences = 0
    for i in range(len(matrix)):
        if matrix[i][ind1] != matrix[i][ind2]:
            num_differences += 1

    return num_differences

def check_smudge(matrix: List[str], ind: int, row: bool) -> bool:
    """
    Checks a matrix for an axis of reflection with a smudge

    Parameters:
    matrix (List[str]): 2D matrix representing mirror data
    ind (int): Index of relection (index of column to the left or row above reflection)
    row (bool): True for checking rows, false for cols

    Returns:
    bool: True if reflection found with smudge
    """
    if row:
        max = len(matrix)
    else:
        max = len(matrix[0])

    num_differences = 0
    for i, j in zip(range(ind, -1, -1), range(ind+1, max)):
        if row:
            num_differences += row_differences(matrix, i, j)
        else:
            num_differences += col_differences(matrix, i, j)
        
        if num_differences > 1:
            return False
        
    return num_differences == 1

def find_reflection(matrix: List[str]) -> int:
    """
    Finds the reflection (with smudge) in a grid of mirror observation data

    Parameters:
    matrix (List[str]): 2D matrix representing mirror data

    Returns:
    int: Number of columns to the left of vertical reflection, or rows*100 above horizontal reflection
    """
    for i in range(len(matrix)-1):
        if check_smudge(matrix, i, True):
            return 100*(i+1)
    
    for i in range(len(matrix[0])-1):
        if check_smudge(matrix, i, False):
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
