import random


def generate_starter_world_explanation(world_map):
    explanation = 'The world is a landscape dominated by '
    all_changes = []
    for stat, change_list in world_map.items():
        all_changes.extend(change_list)
    all_changes = list(set(all_changes))

    if len(all_changes) == 1:
        explanation += all_changes[0]
    elif len(all_changes) == 2:
        explanation += all_changes[0] + ' and ' + all_changes[1]
    else:
        explanation += ', '.join(all_changes[:-1]) + ' and ' + all_changes[-1]

    return explanation



def generate_explanation(species_change_map, world_map):
    explanation = 'The species evolved '

    i = 0

    matches = [item for item in species_change_map.items() if item[0] in world_map]

    length = len(matches)
    for stat, changeList in matches:
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

            if i == length - 1:
                explanation += ' and '

            explanation += '{} to {} {} the {}'.format(evolutions, help_word, survive_word, hazards)

            if i < length - 1:
                explanation += ', \n'
            i += 1

    return explanation