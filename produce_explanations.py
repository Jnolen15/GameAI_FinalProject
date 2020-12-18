import random
def generate_explanation(species_change_map, world_map):
    explanation = 'The species evolved '

    for stat, changeList in species_change_map.items():
        if stat in world_map:

            evolutions = ''
            if len(changeList) > 2:
                evolutions = ', '.join(changeList[:-1]) + ' and ' + changeList[-1]
            elif len(changeList) == 2:
                evolutions = changeList[0] + ' and ' + changeList[1]
            elif len(changeList) == 1:
                evolutions = changeList[0]


            hazards = ''
            if len(world_map[stat]) > 2:
                hazards = ', '.join(world_map[stat][:-1]) + ' and ' + world_map[stat][-1]
            elif len(world_map[stat]) == 2:
                hazards = world_map[stat][0] + ' and ' + world_map[stat][1]
            elif len(world_map[stat]) == 1:
                hazards = world_map[stat][0]


            help_word = random.choice(['help it', 'strengthen its ability to', 'empower it to'])
            survive_word = random.choice(['cope with', 'survive', 'thrive amidst' ])
            explanation += '{} to {} {} the {}, '.format(evolutions, help_word, survive_word, hazards)

    return explanation