INPUT = "input"

with open(INPUT, "r") as f:
    calibration = f.readlines()

def digit_filter(s: str) -> str:
    return ''.join(filter(str.isdigit, s))

def parse_digit(s: str) -> int:
    return int(s[0] + (s[-1]))

calibration = list(map(parse_digit, map(digit_filter, calibration)))
print(f"ANSWER: {sum(calibration)}")