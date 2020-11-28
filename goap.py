import json
# put goap stuff here

#Model will be that all changes from 1 genome to the next will get normalised to 1, 2, or 3 (probably), 
#So that GOAP doesn't have to deal with slightly missing decimals
#Going to import functions from a JSON file like in p5

#Going off of how P5 did it:

#Takes JSON objects/dictionaries and turns them into functions
def makeChange(change):
    def effect(state):
        next_state = state.copy()
        for attribute, change in state["Changes"]:
            next_state[attribute] += change

    return effect

#Only want to initialise the possible changes once, so function for it
def init():
    with open("GOAP_Actions.json") as f:
        Explanations = json.load(f)
        #Need to ask in office hours why in P5 we could access the equivalent variable anywhere