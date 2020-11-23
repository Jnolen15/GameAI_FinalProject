
# Species Class
class species:
    # A Species Stats
    def __init__(self, offense=0, defense=0, heatRes=0, \
                coldRes=0, social=0, size=0, diet=0, swim=0, walk=0, fly=0):
        # BASIC STATS
        # Lowest stat score = 0, highest = 99
        self.offense = offense
        self.defense = defense
        self.heatRes = heatRes
        self.coldRes = coldRes
        self.social = social
        # OTHER STATS
        # SIZE: (in increments of 20) tiny -> small -> medium -> large -> huge
        self.size = size
        # DIET: 0-29: Herbavore 30-69: Omnivore 70-99: Carnivore
        self.diet = diet
        # MOVEMENT: If a stat is above 50 then they can do it
        self.swim = swim
        self.walk = walk
        self.fly = fly

    # Print functions
    def __repr__(self):
        return "species()"
    def __str__(self):
        
        # Size
        if self.size >= 0 and self.size <= 19:
            sizeType = "Tiny"
        if self.size >= 20 and self.size <= 39:
            sizeType = "Small"
        if self.size >= 40 and self.size <= 59:
            sizeType = "Medium"
        if self.size >= 60 and self.size <= 79:
            sizeType = "large"
        if self.size >= 80 and self.size <= 99:
            sizeType = "Huge"

        # Diet
        if self.diet >= 70:
            dietType = "Carnivore"
        if self.diet >= 30 and self.diet <= 69:
            dietType = "Omnivore"
        if self.diet <= 29:
            dietType = "Herbavore"

        # Movement 
        moveTypes = []
        if self.swim > 50:
            moveTypes.append("Swim")
        if self.walk > 50:
            moveTypes.append("Walk")
        if self.fly > 50:
            moveTypes.append("Fly")

        return "\n~~~~~Stats~~~~~ \nOffense: %s \nDefense: %s \
                \nHeatRes: %s \nColdRes: %s \nSocial: %s \nSize: %s \nDiet: %s \
                \nMovement: %s" \
                % (self.offense, self.defense, self.heatRes, \
                self.coldRes, self.social, sizeType, dietType, moveTypes)

