import Species
import random

def ga():
    # Create Initial Species Population
    generation = 0
    test = Species.species(random.randint(0, 9), random.randint(0, 9))
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

    skills = [self.attack, self.defense]
    choice = random.randint(0, 1)
    if choice == 0:
        self.attack += random.randint(0, 4)
    if choice == 1:
        self.defense += random.randint(0, 4)

    return mutated

if __name__ == "__main__":
    ga()