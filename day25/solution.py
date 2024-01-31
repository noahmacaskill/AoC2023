from typing import Dict, List
import random

INPUT = "input"

connections = {}
with open(INPUT) as f:
    for line in f:
        line = line.strip()

        src, dests = line.split(': ')
        
        if src not in connections: connections[src] = []

        for dest in dests.split():
            connections[src].append(dest)
            if dest not in connections: connections[dest] = []
            connections[dest].append(src)


def contract(n1: str, n2: str, connections: Dict[str, List[str]]):
    """
    Contracts two nodes into a single node

    Parameters:
    n1 (str): Node 1
    n2 (str): Node 2
    connections (Dict[str, List[str]]): Graph edges
    """
    n1_neighbours = [edge for edge in connections[n1] if edge != n2]
    n2_neighbours = [edge for edge in connections[n2] if edge != n1]

    for neighbour in n1_neighbours:
        connections[neighbour] = [n1+n2 if edge == n1 else edge for edge in connections[neighbour]]
    
    for neighbour in n2_neighbours:
        connections[neighbour] = [n1+n2 if edge == n2 else edge for edge in connections[neighbour]]

    connections[n1+n2] = n1_neighbours + n2_neighbours
    del connections[n1]
    del connections[n2]

def karger_min_cut(connections: Dict[str, List[str]]) -> Dict[str, List[str]]:
    """
    Performs a karger min_cut: https://en.wikipedia.org/wiki/Karger%27s_algorithm

    Parameters:
    connections (Dict[str, List[str]]): Graph edges
    
    Returns:
    (Dict[str, List[str]]): Final graph edges (i.e. two super nodes connected by x edges that may be the min_cut)
    """
    while len(connections) > 2:
        n1 = random.choice(list(connections.keys()))
        n2 = random.choice(list(connections[n1]))
        contract(n1, n2, connections)

    return connections

min_cut = 0
while min_cut != 3:
    super_nodes = karger_min_cut(connections.copy())
    min_cut = len(super_nodes[list(super_nodes.keys())[0]])

group_size = len(list(super_nodes.keys())[0])/3
other_group_size = len(list(super_nodes.keys())[1])/3
print(f"ANSWER: {group_size*other_group_size}")
