import random

def create_generation(states, r, population_size):
    new_states = []
    rules = []
    for i in range(len(states)):
        for j in range(r):
                if(states[i][j] not in rules):
                    rules.append(states[i][j])
    print(rules)
    if(r == 2):
        for i in range(population_size):
             x = random.randint(0, 55)
             y = random.choice(rules)
             new_states.append([x,y])
    else:
        for i in range(population_size):
             x = random.randint(0, 55)
             y = random.choice(rules)
             k = random.choice(rules)
             new_states.append([x,y,k])

    return new_states
    
# states = [[1,2,78], [2,3,56], [4,5,23], [5,6,32], [32,45,89], [43,45,12], [23,45,78]]
# print(create_generation(states, 3))