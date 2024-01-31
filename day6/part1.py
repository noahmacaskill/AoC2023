import numpy as np

INPUT = "input"

with open(INPUT, "r") as f:
    boat_races = f.readlines()

def break_record(time: int, record: int) -> int:
    """
    Given a race duration and record distance, returns the number of ways a race can be won.
    Distance of a race can be given by the formula: d=h(t-h) where:
        d = distance
        h = time spent holding the button
        t = race duration
    The roots of the quadratic function where d=record are solved, yielding the values for which the record is beaten

    Parameters:
    - time (int): Duration of race
    - record (int): Record distance of race
    
    Returns:
    int: Number of ways the record can be beaten
    """

    root1, root2 = np.roots([-1, time, -record])
    return abs(int(root1)-int(root2))

race_times = [int(x) for x in boat_races[0].split(':')[1].split()]
record_distances = [int(x) for x in boat_races[1].split(':')[1].split()]

ways_to_win = []

for time, record in zip(race_times, record_distances):
    ways_to_win.append(break_record(time, record))

print(f"ANSWER: {np.prod(ways_to_win)}")