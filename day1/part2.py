with open("input", "r") as f:
    calibration = f.readlines()

# Replacements must be cushioned with the spelled out numbers to deal with overlap cases in which we want to preserve each number
# e.g. oneight, eightwo, etc.
keywords = {
    'one': 'one1one',
    'two': 'two2two',
    'three': 'three3three',
    'four': 'four4four',
    'five': 'five5five',
    'six': 'six6six',
    'seven': 'seven7seven',
    'eight': 'eight8eight',
    'nine': 'nine9nine'
}

def find_hidden_numbers(s: str) -> str:
    for k, r in keywords.items():
        s = s.replace(k, r)

    return s

def digit_filter(s: str) -> str:
    return ''.join(filter(str.isdigit, s))

def parse_digit(s: str) -> int:
    return int(s[0] + (s[-1]))

functions = [find_hidden_numbers, digit_filter, parse_digit]

for function in functions:
    calibration = list(map(function, calibration))

print(f"ANSWER: {sum(calibration)}")