from typing import Type
import z3

INPUT = "input"
PART_1 = False

MIN_POS = 200000000000000
MAX_POS = 400000000000000

class Hailstone:
    def __init__(self, x_pos, y_pos, z_pos, x_vel, y_vel, z_vel):
        self.x_pos = x_pos
        self.y_pos = y_pos
        self.z_pos = z_pos
        self.x_vel = x_vel
        self.y_vel = y_vel
        self.z_vel = z_vel

    def pos_x(self, x_val: int) -> bool:
        """ 
        Determines whether a given x value occurs forward in time for a hailstone

        Parameters:
        x_val (int): The x value
        
        Returns:
        bool: True if forward in time, else false
        """
        return (x_val >= self.x_pos and self.x_vel > 0) or (x_val <= self.x_pos and self.x_vel < 0)

    def xy_intersect(self, other: Type['Hailstone']) -> bool:
        """
        Determines whether the path of two hailstones intersect one another in the x/y plane, within the search bounds

        Parameters:
        other (Hailstone): Other hailstone

        Returns:
        bool: True for intersection, else false
        """
        slope = self.y_vel/self.x_vel
        other_slope = other.y_vel/other.x_vel

        try:
            x_intersect = (slope*self.x_pos - other_slope*other.x_pos + other.y_pos - self.y_pos)/(slope - other_slope)
        except ZeroDivisionError:
            return False
        
        y_intersect = slope * (x_intersect - self.x_pos) + self.y_pos

        return MIN_POS <= x_intersect <= MAX_POS and MIN_POS <= y_intersect <= MAX_POS and self.pos_x(x_intersect) and other.pos_x(x_intersect)

def parse_hailstone(text: str) -> Type[Hailstone]:
    """
    Parses a hailstone from raw text

    Parameters:
    text (str): Raw text

    Returns:
    Hailstone: Pared hailstone
    """
    pos, vel = text.split(' @ ')
    pos = [int(p) for p in pos.split(', ')]
    vel = [int(v) for v in vel.split(', ')]

    return Hailstone(*pos, *vel)

hailstones = []

with open(INPUT) as f:
    for line in f:
        line = line.strip()
        hailstones.append(parse_hailstone(line))

if PART_1:
    num_intersects = 0
    for i in range(len(hailstones)):
        for j in range(i+1, len(hailstones)):
            if hailstones[i].xy_intersect(hailstones[j]):
                num_intersects += 1

    print(f"ANSWER: {num_intersects}")
else: # Part 2
    """
    Note that the problem definition is over defined by the input, three objects in 3D space will intersect along a maximum of one line
    Thus the starting position and velocity found to connect the first three hailstones will indeed connect them all
    """
    s = z3.Solver()
    rx, ry, rz, rx_vel, ry_vel, rz_vel = z3.Ints('rx ry rz rx_vel ry_vel rz_vel')
    t1, t2, t3 = z3.Ints('t1 t2 t3')
    for stone, t in zip(hailstones[:3], [t1, t2, t3]):
        s.add(rx + rx_vel*t - stone.x_vel*t == stone.x_pos)
        s.add(ry + ry_vel*t - stone.y_vel*t == stone.y_pos)
        s.add(rz + rz_vel*t - stone.z_vel*t == stone.z_pos)

    s.check()
    m = s.model()
    pos_sum = m[rx].as_long() + m[ry].as_long() + m[rz].as_long()

    print(f"ANSWER: {pos_sum}")
