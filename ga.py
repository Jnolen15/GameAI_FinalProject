import Species
import random
import time
import numpy as np

population_record = []
worldState_record = []
population_size = 150


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
    frontier_generation = 0
    population = []

    # Create Initial Species Population
    for i in range(population_size):
        population.append(randomSpecies())

    # Create world State and save in record
    worldState = randomWorld()
    print("WORLD STATE: ", worldState)
    worldState_record = [worldState]
    new_worldState = worldState

    # Generation Loop
    while True:
        # Save fitness given current world state
        for member in population:
            member.set_saved_fitness(worldState)
        # Save current population in population record
        population_record.append(population)

        # Update world if necessary
        worldState = new_worldState

        # Generate new population
        next_pop = gen_successors(population, worldState)

        generation += 1
        frontier_generation += 1

        print("Generation: ", str(generation))
        max_child = max(next_pop, key=lambda p: p.calc_fitness(worldState))
        print("Max child fitness: {}".format(max_child.calc_fitness(worldState)))
        time.sleep(1)

        def check_evolutionary_milestone():
            # stubbing this out. For now, it happens every so often
            #return random.random() < 0.075
            # Picking based on the fitness of the best current population
            if max_child.calc_fitness(worldState) > 0:
                return True

        # If we've reached an evolutionary milestone:
        # get the lineage of parents up till this point,
        # get the list of world states,
        # and clear the records
        if check_evolutionary_milestone():
            print('==================================')
            print('Reached an evolutionary milestone!')
            # Get parent_sequence
            lineage = [max_child]
            current_generation = frontier_generation
            while current_generation > 0:
                # Get parents from previous generation
                parents = [p for p in population_record[current_generation - 1]
                           if p.id in lineage[-1].parent_ids]

                # Choose the parent who had the highest fitness
                lineage.append(max(parents, key=lambda p: p.saved_fitness))

                # Backtrack to previous generation
                current_generation -= 1

            lineage.reverse()

            print('Lineage: {}'.format(', '.join([p.name for p in lineage])))
            print('Num world state changes: {}'.format(len(worldState_record)))

            # At this point, we have a lineage & world state record to pass to GOAP
            print('Call GOAP here!')
            print('==================================')
            time.sleep(5)

            # Reset tracked population & world states
            population_record.clear()
            worldState_record = [worldState]
            frontier_generation = 0

        def check_should_evolve_world():
            return random.random() < 0.1

        def get_evolved_world(current_world_state):
            # Copy
            next_world_state = Species.species()
            for (stat, val) in current_world_state.stats.items():
                next_world_state.stats[stat] = val

            # Mega mutation
            change = np.random.normal(loc=50, scale=10)
            direction = random.choice([-1, 1])
            stat_to_change = random.choice(list(current_world_state.stats.keys()))

            next_world_state.stats[stat_to_change] += change * direction
            return next_world_state


        # World mutation
        if check_should_evolve_world():
            new_worldState = get_evolved_world(worldState)
            worldState_record.append(new_worldState)
            print('The world is changing!')
            time.sleep(5)



        # Advance to next pop
        population = next_pop


def gen_successors(population, world_state):
    # generate successors from given population
    # Breeds each species with another species from the list.
    selected_parents = []

    # Which percent of the population to use for breeding
    select_factor = 0.4
    parents_count = int(population_size * select_factor)

    def tournament_select(population, k=3):
        tourney = random.choices(population, k=k)
        return max(tourney, key=lambda p: p.calc_fitness(world_state))

    # Get selected breeding parents
    for _ in range(parents_count):
        selected_parents.append(tournament_select(population))

    # Make children
    child_pop = []
    while len(child_pop) < population_size:
        parents = random.choices(selected_parents, k=2)
        child_pop.extend(gen_children(parents[0], parents[1], world_state))

    return child_pop


def gen_children(parent1, parent2, world_state):
    # generate children from given parents
    parents = [parent1, parent2]

    # crossover
    child = Species.species()
    stats = list(parent1.stats.keys())
    
    # "Pull" crossover
    # Picks a parent for base stats then pulls the stats in the direction of the other parent
    # If parent 2 has a low stat it will decrease a little. and vice versa if higher
    # Child gets stats of first parent
    for stat in stats:
        child.stats[stat] = parent1.stats[stat]
    # Stats are pulled twords second parent
    for stat in stats:
        if parent1.stats[stat] > parent2.stats[stat]: # If parent2 stat is lower
            diff = abs(parent1.stats[stat] - parent2.stats[stat])
            child.stats[stat] -= ((diff - (diff % 5)) / 5)
        elif parent1.stats[stat] < parent2.stats[stat]: # If parent2 stat is higher
            diff = abs(parent1.stats[stat] - parent2.stats[stat])
            child.stats[stat] += ((diff - (diff % 5)) / 5)

    """
    # Random choice between two parents' choices for stat.
    # I think this might be called like checkerboard crossover
    for stat in stats:
        child.stats[stat] = random.choice(parents).stats[stat]
    """

    # Set parent IDs for new child
    child.parent_ids = [parent1.id, parent2.id]

    # Copy name and meaning
    child.name = random.choice(parents).name
    #child.meaning = parent1.meaning

    # Mutate
    child.mutate()

    # In case we decide to support multiple children
    return [child]

if __name__ == "__main__":
    ga()