with open("input", "r") as f:
    spring_records = f.readlines()

cached_combinations = {}

def num_combinations(unknown_springs: str, damaged_springs: tuple[int]) -> int:
    """
    Determines the number of combinations of damaged/functioning springs

    Parameters:
    unknown_groupings (str): The arrangement of springs containing unknowns (?s)
    damaged_groupings (tuple[int]): Tuple representing groups of successive damaged springs

    Returns:
    int: Number of possible combinations of damaged/functioning springs
    """
    if not damaged_springs:
        return '#' not in unknown_springs
    
    if (unknown_springs,) + damaged_springs in cached_combinations:
        return cached_combinations[(unknown_springs,) + damaged_springs]

    combinations = 0
    spring, next_springs = damaged_springs[0], damaged_springs[1:]

    for i in range(len(unknown_springs) - sum(damaged_springs) - len(damaged_springs) + 2):
        if '#' in unknown_springs[:i]:
            break
        if '.' not in unknown_springs[i:i+spring] and unknown_springs[i+spring] != '#':
            combinations += num_combinations(unknown_springs[i+spring+1:], next_springs)

    cached_combinations[(unknown_springs,) + damaged_springs] = combinations
    return combinations

total_combinations = 0
for record in spring_records:
    unknowns, damaged = record.split()
    damaged = tuple(int(dam) for dam in damaged.split(','))
    cached_combinations = {}
    total_combinations += num_combinations('?'.join([unknowns]*5) + '.', (damaged*5))

print(f'ANSWER: {total_combinations}')
