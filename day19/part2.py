import math
from typing import List

INPUT = "input"
MAX_RATING = 4000

ranges_tuple = tuple[List[tuple[int, int]], List[tuple[int, int]], List[tuple[int, int]], List[tuple[int, int]]]

xmas_to_index = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3
}

def parse_workflow(workflow_text: str) -> List[tuple[int, tuple[int, int], str]]:
    """
    Parses a workflow into:
    
    List[tuple[int, tuple[int, int], str]]: List representing rules in the workflow
        int: index of rating
        tuple[int, int]: Range of values for rating in which rule is true
        str: Part destination if rule is true
    """
    workflow = []
    rules = workflow_text.split(',')
    
    for rule in rules[:-1]:
        cond, res = rule.split(':')

        ind = xmas_to_index[cond[0]]
        comparator = int(cond[2:])

        if cond[1] == '<':
            rng = (1, comparator)
            workflow.append((ind, rng, res))
        else: # >
            rng = (comparator+1, MAX_RATING+1)
            workflow.append((ind, rng, res))

    workflow.append((0, (1, MAX_RATING+1), rules[-1]))
    return workflow

def num_possibilities(ranges: ranges_tuple) -> int:
    """
    Calculate number of possible arrangements of a range of possible ratings

    Parameters:
    ranges (ranges_tuple): Tuple containg four lists of ranges (range = (start_index, end_index))
        representing X, M, A and S ratings

    Returns:
    int: Number of possible ranges
    """
    return math.prod([sum([rng[1]-rng[0] for rng in rating_rngs]) for rating_rngs in ranges])

def get_ranges(ranges: List[tuple[int, int]], true_range_start: int, true_range_end: int) -> tuple[List[tuple[int, int]], List[tuple[int, int]]]:
    """
    Calculates the parts of a range that fall within a "true range" and the parts that fall outside it
    True range is a range that applies to a given rule (e.g. a<2000: (1, 2000))

    Parameters:
    ranges (List[tuple[int, int]]): List of ranges applying to ratings for the category that applies to the rule
    true_range_start (int): Start of the true range for the rule
    true_range_end (int): End of the true range for the rule
    
    Returns:
    tuple[List[tuple[int, int]], List[tuple[int, int]]]: (True range overlap, False range)
    """
    
    true_ranges, false_ranges = [], []
    for rng in ranges:
        start, end = rng
        
        if end <= true_range_start or true_range_end <= start:
            false_ranges.append(rng)

        overlap_start = max(true_range_start, start)
        overlap_end = min(true_range_end, end)
        true_ranges.append((overlap_start, overlap_end))

        if start < overlap_start:
            false_ranges.append((start, overlap_start))
        elif end > overlap_end:
            false_ranges.append((overlap_end, end))

    return true_ranges, false_ranges

workflows = {}

with open(INPUT, "r") as f:
    for line in f:
        line = line.strip()

        if not line:
            break
        
        name, wf = line.split('{', 1)
        workflows[name] = parse_workflow(wf[:-1])

possibilities = 0
paths = [('in', tuple([[(1, MAX_RATING+1)]])*4)]

while paths:
    wf, ranges = paths.pop()

    if wf in 'AR':
        if wf == 'A':
            possibilities += num_possibilities(ranges)
        
        continue
    
    wf = workflows[wf]
    for rule in wf:
        ind, rng, res = rule
        true_ranges, false_ranges = get_ranges(ranges[ind], *rng)

        true_ranges = tuple(true_ranges if i == ind else rng for i, rng in enumerate(ranges))
        ranges = tuple(false_ranges if i == ind else rng for i, rng in enumerate(ranges))

        if true_ranges != [[], [], [], []]:
            paths.append((res, true_ranges))
        if ranges == [[], [], [], []]:
            break

print(f"ANSWER: {possibilities}")
