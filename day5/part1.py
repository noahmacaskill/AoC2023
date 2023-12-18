from typing import List

with open("input", "r") as f:
    almanac = f.readlines()

def decode_map(cat_map: List[str]) -> List[tuple[int, int, int]]:
    """
    Decodes mapping data from one category to another into tuples

    Parameters:
    - cat_map (List[str]): List of the raw mapping data from the almanac

    Returns:
    List[tuple[int, int, int]]: 
        1. range_start: Start of the source range (inclusive)
        2. range_end: End of the source range (exclusive)
        3. jump: Jump required to determine destination number for numbers found in source range
    """
    mappings = []

    for line in cat_map:
        mapping = line.split()
        range_start = int(mapping[1])
        range_end = range_start + int(mapping[2])
        jump = int(mapping[0]) - range_start

        mappings.append((range_start, range_end, jump))
    
    return mappings

def mapping(source_num: int, cat_map: List[tuple[int, int, int]]) -> int:
    """
    Maps a source number to its destination number

    Parameters:
    - source_num (int): The source number
    - cat_map (List[tuple[int, int, int]]): 
        1. range_start: Start of the source range (inclusive)
        2. range_end: End of the source range (exclusive)
        3. jump: Jump required to determine destination number for numbers found in source range
    
    Returns:
    int: Destination number
    """
    for mapping in cat_map:
        if mapping[0] <= source_num < mapping[1]:
            return source_num + mapping[2]
    
    return source_num

split_indices = [i for i in range(len(almanac)) if almanac[i] == '\n']

cat_maps = []
start_index = 0
for split_index in split_indices:
    cat_maps.append(almanac[start_index:split_index])
    start_index = split_index + 1

cat_maps.append(almanac[start_index:])

category_numbers = [int(x) for x in almanac[0].split(':')[1].split()]

for cat_map in cat_maps[1:]:
    decoded_map = decode_map(cat_map[1:])

    lambda_mapping = lambda source_num: mapping(source_num, decoded_map)
    category_numbers = list(map(lambda_mapping, category_numbers))

print(f"ANSWER: {min(category_numbers)}")

