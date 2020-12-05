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