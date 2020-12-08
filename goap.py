import json
# put goap stuff here

#Model will be that all changes from 1 genome to the next will get normalised to 1, 2, or 3 (probably), 
#So that GOAP doesn't have to deal with slightly missing decimals
#Going to import functions from a JSON file like in p5


#Initially define the JSON to be false so that we can initialise it properly
Explanations = False

#Going off of how P5 did it:

#Takes JSON objects/dictionaries and turns them into functions
def makeChange(changes):
    def effect(state):
        next_state = state.copy()
        for attribute, change in changes["Changes"]:
            next_state[attribute] += change
        
        return next_state

    return effect

# Should really make restrictions too
def makeRequirement(changes):
    def requirement(state):
        for attribute, requirement in changes["Requirements"]:
            if requirement[1] == "Equal":
                if state[attribute] != requirement:
                    return False

            if requirement[1] == "Less than":
                if state[attribute] <= requirement:
                    return False
            if requirement[1] == "Greater than":
                if state[attribute] >= requirement:
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

    # For now, going to run GOAP over every pair.
    for i in range(len(sequence)-1):
        search(sequence[i], sequence[i+1])

# Actually runs the GOAP
def search(start, finish):
    pass
# Normalises the values of the genome into a small variety of integers
def normalise(genome):
    for name in genome:
        #Need to hardcode different ranges
        if name == "offense" or name == "defense" or name == "heatRes" or name == "coldRes" or name == "social":
            genome[name] == int(genome[name] / 3)
        else:
            genome[name] == int(genome[name]/33)
    pass
