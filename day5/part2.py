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

def mapping(source_range: tuple[int, int], cat_map: List[tuple[int, int, int]]) -> List[tuple[int, int]]:
    """
    Maps a source number range to a list of destination number ranges

    Parameters:
    - source_range tuple[int, int]: The source category number range (meaning all numbers in the range are being mapped)
    - cat_map (List[tuple[int, int, int]]): 
        1. range_start: Start of the source range to map (inclusive)
        2. range_end: End of the source range to map (exclusive)
        3. jump: Jump required to determine destination number for numbers found in source range
    
    Returns:
    List[tuple[int, int]]: List of destination ranges source range has been mapped to
    """
    source_ranges = [source_range]
    dest_ranges = []
    next_source_ranges = []

    for mapping in cat_map:
        for sr in source_ranges:
            if sr[0] < mapping[0]:
                if sr[1] > mapping[1]: # Case 1: Mapping range is found entirely within source range
                    next_source_ranges.append((sr[0], mapping[0]))
                    dest_ranges.append((mapping[0]+mapping[2], mapping[1]+mapping[2]))
                    next_source_ranges.append((mapping[1], sr[1]))
                    continue
                elif mapping[0] < sr[1] <= mapping[1]: # Case 2: Upper subsection of source range overlaps with mapping range
                    next_source_ranges.append((sr[0], mapping[0]))
                    dest_ranges.append((mapping[0]+mapping[2], sr[1]+mapping[2]))
                    continue
            elif sr[0] >= mapping[0]:
                if sr[1] <= mapping[1]: # Case 3: Source range is found entirely within mapping range
                    dest_ranges.append((sr[0]+mapping[2], sr[1]+mapping[2]))
                    continue
                elif sr[0] < mapping[1] < sr[1]: # Case 4: Lower subsection of source range overlaps with mapping range
                    dest_ranges.append((sr[0]+mapping[2], mapping[1]+mapping[2]))
                    next_source_ranges.append((mapping[1], sr[1]))
                    continue
            
            next_source_ranges.append(sr)
        
        source_ranges = next_source_ranges
        next_source_ranges = []
    
    return dest_ranges + source_ranges

split_indices = [i for i in range(len(almanac)) if almanac[i] == '\n']

cat_maps = []
start_index = 0
for split_index in split_indices:
    cat_maps.append(almanac[start_index:split_index])
    start_index = split_index + 1

cat_maps.append(almanac[start_index:])

seed_data = [int(x) for x in almanac[0].split(':')[1].split()]
category_ranges = [(seed_data[i], seed_data[i]+seed_data[i+1]) for i in range(0, len(seed_data), 2)]

for cat_map in cat_maps[1:]:
    decoded_map = decode_map(cat_map[1:])

    lambda_mapping = lambda source_range: mapping(source_range, decoded_map)
    category_ranges = [rng for dst_ranges in list(map(lambda_mapping, category_ranges)) for rng in dst_ranges]

print(f"ANSWER: {min([cat_range[0] for cat_range in category_ranges])}")

