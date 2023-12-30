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
    filtered_node = ''.join(c for c in node if c.isalpha() or c.isspace())
    src, l, r = filtered_node.split()

    network[src] = (l, r)

index = 0
steps = 0
node = 'AAA'
while True:
    dir = dir_to_ind[lr[index]]
    node = network[node][dir]
    
    index += 1
    steps += 1

    if node == 'ZZZ':
        break

    if index == len(lr):
        index = 0

print(f"ANSWER: {steps}")
