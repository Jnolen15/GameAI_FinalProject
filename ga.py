import Species
import random

population_record = []

def randomSpecies(): # Creates a species with random stats This can be improved
    randSpecies = Species.species(random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), \
                                random.randint(0, 9), random.randint(0, 9), random.randint(0, 99), \
                                random.randint(0, 99), random.randint(0, 99), random.randint(0, 99),\
                                random.randint(0, 99))
    return randSpecies

def randomWorld(): # Creates a world with random stats This can be improved
    randWorld = Species.species(random.randint(49, 99), random.randint(49, 99), random.randint(49, 99), \
                                random.randint(49, 99), random.randint(49, 99), random.randint(0, 99), \
                                random.randint(0, 99), random.randint(0, 99), random.randint(0, 99),\
                                random.randint(0, 99), "WORLD", "The world State")
    return randWorld

def ga():
    
    generation = 0
    population = []
    # Create Initial Species Population
    for i in range(6):
        population.append(randomSpecies())
    # Create world State
    worldState = randomWorld()
    print("WORLD STATE: ", worldState)
    # Generation Loo
    while True:
        population_record.append(population)
        # Generate 6 new children
        next_pop = gen_successors(population)
        generation += 1
        # Calculate fitness new population
        # Print them out
        print("Generation: ", str(generation))
        for child in next_pop:
            print("Child: " , str(child))
            print("Child fitness: ", child.calc_fitness(worldState))
        # Set current pop to new pop
        population = next_pop
        # Break
        input("Press Enter to continue...")



def gen_successors(population):
    # generate successors from given population
    # Breeds each species with another species from the list.
    results = []
    for i in range(len(population)):
        results.append(gen_children(population[i], random.choice(population)))
    return results

def gen_children(self, other):
    # generate children from given parents
    parents = [self, other]
    child = Species.species(random.choice(parents).stats['offense'], random.choice(parents).stats['defense'], \
                            random.choice(parents).stats['heatRes'], random.choice(parents).stats['coldRes'], \
                            random.choice(parents).stats['social'], random.choice(parents).stats['size'], \
                            random.choice(parents).stats['diet'], random.choice(parents).stats['swim'], \
                            random.choice(parents).stats['walk'], random.choice(parents).stats['fly'], \
                            self.name, self.meaning)
    new_genome = mutate(child)
    child.parent_ids = [self.id, other.id]
    return new_genome

def mutate(self):
    # cause mutation
    mutated = self

    # Picking a random basic stat to buff. This is mostly just to test rn
    choice = random.randint(0, 4)
    if choice == 0:
        self.stats['offense'] += random.randint(0, 6)
    elif choice == 1:
        self.stats['defense'] += random.randint(0, 6)
    elif choice == 2:
        self.stats['heatRes'] += random.randint(0, 6)
    elif choice == 3:
        self.stats['coldRes'] += random.randint(0, 6)
    elif choice == 4:
        self.stats['social'] += random.randint(0, 6)

    # Changing Other stats
    choice = random.randint(0, 2)
    if choice == 0: # Size
        choice2 = random.randint(0, 1)
        if choice2 == 0:
            self.stats['size'] -= random.randint(0, 10)
        if choice2 == 1:
            self.stats['size'] += random.randint(0, 10)
    elif choice == 1: # Diet
        choice2 = random.randint(0, 1)
        if choice2 == 0:
            self.stats['diet'] -= random.randint(0, 10)
        if choice2 == 1:
            self.stats['diet'] += random.randint(0, 10)
    elif choice == 2: # Movement
        choice2 = random.randint(0, 2)
        if choice2 == 0:
            self.stats['fly'] += random.randint(0, 10)
        if choice2 == 1:
            self.stats['walk'] += random.randint(0, 10)
        if choice2 == 1:
            self.stats['swim'] += random.randint(0, 10)

    
    return mutated

if __name__ == "__main__":
    ga()