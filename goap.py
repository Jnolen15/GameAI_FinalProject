import json
from heapq import heappop, heappush
from collections import namedtuple, defaultdict, OrderedDict
from math import inf, ceil
# put goap stuff here

#Model will be that all changes from 1 genome to the next will get normalised to 1, 2, or 3 (probably), 
#So that GOAP doesn't have to deal with slightly missing decimals
#Going to import functions from a JSON file like in p5


#Initially define the JSON to be false so that we can initialise it properly
Explanations = False
#Do same with changes
all_changes = False
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
def explain_full(sequence, world_state_indices):

    # Sequence = the list of ancestors in a lineage
    # World state indices = at which ancestor indices did the world change?

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

    # Normalise all the values in the genomes
    for genome in sequence:
        normalise(genome)
    #Keep track of the name
    species_name = sequence[0].name

    # In this version, GOAP runs over ranges separated by world changes
    # (for example, world changes occur at 1, 25, 28, and 40)
    # Each i in world state indices marks the beginning of a range
    # Each i + 1 marks the end of that range
    # For example, 1-25, 25-28, 28-40
    for i in range(len(world_state_indices)):

        # The start of the world range sequence
        start = world_state_indices[i]
        # The end of the world range sequence
        # (if i == len(world_state indices), just go use the final species as the end
        end = len(sequence) - 1 if i == len(world_state_indices) - 1 else world_state_indices[i + 1]
        path = search(sequence[start], sequence[end])

        if len(path) != 0:
            print("Generation " + str(world_state_indices[i] + 1) + " (describe how world changed here)")
            if species_name != sequence[i].name:
                print("The " + species_name + " species is now known as " + sequence[i].name " due to changes in its genome.")
            for value in path:
                print(sequence[i].name + " " + value[1])

#Same as in P5, constructs the objects that we then search through
def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_changes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost, r.description)

# Actually runs the GOAP
def search(start, finish):
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
                action = action_to_state[cs] #action to lead up to previous state
                pathCells.append((cs, action)) #append previous state and the action
                cs = came_from[cs] #go back one, this has to be on the end because otherwise we might be putting in None. I guess I can do while came_from[cs] is not none but too late im sticking with it
            pathCells.reverse()
            return pathCells
    #-----------------------------------------------------------------

        for name, new_state, cost_to_state, description in graph(current_state):
            cost = cost_to_state
            new_cost = cost_so_far[current_state] + cost
            if new_cost != inf and (new_state not in cost_so_far or new_cost < cost_so_far[new_state]):
                #print("adding")
                cost_so_far[new_state] = new_cost
                priority = new_cost + heuristic(new_state, name)
                heappush(frontQueue, (priority, new_state))
                came_from[new_state] = current_state
                action_to_state[new_state] = description
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