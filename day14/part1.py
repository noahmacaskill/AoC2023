INPUT = "input"

with open(INPUT, "r") as f:
    platform = f.readlines()

total_load = 0
for i in range(len(platform[0][:-1])):
    stack_index = 0
    for j in range(len(platform)):
        if platform[j][i] == '.':
            continue
        elif platform[j][i] == 'O':
            total_load += len(platform) - stack_index
            stack_index += 1
        else:
            stack_index = j+1

print(f"ANSWER: {total_load}")