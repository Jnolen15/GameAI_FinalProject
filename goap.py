import json
import Species
from heapq import heappop, heappush
from collections import namedtuple, defaultdict, OrderedDict
from math import inf, ceil
from produce_explanations import generate_starter_world_explanation
# put goap stuff here

#Model will be that all changes from 1 genome to the next will get normalised to 1, 2, or 3 (probably), 
#So that GOAP doesn't have to deal with slightly missing decimals
#Going to import functions from a JSON file like in p5


#Initially define the JSON to be false so that we can initialise it properly
Explanations = False
#Do same with changes
all_changes = False
#Do same with world changes
all_world_changes = False

#Going off of how P5 did it:

Change = namedtuple('Change', ['name', 'check', 'effect', "cost", "description"])

#Takes JSON objects/dictionaries and turns them into functions
def makeChange(changes):
    def effect(state):
        next_state = state.copy()
        #print("state")
        #print(state)
        #print("next state")
        #print(next_state)
        
        for attribute, change in changes["Changes"].items():
            #print (type(next_state.stats[attribute]))
            next_state.stats[attribute] += change
        
        return next_state

    return effect

# Should really make restrictions too
def makeRequirement(changes):
    def requirement(state):
        for attribute, requirement in changes["Requirements"].items():
            if requirement[1] == "Equal":
                if state.stats[attribute] != requirement[0]:
                    return False
            if requirement[1] == "Less than":
                if state.stats[attribute] < requirement[0]:
                    return False
            if requirement[1] == "Greater than":
                if state.stats[attribute] > requirement[0]:
                    return False
        return True
    return requirement

#Only want to initialise the possible changes once, so function for it
def init():
    global Explanations
    with open("GOAP_Actions.json") as f:
        Explanations = json.load(f)
    #Really hope this is correct global syntax

# Main method that deals with running GOAP on each pair and outputting results
# Parameters:
# - sequence = the list of ancestors in a lineage
# - lineage_world_map = a dictionary mapping indices from lineage to world states
def explain_full(sequence, lineage_world_map,
                 current_species_explain_map, current_world_explain_map):

    # Used to keep track of the terms we used to explain changes in the species
    species_changes_map = {}
    # Used to keep track of the terms we used to explain changes in the world
    world_changes_map = {}

    def update_species_change_map(explain_map):
        # Collect changes and add them to the species change map
        for change_key, change_cause in explain_map.items():
            # If the path includes multiple changes to the same stat, add to the list
            if change_key in species_changes_map:
                species_changes_map[change_key].append(change_cause)
            # Else make a new list
            else:
                species_changes_map[change_key] = [change_cause]

    def update_world_change_map(explain_map):
        # Collect changes and add them to the world change map
        for change_key, change_cause in explain_map.items():
            # If the path includes multiple changes to the same stat, add to the list
            if change_key in world_changes_map:
                world_changes_map[change_key].append(change_cause)
            # Else make a new list
            else:
                world_changes_map[change_key] = [change_cause]

    # Initialise the file
    if not Explanations:
        init()

    # Do same with changes
    global all_changes
    all_changes = []
    for name, change_original in Explanations["Operations"].items():
        checker = makeRequirement(change_original)
        effector = makeChange(change_original)
        change = Change(name, checker, effector, 1, change_original["Message"])
        all_changes.append(change)

    # World changes
    global all_world_changes
    all_world_changes = []
    for name, change_original in Explanations["WorldOperations"].items():
        checker = makeRequirement(change_original)
        effector = makeChange(change_original)
        change = Change(name, checker, effector, 1, change_original["Message"])
        all_world_changes.append(change)

    # Normalise all the values in the genomes
    for genome in sequence:
        normalise(genome)


    # Normalise all world sequence genomes:
    for key in lineage_world_map.keys():
        normalise(lineage_world_map[key])

    #Keep track of the name
    species_name = sequence[0].name


    #Explain the initial species and world states

    initial_world_path = search(Species.species(), lineage_world_map[0], world_search=True)
    if len(initial_world_path) != 0:
        for state, message, explain_map in initial_world_path:
            update_world_change_map(explain_map)
    print(generate_starter_world_explanation(world_changes_map))

    """
    initial_species_path = search(Species.species(), sequence[0])
    if len(initial_species_path) != 0:
        for state, message, explain_map in initial_species_path:
            update_species_change_map(explain_map)
    """

    # In this version, GOAP runs over ranges separated by world changes
    # (for example, world changes occur at 1, 25, 28, and 40. Then 1-25, 25-28, 28-40, and 40-end
    # each require explanations
    # Each item in lineage_world_map is (lineage_index, corresponding_world_state)
    lineage_world_map_items = list(lineage_world_map.items())
    for i in range(len(lineage_world_map_items)):

        # The start of the world range sequence is the lineage index
        # of the current item
        species_start_index = lineage_world_map_items[i][0]
        # The end of the world range sequence is either
        # the lineage index of the next item (i + 1), or the final species if we are at the end
        if i == len(lineage_world_map_items) - 1:
            species_end_index = len(sequence) - 1
        else:
            species_end_index = lineage_world_map_items[i + 1][0]
        # Find an explantion path from the start to the end of the range
        path = search(sequence[species_start_index], sequence[species_end_index])



        if len(path) != 0:
            print("Generation " + str(lineage_world_map_items[i][0] + 1))
            if species_name != sequence[i].name:
                print("The " + species_name + " species is now known as " + sequence[i].name + " due to changes in its genome.")
                species_name = sequence[i].name
            for state, message, explain_map in path:
                print(sequence[i].name + message)
                update_species_change_map(explain_map)

        if species_name != sequence[i].name:
            print("The " + species_name + " species is now known as " + sequence[i].name + \
                  " due to changes in its genome.")
        print("After " + str(lineage_world_map_items[-1][0] + 1) + " generations, " + sequence[i].name + " has evolved to become the apex species of this world.")

        #print('TEST EXPLANATION: ' + generate_explanation(species_changes_map, current_world_explain_map))
        # Next, explain the change in world state
        if i < len(lineage_world_map_items) - 1:
            # The value of the current lineage_world_map item
            world_start = lineage_world_map_items[i][1]
            # The value of the next lineage_world_map item (i + 1)
            world_end = lineage_world_map_items[i + 1][1]
            world_path = search(world_start, world_end, world_search=True)
            if len(world_path) != 0:
                for state, message, explain_map in world_path:
                    print(message)
                    update_world_change_map(explain_map)




    # Absorb species changes into active species explanations
    for change_key, change_causes in species_changes_map.items():
        # If the species already has evolutions for the stat change, add to the list
        if change_key in current_species_explain_map:
            current_species_explain_map[change_key].extend(change_causes)
        # Else make a new list
        else:
            current_species_explain_map[change_key] = change_causes

        # remove duplicates
        current_species_explain_map[change_key] = list(set(current_species_explain_map[change_key]))

    # Absorb world changes into active world explanations
    for change_key, change_causes in world_changes_map.items():
        if change_key in current_world_explain_map:
            current_world_explain_map[change_key].extend(change_causes)
        else:
            current_world_explain_map[change_key] = change_causes

        current_world_explain_map[change_key] = list(set(current_world_explain_map[change_key]))

#Same as in P5, constructs the objects that we then search through
# The world_search parameter alternates between using the list of world changes &
# the list of species changes. It's passed in from search.
def graph(state, world_search=False):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    changes = all_world_changes if world_search else all_changes
    for r in changes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost, r.description)

# Actually runs the GOAP
# The world_search parameter alternates between using the list of world changes &
# the list of species changes. It defaults to species.
def search(start, finish, world_search=False):
    frontQueue = []
    heappush(frontQueue, (0, start))
    action_to_state = {}
    came_from = {}
    cost_so_far = {}
    action_to_state[start] = None
    came_from[start] = None
    cost_so_far[start] = 0
    while frontQueue:
        _, current_state = heappop(frontQueue)
    #----------------------------------------------------------------
    #is what happens if we find destination
        if all([finish.stats[key] == current_state.stats[key] for key in current_state.stats.keys()]):
            #print ("finished")
            #print (cost_so_far[current_state])
            pathCells = []
            cs = current_state
            while cs is not start:
                action_name = action_to_state[cs] #action to lead up to previous state

                explanation_source = Explanations["WorldOperations" if world_search else "Operations"]
                action = explanation_source[action_name]["Message"]
                explanation_map = explanation_source[action_name]["ExplanationMap"]

                pathCells.append((cs, action, explanation_map)) #append previous state and the action
                cs = came_from[cs] #go back one, this has to be on the end because otherwise we might be putting in None. I guess I can do while came_from[cs] is not none but too late im sticking with it
            pathCells.reverse()
            return pathCells
    #-----------------------------------------------------------------

        for name, new_state, cost_to_state, description in graph(current_state, world_search):
            cost = cost_to_state
            new_cost = cost_so_far[current_state] + cost
            if new_cost != inf and (new_state not in cost_so_far or new_cost < cost_so_far[new_state]):
                #print("adding")
                cost_so_far[new_state] = new_cost
                priority = new_cost + heuristic(new_state, name)
                heappush(frontQueue, (priority, new_state))
                came_from[new_state] = current_state
                action_to_state[new_state] = name
    pass

# Normalises the values of the genome into a small variety of integers
def normalise(genome):
    for name in genome.stats:
        #print(name)
        genome.stats[name] = int(genome.stats[name]/20)
    pass
# For now, blank
def heuristic(state, name):
    for name in state.stats:
        if state.stats[name] < 0 or state.stats[name] > 4:
            return inf
    return (0)