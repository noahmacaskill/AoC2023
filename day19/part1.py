from typing import List, Callable

INPUT = "input"

xmas_to_index = {
    'x': 0,
    'm': 1,
    'a': 2,
    's': 3
}

def parse_part(part: str) -> tuple[int, int, int, int]:
    """
    Parses a part into (X, M, A, S) ratings
    """
    x, m, a, s = part.split(',')
    return (int(x[2:]), int(m[2:]), int(a[2:]), int(s[2:]))

def parse_workflow(workflow_text: str) -> List[tuple[Callable[[tuple[int, int, int, int]], bool], str]]:
    """
    Parses a workflow into:
    
    List[tuple[Callable[[tuple[int, int, int, int]], bool], str]]: List of (Callable, str) representing rules in the workflow
        Callable: Lambda function representing a rule
            in: part
            out: bool (T/F)
        str: Part destination if rule is true
    """
    workflow = []
    rules = workflow_text.split(',')

    for rule in rules[:-1]:
        func, res = rule.split(':')
        
        ind = xmas_to_index[func[0]]
        comparator = int(func[2:])
        if func[1] == '<':
            workflow.append((lambda prt, ind=ind, comparator=comparator: prt[ind] < comparator, res))
        else:
            workflow.append((lambda prt, ind=ind, comparator=comparator: prt[ind] > comparator, res))

    workflow.append((lambda _: True, rules[-1]))
    return workflow

def process_part(part: tuple[int, int, int, int], workflow: List[tuple[Callable[[tuple[int, int, int, int]], bool], str]]) -> str:
    """
    Processes a part
    * Last function in a workflow defaults to true *

    part (tuple[int, int, int, int]): XMAS ratings of a part
    workflow (List[tuple[Callable[[tuple[int, int, int, int]], bool], str]]): List of (Callable, str) in workflow
        Callable: Lambda function representing a rule
            in: part
            out: bool (T/F)
        str: Part destination if rule is true

    Returns:
    str: Part destination
    """
    for func, out in workflow:
        if func(part):
            return out

workflows = {}
parts = []

with open(INPUT, "r") as f:
    part1 = True
    for line in f:
        line = line.strip()

        if not line:
            part1 = False
            continue
        
        if part1:
            name, wf = line.split('{', 1)
            workflows[name] = parse_workflow(wf[:-1])
        else:
            parts.append(parse_part(line[1:-1]))

part_sum = 0
for part in parts:
    wf = workflows['in']
    while (res := process_part(part, wf)) not in 'AR':
        wf = workflows[res]
    
    if res == 'A':
        part_sum += sum(part)

print(f"ANSWER: {part_sum}")
