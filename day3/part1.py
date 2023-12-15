with open("input", "r") as f:
    schematic = f.readlines()
    max_row, max_col = len(schematic), len(schematic[0])-1


def is_part_number(start: int, end: int, line: int) -> bool:
    """
    Identifies whether a number is a part number

    Parameters:
    - start (int): The starting index of the number (inclusive)
    - end (int): The ending index of the number (inclusive)
    - line (int): The line number

    Returns:
    bool: Whether number is a part number
    """
    for row in range(line-1 if line>0 else 0, line+2 if line+1<max_row else max_row):
        for col in range(start-1 if start>0 else 0, end+2 if end+1<max_col else max_col):
            if schematic[row][col] not in "0123456789.":
                return True
    
    return False

part_sum = 0

for index, line in enumerate(schematic):
    # Retrieve the indices where numbers are found
    num_start_indices = [ind for ind in range(len(line)) if str.isdigit(line[ind]) and (not str.isdigit(line[ind-1]) or ind == 0)]
    num_end_indices = [ind for ind in range(len(line)) if str.isdigit(line[ind]) and (not str.isdigit(line[ind+1]) or ind == len(line)-1)]
    num_indices = list(zip(num_start_indices, num_end_indices))

    for start, end in num_indices:
        if is_part_number(start, end, index):
            part_sum += int(line[start:end+1])

print(f"ANSWER {part_sum}")

