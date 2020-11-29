import random
import numpy as np
species_attributes = ['offense', 'defense', 'heatRes', 'coldRes', 'social', 'size', 'diet', 'swim', 'walk', 'fly']

# Species Class
class evolution_increment:
    # A Species Stats
    def __init__():
      self.stats = {}


def get_evolution_increment_set(num_increments):
  evolution_increments = []

  def clipped_normal(mean, variance, minimum, maximum):
    return min(max(random.normalvariate(mean, variance ** 0.5), minimum), maximum)

  for i in range(num_increments):
    evolution_increment = {}
    num_attr = random.choice([1, 2, 3])
    evolution_attributes = random.choices(species_attributes, k=num_attr)

    for evolution_attribute in evolution_attributes:
      evolution_increment[evolution_attribute] = clipped_normal(mean=0, variance=5, minimum=-100, maximum=100)

    evolution_increments.append(evolution_increment)

  return evolution_increments







