import heapq
from itertools import product
from typing import Type

INPUT = "input"
PART_1 = False

X_DIM = 10
Y_DIM = 10

HEIGHT = 0
BLOCK = 1

class Block:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z
        self.support_blocks = []
        self.supported_blocks = []

    # Block comparator is based on height
    def __lt__(self, other) -> bool:
        return self.z[1] < other.z[1]

    # Support block are the blocks holding a block up
    def add_support_block(self, support_block: Type['Block']):
        self.support_blocks.append(support_block)
        support_block.add_supported_block(self)

    # Supported blocks on supported by a block
    def add_supported_block(self, supported_block: Type['Block']):
        self.supported_blocks.append(supported_block)

    # Drop a block to a specified new z value
    def drop_block(self, new_z: int):
        self.z = (new_z, new_z+(self.z[1]-self.z[0]))

    def safe_disintegration(self) -> bool:
        """
        Determines if a block can be safely disintegrated (i.e. wouldn't cause other blocks to fall upon disintegration)

        Parameters:
        self (Block): The block

        Returns:
        Bool: True if safe disintegration
        """
        for block in self.supported_blocks:
            if len(block.support_blocks) <= 1:
                return False

        return True
    
    def total_supported_blocks(self) -> int: 
        """
        Determines the total blocks supported by a block - specifically those that would fall if the block were disintegrated
        """
        priority_supported_blocks = [block for block in self.supported_blocks if len(block.support_blocks) == 1]
        heapq.heapify(priority_supported_blocks)
        supported_blocks = set(priority_supported_blocks)
        num_supported = len(supported_blocks)

        while priority_supported_blocks:
            block = heapq.heappop(priority_supported_blocks)

            for new_block in block.supported_blocks:
                if all(block in supported_blocks for block in new_block.support_blocks):
                    heapq.heappush(priority_supported_blocks, new_block)
                    supported_blocks.add(new_block)
                    num_supported += 1
            supported_blocks.discard(block)

        return num_supported

def parse_block(text: str) -> Type[Block]:
    """
    Parses a block from plain text

    Parameters:
    text (str): Raw text

    Returns:
    Block: A block object
    """
    mins, maxes = text.split('~')

    x1, y1, z1 = (int(x) for x in mins.split(','))
    x2, y2, z2 = (int(x) for x in maxes.split(','))

    return Block((x1, x2+1), (y1, y2+1), (z1, z2+1))

blocks = {}
with open(INPUT) as f:
    for ind, line in enumerate(f):
        line = line.strip()
        blocks[ind] = parse_block(line)

# Determine how the blocks fall, and which blocks support each other
blocks = dict(sorted(blocks.items(), key=lambda b: b[1].z[0]))
tower = [[(1, None) for _ in range(X_DIM)] for _ in range(Y_DIM)]
for (ind, block) in blocks.items():
    min_x, max_x = block.x[0], block.x[1]
    min_y, max_y = block.y[0], block.y[1]
    max_z = 0
    support_blocks = set()
    for x, y in product(range(min_x, max_x), range(min_y, max_y)):
        height, support_block = tower[x][y]
        
        if height == max_z and support_block is not None:
            support_blocks.add(support_block)
        elif height > max_z:
            support_blocks = {support_block} if support_block != None else set()
            max_z = height

    block.drop_block(max_z)
    new_value = (block.z[1], ind)
    tower[min_x:max_x] = [row[:min_y] + [new_value] * (max_y-min_y) + row[max_y:] for row in tower[min_x:max_x]]

    for support_block in support_blocks:
        block.add_support_block(blocks[support_block])

# Tally final answer
num_safe_disintegration = 0
total_brick_fall = 0
for block in blocks.values():
    if block.safe_disintegration() and PART_1:
        num_safe_disintegration += 1
    elif not block.safe_disintegration() and not PART_1:
        total_brick_fall += block.total_supported_blocks()

if PART_1:
    print(f"ANSWER: {num_safe_disintegration}")
else:
    print(f"ANSWER: {total_brick_fall}")
