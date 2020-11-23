import Species
import random

def ga():
    # Create Initial Species Population
    generation = 0
    test = Species.species(random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), \
                            random.randint(0, 9), random.randint(0, 9), random.randint(0, 9), \
                            random.randint(0, 99), random.randint(0, 99), \
                            random.randint(0, 99), random.randint(0, 99), random.randint(0, 99))
    print("Initial: ", str(test))
    population = [test]
    while True:
        next_pop = gen_successors(population)
        generation += 1
        print("Generation: ", str(generation))
        for child in next_pop:
            print("Child: ", str(child))
        population = next_pop
        input("Press Enter to continue...")


def gen_successors(population):
    # generate successors from given population
    results = []
    for i in range(len(population)):
        results.append(gen_children(population[i], population[i]))
    return results

def gen_children(self, other):
    # generate children from given parents
    new_genome = mutate(self)
    return new_genome

def mutate(self):
    # cause mutation
    mutated = self

    # Picking a random basic stat to buff. This is mostly just to test rn
    choice = random.randint(0, 5)
    if choice == 0:
        self.offense += random.randint(0, 6)
    if choice == 1:
        self.defense += random.randint(0, 6)
    if choice == 2:
        self.aquatic += random.randint(0, 6)
    if choice == 3:
        self.heatRes += random.randint(0, 6)
    if choice == 4:
        self.coldRes += random.randint(0, 6)
    if choice == 5:
        self.social += random.randint(0, 6)

    # Changing Other stats
    choice = random.randint(0, 2)
    if choice == 0: # Size
        choice2 = random.randint(0, 1)
        if choice2 == 0:
            self.size -= random.randint(0, 10)
        if choice2 == 1:
            self.size += random.randint(0, 10)
    if choice == 1: # Diet
        choice2 = random.randint(0, 1)
        if choice2 == 0:
            self.diet -= random.randint(0, 10)
        if choice2 == 1:
            self.diet += random.randint(0, 10)
    if choice == 2: # Movement
        choice2 = random.randint(0, 2)
        if choice2 == 0:
            self.fly += random.randint(0, 10)
        if choice2 == 1:
            self.walk += random.randint(0, 10)
        if choice2 == 1:
            self.swim += random.randint(0, 10)

    
    return mutated

if __name__ == "__main__":
    ga()