with open("input", "r") as f:
    scratchcards = f.readlines()

point_total = 0

for card in scratchcards:
    winning_nums, my_nums = card.split(':')[1].split('|')
    winning_nums = winning_nums.split()
    my_nums = my_nums.split()

    matching_nums = [num for num in my_nums if num in winning_nums]
    point_total += int(2**(len(matching_nums)-1))

print(f"ANSWER: {point_total}")