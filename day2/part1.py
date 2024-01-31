import re

INPUT = "input"
MAX_BLUE, MAX_GREEN, MAX_RED = 14, 13, 12

with open(INPUT, "r") as f:
    games = f.readlines()

def digit_filter(s: str) -> int:
    return int(''.join(filter(str.isdigit, s)))

def parse_game(game: str) -> tuple[int, int, int, int]:
    """
    Parses information about a game

    Parameters:
    - game (str): The game string as given from the input

    Returns:
    tuple[int, int, int, int]: 
        1. Game ID
        2. Maximum blue cubes pulled at one time
        3. Maximum green cubes pulled at one time
        4. Maximum red cubes pulled at one time
    """
    game_id, game = (game.split(':', 1))
    game_id = digit_filter(game_id)

    max_blue = max_green = max_red = 0

    for cubes in re.split(r';|,', game):
        num_pulled = digit_filter(cubes)
        if 'blue' in cubes and num_pulled > max_blue:
            max_blue = num_pulled
        elif 'green' in cubes and num_pulled > max_green:
            max_green = num_pulled
        elif 'red' in cubes and num_pulled > max_red:
            max_red = num_pulled

    return (game_id, max_blue, max_green, max_red)

games = list(map(parse_game, games))
id_sum = 0

for game in games:
    if game[1] <= MAX_BLUE and game[2] <= MAX_GREEN and game[3] <= MAX_RED:
        id_sum += game[0]

print(f"ANSWER: {id_sum}")
