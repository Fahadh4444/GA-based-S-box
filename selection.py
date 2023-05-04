import random

def roulette_wheel_selection(rules, fitness_values, num_selections):
    # Calculate total fitness value
    total_fitness = sum(fitness_values)
    
    # Calculate selection probabilities
    selection_probs = [fitness/total_fitness for fitness in fitness_values]
    
    # Create wheel with selection probabilities
    wheel = []
    for i in range(len(fitness_values)):
        num_ticks = int(selection_probs[i] * 100)
        for j in range(num_ticks):
            wheel.append(i)
    
    # Perform selections
    selections = []
    i=0
    while(i<num_selections):
        selection_index = random.choice(wheel)
        selections.append(rules[selection_index])
        i = i+1
    
    return selections