import json
from heapq import heappop, heappush
from collections import namedtuple, defaultdict, OrderedDict
# put goap stuff here

#Model will be that all changes from 1 genome to the next will get normalised to 1, 2, or 3 (probably), 
#So that GOAP doesn't have to deal with slightly missing decimals
#Going to import functions from a JSON file like in p5


#Initially define the JSON to be false so that we can initialise it properly
Explanations = False
#Do same with changes
all_changes = False
#Going off of how P5 did it:

Change = namedtuple('Change', ['name', 'check', 'effect', "cost"])

#Takes JSON objects/dictionaries and turns them into functions
def makeChange(changes):
    def effect(state):
        next_state = state.copy()
        for attribute, change in changes["Changes"]:
            next_state.stats[attribute] += change
        
        return next_state

    return effect

# Should really make restrictions too
def makeRequirement(changes):
    def requirement(state):
        for attribute, requirement in changes["Requirements"]:
            if requirement[1] == "Equal":
                if state.stats[attribute] != requirement:
                    return False
            if requirement[1] == "Less than":
                if state.stats[attribute] <= requirement:
                    return False
            if requirement[1] == "Greater than":
                if state.stats[attribute] >= requirement:
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
def explain_full(sequence):
    #Initialise the file
    if not Explanations:
        init()

    #Do same with changes
    global all_changes
    for name, change_original in Explanations.items():
        checker = makeRequirement(change_original)
        effector = makeChange(change_original)
        change = Change(name, checker, effector, 1)
        all_changes.append(change)
    # For now, going to run GOAP over every pair.
    for i in range(len(sequence)-1):
        path = search(sequence[i], sequence[i+1])
        print("Generation " + (i+1))
        for value in path:
            print(sequence[i].name + value)
            

#Same as in P5, constructs the objects that we then search through
def graph(state):
    # Iterates through all recipes/rules, checking which are valid in the given state.
    # If a rule is valid, it returns the rule's name, the resulting state after application
    # to the given state, and the cost for the rule.
    for r in all_changes:
        if r.check(state):
            yield (r.name, r.effect(state), r.cost)

# Actually runs the GOAP
def search(start, finish):
    frontQueue = []
    heappush(frontQueue, (0, start))
    action_to_state[start] = None
    came_from[start] = None
    cost_so_far[start] = 0
    while frontQueue:
        _, current_state = heappop(frontQueue)
    #----------------------------------------------------------------
    #is what happens if we find destination
        if is_goal(current_state):
            #print (cost_so_far[current_state])
            pathCells = []
            cs = current_state
            while cs is not state:
                action = action_to_state[cs] #action to lead up to previous state
                pathCells.append((cs, action)) #append previous state and the action
                cs = came_from[cs] #go back one, this has to be on the end because otherwise we might be putting in None. I guess I can do while came_from[cs] is not none but too late im sticking with it
            pathCells.reverse()
            final_time = time() - start_time
            return pathCells
    #-----------------------------------------------------------------

        for name, new_state, cost_to_state in graph(current_state):
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
        #Need to hardcode different ranges
        if name == "offense" or name == "defense" or name == "heatRes" or name == "coldRes" or name == "social":
            genome.stats[name] == int(genome.stats[name] / 3)
        else:
            genome.stats[name] == int(genome.stats[name]/33)
    pass
# For now, blank
def heuristic(state, name):
    return (0)