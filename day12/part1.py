from typing import List

INPUT = "input"

with open(INPUT, "r") as f:
    spring_records = f.readlines()

def num_combinations(unknown_groupings: List[str], damaged_groupings: List[int]) -> int:
    """
    Determines the number of combinations of damaged/functioning springs

    Parameters:
    unknown_groupings (List[str]): List of strings representing the damaged condition report
        Each element is a group of successive #s or ?s, .s have been filtered out
    damaged_groupings (List[int]): List representing groups of successive damaged springs

    Returns:
    int: Number of possible combinations of damaged/functioning springs
    """
    if len(damaged_groupings) == 0:
        for ug in unknown_groupings:
            if '#' in ug:
                return 0
        return 1

    combinations = 0
    dg = damaged_groupings[0]

    while len(unknown_groupings) > 0:
        ug = unknown_groupings.pop()

        if dg <= len(ug):
            for i in range(len(ug)-dg+1):
                if i > 0 and ug[i-1] == '#':
                    return combinations
                elif i+dg < len(ug) and ug[i+dg] == '#':
                    continue

                new_combinations = num_combinations(unknown_groupings + [ug[i+dg+1:]], damaged_groupings[1:])
                combinations += new_combinations
                if ug[i] == '#' or (i == (len(ug)-dg) and '#' in ug[i:]):
                    return combinations
        elif '#' in ug:
            return combinations

    return combinations

total_combinations = 0
for record in spring_records:
    unknowns, damaged = record.split()

    unknowns = [unk for unk in unknowns.split('.') if unk.strip()]
    unknowns.reverse()
    damaged = [int(dam) for dam in damaged.split(',')]

    total_combinations += num_combinations(unknowns, damaged)

print(f'ANSWER: {total_combinations}')
