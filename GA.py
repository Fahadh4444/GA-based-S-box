from statistics import pstdev
from collections import OrderedDict
from numpy import mean
import sbox as sbox
import rulelist as m3
import selection as rw
import generations as gt
import random


bent_functions = 2
input_len = 8
output_len = 8
MAX_STATES = 100
generations = 30

population_size = 20

best_individual = None
best_fitness = 0
best_DU = float('-inf')
best_NL = float('-inf')
worst_fitness = float('inf')
worst_DU = float('inf')
worst_NL = float('inf')
visited_states = OrderedDict()
best_states = []
fitness_scores = []
fitness = []
DUs=[]
NLs=[]

rules_list, rule_names = m3.return_rules()

# Create an empty 2D array
population = [[0]*bent_functions for i in range(population_size)]

# Populate the 2D array with random numbers
for i in range(population_size):
    for j in range(bent_functions):
        population[i][j] = random.randint(0, 55)

for gen in range(0, generations):
    print("Starting Generation: ",gen+1)
    print("Population: ", population)
    fitness_scores = []
    for i in range(population_size):
        if((population[i][0], population[i][1]) in visited_states):
            fitness_scores.append(visited_states[(population[i][0], population[i][1])])
            DUs.append(0)
            NLs.append(0)
            continue
        print("State: ",population[i])
        R, DU, NL = sbox.fitness(population[i], True)
        visited_states[(population[i][0], population[i][1])] = R
        fitness.append(R)
        fitness_scores.append(R)
        DUs.append(DU)
        NLs.append(NL)

        if(R < worst_fitness):
            worst_fitness = R
            worst_DU = DU
            worst_NL = NL
        if(R > best_fitness):
            best_fitness = R
            best_individual = population[i]
            best_DU = DU
            best_NL = NL
            best_states = [[rule_names[s] for s in population[i]]]
        elif (R == best_fitness and ([rule_names[s] for s in population[i]] not in best_states)):
            best_states.append([rule_names[s] for s in population[i]])

        if(len(visited_states) >= MAX_STATES):
            break
    
    print("Fitness_Scores: ", fitness_scores)
    print("Best fitness: ", best_fitness)
    print("Best Individual: ", best_individual)
    selections = rw.roulette_wheel_selection(population,fitness_scores,5)

    new_population = gt.create_generation(selections, bent_functions, population_size)
    population = new_population
    if(len(visited_states) >= MAX_STATES):
         break

print("************************************************Final Report************************************************")
print("Number of states visisted: ", len(visited_states))
print("Best Strength: ", best_fitness)
print("Worst Strength: ", worst_fitness)
print("Best DU: ", best_DU)
print("Best NL: ", best_NL)
print("Worst DU: ", worst_DU)
print("Worst NL: ", worst_NL)
print("Average Strength of visited States: ", round(mean(fitness),2))
print("Standard Deviation of strength: ", round(pstdev(fitness),2))
print("Number of states with best strengths: ", len(best_states))
print("Best States: ", best_states)