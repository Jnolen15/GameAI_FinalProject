import json
species_attributes = ['offense', 'defense', 'heatRes', 'coldRes', 'social', 'size', 'diet', 'swim', 'walk', 'fly']
import random

f = open("stat_sheet_dump.txt", "w")

num_rolls = 50
max_changes = 3


evolutions = {}
for roll in range(num_rolls):
    evolution_name = "Evolution{}".format(roll)
    evolution = {}

    evolution["Requirements"] = {}



    change_configurations = [
        {"stat0": 1},
        {"stat0": 2, "stat1": -2},
        {"stat0": 2, "stat1": -1, "stat2": -1},
        {"stat0": 1, "stat1": 1, "stat2": -2}
    ]

    change_configuration = random.choice(change_configurations)
    evolution["Changes"] = {}
    direction = random.choice([-1,1])
    stats_to_change = random.choices(species_attributes, k=len(change_configuration.keys()))
    for (i, value) in enumerate(change_configuration.values()):
        evolution["Changes"][stats_to_change[i]] = value * direction

        has_corresponding_requirement = random.random() < 0.15
        if has_corresponding_requirement:
            requirement_operator = random.choice(["Less Than", "Greater Than"])
            requirement_value = 0
            if requirement_operator == "Less Than":
                requirement_value = random.choice([1, 2])
            else:
                requirement_value = random.choice([0, 1])

            evolution["Requirements"][stats_to_change[i]] = \
                [requirement_value, requirement_operator]

    evolution["Message"] = "Mesage goes here"
    evolutions[evolution_name] = evolution

dump = json.dumps(evolutions, indent=4)
print(dump)
f.write(dump)



