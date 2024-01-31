from typing import List

INPUT = "input"

with open(INPUT, "r") as f:
    report = f.readlines()

history = []
for line in report:
    line = line[:-1].split()
    history.append([int(val) for val in line])

def calculate_difference(values: List[int]) -> List[int]:
    """
    Calculates the differences between successive elements in a list

    Parameters:
    values (List[int]): List of integers

    Returns:
    List[int]: List of integers representing the differences
    """
    differences = []
    for ind, val in enumerate(values[:-1]):
        difference = values[ind+1] - val
        differences.append(difference)
    
    return differences

def extrapolate_value(values: List[int]) -> int:
    """
    Extrapolates the next value in a list

    Parameters:
    values (List[int]): List of integers

    Returns:
    int: The extrapolated next value in the sequence
    """
    differences = []
    while not all(elm == 0 for elm in values):
        differences.append(values[-1])
        values = calculate_difference(values)

    differences.append(0)
    while len(differences) > 1:
        difference = differences.pop()
        final_element = differences.pop()
        extrapolated_element = final_element + difference
        differences.append(extrapolated_element)
    
    return extrapolated_element

extrapolated_sum = 0
for line in history:
    extrapolated_sum += extrapolate_value(line)

print(f"ANSWER: {extrapolated_sum}")
