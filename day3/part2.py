INPUT = "input"

with open(INPUT, "r") as f:
    schematic = f.readlines()
    max_row, max_col = len(schematic), len(schematic[0])-1

def find_number(row: int, col: int) -> tuple[int, int, int]:
    """
    Given a location in the schematic where a digit is found, identify the start and end index of the whole number

    Parameters:
    - row (int): Row where the digit is found
    - col (int): Column where the digit is found

    Returns: The line (row), start and end indices (inclusive) where the number is found
    """
    start_index = col
    while str.isdigit(schematic[row][start_index-1]) and start_index>0:
        start_index -=1
    
    end_index = col
    while str.isdigit(schematic[row][end_index+1]) and end_index<max_col-1:
        end_index += 1

    return (row, start_index, end_index)

def gear_ratio(gear: int, line: int) -> int:
    """
    Calculates the gear ratio of a given gear

    Parameters:
    - gear (int): Index of the gear in the line
    - line (int): Line number

    Returns:
    int: The gear ratio, or zero if the given gear is not a true gear (i.e., not adjacent to two part numbers)
    """

    adj_part_numbers = set()

    for row in range(line-1 if line>0 else 0, line+2 if line+1<max_row else max_row):
        for col in range(gear-1 if gear>0 else 0, gear+2 if gear+1<max_col else max_col):
            if str.isdigit(schematic[row][col]):
                adj_part_numbers.add(find_number(row, col))
    
    if len(adj_part_numbers) == 2:
        adj_part_numbers = list(adj_part_numbers)
        part_num_1 = int(schematic[adj_part_numbers[0][0]][adj_part_numbers[0][1]:adj_part_numbers[0][2]+1])
        part_num_2 = int(schematic[adj_part_numbers[1][0]][adj_part_numbers[1][1]:adj_part_numbers[1][2]+1])
        return part_num_1*part_num_2
    else:
        return 0

tot_gear_ratio = 0

for index, line in enumerate(schematic):
    gear_indices = [ind for ind in range(len(line)) if line[ind] == '*']

    for gear in gear_indices:
        tot_gear_ratio += gear_ratio(gear, index)

print(f"ANSWER: {tot_gear_ratio}")