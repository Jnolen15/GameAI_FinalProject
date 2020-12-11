import random
import uuid
import copy

# Species Class
class species:
    # A Species Stats
    def __init__(self, offense=0, defense=0, heatRes=0, \
                coldRes=0, social=0, size=0, diet=0, swim=0, walk=0, fly=0, name="", meaning=""):
        # BASIC STATS
        # Lowest stat score = 0, highest = 99

        self.id = uuid.uuid4()
        # Should be set whenever generating children (see generate_children in ga_v2)
        self.parent_ids = [None, None]
        self.stats = {}
        self.saved_fitness = None



        self.stats['offense'] = offense
        self.stats['defense'] = defense
        self.stats['heatRes'] = heatRes
        self.stats['coldRes'] = coldRes
        self.stats['social'] = social
        # OTHER STATS
        # SIZE: (in increments of 20) tiny -> small -> medium -> large -> huge
        self.stats['size'] = size
        # DIET: 0-29: Herbavore 30-69: Omnivore 70-99: Carnivore
        self.stats['diet'] = diet
        # MOVEMENT: If a stat is above 50 then they can do it
        self.stats['swim'] = swim
        self.stats['walk'] = walk
        self.stats['fly'] = fly

        # This only stays if the creature's genome is basically a "list" of evolution increments
        self.evolutions = []

        # Name
        self.name = name
        self.meaning = meaning
        if self.name == "" or self.meaning == "":
            nameTuple = nameSelect()
            self.name = nameTuple[0]
            self.meaning = nameTuple[1]

    def add_increment(self, evolution_increment):
      self.evolutions.append(evolution_increment)
      for (attribute, adjustment) in evolution_increment.items():
        self.stats[attribute] += adjustment

    def print_increments(self):
      return (', '.join(['{{ {} }}'.format(', '.join(['{}: {:.2f}'.format(attr[:3], quant) for (attr, quant) in evolution.items()]))
                       for evolution in self.evolutions]))

    # Used to store the fitness relative to what the world looked like when the given individual
    # was born.
    def set_saved_fitness(self, world):
        self.saved_fitness = self.calc_fitness(world)

    def calc_fitness(self, world):
        penalty = 0
        attributes = self.stats.keys()
        for attribute in attributes:
          penalty += (self.stats[attribute] - world.stats[attribute])

        return penalty

    def mutate(self):

        # Mutation probability
        if random.random() > 0.3:
            return

        # Redistribution way
        # Either increases one stat and slightly decreases another
        # or randomly decreases one stat
        # or randomly Increases one stat
        stats = list(self.stats.keys())
        stat_to_change = random.choice(stats)
        another_stat_to_change = random.choice(stats)
        while another_stat_to_change == stat_to_change:
            another_stat_to_change = random.choice(stats)
        choice = random.random()
        if choice > 0.5: # Buff one nerf another
            self.stats[stat_to_change] += random.choice(range(6, 12))
            self.stats[another_stat_to_change] -= random.choice(range(2, 10))
        elif choice <= 0.5 and choice > 0.1: # Nerf one
            self.stats[stat_to_change] -= random.choice(range(2, 10))
        elif choice <= 0.1: # Buff one
            self.stats[stat_to_change] += random.choice(range(6, 12))

        # Making sure stats are between 0 and 99
        for stat in self.stats:
            if self.stats[stat] < 0:
                self.stats[stat] = 0
            elif self.stats[stat] > 99:
                self.stats[stat] = 99

        # Random few stats are changed way
        """
        max_stats_that_can_change = 3
        change_range = 4

        stats = list(self.stats.keys())
        num_stats_to_change = random.choice(range(1, max_stats_that_can_change + 1))
        stats_to_change = random.choices(stats, k=num_stats_to_change)

        for stat_to_change in stats_to_change:
            # Random negative or positive change
            self.stats[stat_to_change] += random.choice(range(-change_range, change_range + 1))
        """

    # Print functions
    def __repr__(self):
        return "species()"
    def __str__(self):

        # Size
        sizeType = "ERROR"
        if self.stats['size'] >= 0 and self.stats['size'] <= 19:
            sizeType = "Tiny"
        elif self.stats['size'] >= 20 and self.stats['size'] <= 39:
            sizeType = "Small"
        elif self.stats['size'] >= 40 and self.stats['size'] <= 59:
            sizeType = "Medium"
        elif self.stats['size'] >= 60 and self.stats['size'] <= 79:
            sizeType = "large"
        elif self.stats['size'] >= 80 and self.stats['size'] <= 99:
            sizeType = "Huge"

        # Diet
        dietType = "ERROR"
        if self.stats['diet'] >= 70:
            dietType = "Carnivore"
        elif self.stats['diet'] >= 30 and self.stats['diet'] <= 69:
            dietType = "Omnivore"
        elif self.stats['diet'] <= 29:
            dietType = "Herbavore"

        # Movement
        moveTypes = []
        if self.stats['swim'] > 50:
            moveTypes.append("Swim")
        if self.stats['walk'] > 50:
            moveTypes.append("Walk")
        if self.stats['fly'] > 50:
            moveTypes.append("Fly")

        return "\n~~~~~Stats~~~~~ \nName: %s \nMeaning: %s \nOffense: %s \nDefense: %s \
                \nHeatRes: %s \nColdRes: %s \nSocial: %s \nSize: %s \nDiet: %s \
                \nMovement: %s" \
                % (self.name, self.meaning, self.stats['offense'], self.stats['defense'], self.stats['heatRes'], \
                self.stats['coldRes'], self.stats['social'], sizeType, dietType, moveTypes)
                
    # Copy function
    import copy # put this at the top  
    def copy(self):
        return copy.deepcopy(self)

    # Comparison function
    def __gt__(self, other):
        return self.saved_fitness > other.saved_fitness
    def __lt__(self, other):
        return self.saved_fitness < other.saved_fitness
    def __eq__(self, other):
        return self.saved_fitness == other.saved_fitness

    #Copied from p5 to allow for stuff
    def __key(self):
        return tuple(self.stats.items())

    def __hash__(self):
        return hash(self.__key())

def nameSelect():
    # Dictionary of roots + meanings
    prefix = {
        "stegos" : "plated",
        "thallasso" : "sea",
        "archaeo" : "ancient",
        "micro" : "small",
        "brachio" : "arm",
        "bronte" : "thunder",
        "di" : "two",
        "deino" : "terrible",
        "gravis" : "heavy",
        "frigo" : "cold",
        "glyco" : "sweet",
        "makros" : "long",
        "megalo" : "large",
        "saltus" : "leaping",
        "teratos" : "monster",
        "tri" : "three",
    }

    suffix = {
        "tops" : "face",
        "saur" : "lizard",
        "dactyl" : "reptile",
        "rex" : "king",
        "ceratops" : "horned face",
        "dipus" : "two-footed",
        "gnathus" : "jaw",
        "mimus" : "imitator",
        "nychus" : "claw",
        "ops" : "face",
        "odon" : "teeth",
        "pus" : "foot",
        "raptor" : "theif",
        "rhinos" : "nose",
        "venator" : "hunter",
    }
    randName = ""
    nameDef = ""
    # Choosing Prefix
    pre = random.choice(list(prefix.keys()))
    randName += pre
    nameDef += prefix.get(pre) + " "
    # Choosing Suffix
    suf = random.choice(list(suffix.keys()))
    randName += suf
    nameDef += suffix.get(suf)
    #for i in range(2):
    #    root = random.choice(list(roots.keys()))
    #    randName += root
    #    nameDef += roots.get(root) + " "
    return (randName, nameDef)