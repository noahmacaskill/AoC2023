INPUT = "input"

with open(INPUT, "r") as f:
    init_sequence = f.readline()[:-1]

def hash_algo(s: str) -> int:
    """
    Runs the HASH algorithms on a string

    Parameters:
    s (str): Input string

    Returns:
    int: HASH output
    """
    val = 0
    for c in s:
        val += ord(c)
        val *= 17
        val = val % 256
    
    return val

boxes = [{} for _ in range(256)]

for step in init_sequence.split(','):
    for i, c in enumerate(step):
        if c == '=':
            label = step[:i]
            hash = hash_algo(label)
            boxes[hash][label] = int(step[i+1:])
        elif c == '-':
            label = step[:i]
            hash = hash_algo(step[:i])
            try:
                del boxes[hash][label]
            except KeyError:
                pass

foc_pow = 0
for i, box in enumerate(boxes):
    for j, focal in enumerate(box.values()):
        foc_pow += (i+1) * (j+1) * focal

print(f"ANSWER: {foc_pow}")
