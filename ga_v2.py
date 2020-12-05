import Species
import random
from evolution_increments import get_evolution_increment_set

evolution_pool = get_evolution_increment_set(num_increments=1000)
population_size = 60
# Extremely brute-forcey, but the quickest thing I can think of is to
# Literally store population at each generation
population_record = []

def randomSpecies(): # Creates a species with random stats This can be improved
    randSpecies = Species.species()
    num_evolutions = random.randint(5, 25)

    for n in range(num_evolutions):
      randSpecies.add_increment(random.choice(evolution_pool))

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

    for i in range(population_size):
        population.append(randomSpecies())
    # Create world State
    worldState = randomWorld()
    print("WORLD STATE: ", worldState)
    # Generation Loo
    while True:
        # To keep track of entire population
        population_record.append(population)

        # Generate 6 new children
        next_pop = gen_successors(population, worldState, generation)

        generation += 1
        # Calculate fitness new population
        # Print them out
        print("Generation: ", str(generation))
        max_fitness_child = max(next_pop, key=lambda p: p.calc_fitness(worldState))
        print("Max Fitness Child: ", str(max_fitness_child))
        print("Fitness: ", max_fitness_child.calc_fitness(worldState))
        """Print Lineage"""
        current_member = max_fitness_child
        print('========Lineage=========')
        print('current: {}'.format(current_member.print_increments()))
        i = generation
        while i >= 1:
          parent_population = population_record[i - 1]
          parent_a = [p for p in parent_population
                      if p.id == current_member.parent_ids[0]][0]
          parent_b = [p for p in parent_population
                      if p.id == current_member.parent_ids[1]][0]

          print("Gen {} left parent: {}".format(i, parent_a.print_increments()))
          current_member = parent_a
          i -= 1


        # Set current pop to new pop
        population = next_pop
        # Break
        input("Press Enter to continue...")


def gen_successors(population, world_state, generation):
    # generate successors from given population
    # Breeds each species with another species from the list.
    all_children = []
    for i in range(population_size * 2):
        all_children.append(gen_children(random.choice(population), random.choice(population)))

    def tournament_select(population, k=3):
        tournament = random.choices(population, k=k)
        return max(tournament, key=lambda t: t.calc_fitness(world_state))

    result_population = []
    for i in range(population_size):
      result_population.append(tournament_select(all_children))

    return result_population



def gen_children(self, other):
    # generate children from given parents
    parents = [self, other]
    crossover_point_self = random.randint(int(0.25 * len(self.evolutions)), int(0.75 * len(self.evolutions)))
    crossover_point_other = random.randint(int(0.25 * len(other.evolutions)), int(0.75 * len(other.evolutions)))
    child = Species.species()
    child.parent_ids = [self.id, other.id]
    for a in range(0, crossover_point_self):
      child.add_increment(self.evolutions[a])
    for b in range(crossover_point_other, len(other.evolutions)):
      child.add_increment(other.evolutions[b])

    if len(child.evolutions) == 0:
      print('empty child?')


    return mutate(child)



def mutate(self):
    # cause mutation
    mutate_choice = random.random()
    if mutate_choice < 0.7:
      return self

    mutated = self
    mutated.add_increment(random.choice(evolution_pool))
    return mutated

if __name__ == "__main__":
    ga()