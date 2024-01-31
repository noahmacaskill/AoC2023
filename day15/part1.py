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

result = 0
for step in init_sequence.split(','):
    result += hash_algo(step)

print(f"ANSWER: {result}")
