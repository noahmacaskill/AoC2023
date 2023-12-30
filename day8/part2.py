from typing import List
import math

with open("input", "r") as f:
    directions = f.readlines()

dir_to_ind = {
    'L': 0,
    'R': 1
}
    
lr = directions[0][:-1]
nodes = directions[2:]

network = {}
for node in nodes:
    filtered_node = ''.join(c for c in node if c.isalpha() or c.isdigit() or c.isspace())
    src, l, r = filtered_node.split()

    network[src] = (l, r)

def filter_last_letter(nodes: List[str], letter: str) -> List[str]:
    """
    Filters a list of nodes for those ending in a specific letter

    Parameters:
    nodes (List[str]): List of nodes
    letter (str): Filtering letter

    Returns:
    List[str]: List containing the nodes ending in the specified letter
    """
    filtered_nodes = []
    for node in nodes:
        if node[-1] == letter:
            filtered_nodes.append(node)
    
    return filtered_nodes

index = 0
steps = 0
nodes = filter_last_letter(list(network.keys()), 'A')
cycle_lengths = []

while len(nodes) > 0:
    dir = dir_to_ind[lr[index]]
    nodes = list(map(lambda x: network[x][dir], nodes))
    
    index += 1
    steps += 1

    finished_cycle_nodes = []
    for ind, node in enumerate(nodes):
        if node[-1] == 'Z':
            cycle_lengths.append(steps)
            finished_cycle_nodes.append(node)

    nodes = [node for node in nodes if node not in finished_cycle_nodes]

    if index == len(lr):
        index = 0

print(f"ANSWER: {math.lcm(*cycle_lengths)}")
