INPUT = "input"

with open(INPUT, "r") as f:
    scratchcards = f.readlines()
    copies = [1 for _ in range(len(scratchcards))]

for index, card in enumerate(scratchcards):
    winning_nums, my_nums = card.split(':')[1].split('|')
    winning_nums = winning_nums.split()
    my_nums = my_nums.split()

    matching_nums = len([num for num in my_nums if num in winning_nums])
    
    for i in range(index+1, index+matching_nums+1):
        copies[i] += copies[index]

print(f"ANSWER: {sum(copies)}")