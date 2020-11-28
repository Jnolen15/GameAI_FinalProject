import random

# Species Class
class species:
    # A Species Stats
    def __init__(self, offense=0, defense=0, heatRes=0, \
                coldRes=0, social=0, size=0, diet=0, swim=0, walk=0, fly=0, name="", meaning=""):
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

        # Name
        self.name = name
        self.meaning = meaning
        if self.name == "" or self.meaning == "":
            nameTuple = nameSelect()
            self.name = nameTuple[0]
            self.meaning = nameTuple[1]

    # Print functions
    def __repr__(self):
        return "species()"
    def __str__(self):
        
        # Size
        sizeType = "ERROR"
        if self.size >= 0 and self.size <= 19:
            sizeType = "Tiny"
        elif self.size >= 20 and self.size <= 39:
            sizeType = "Small"
        elif self.size >= 40 and self.size <= 59:
            sizeType = "Medium"
        elif self.size >= 60 and self.size <= 79:
            sizeType = "large"
        elif self.size >= 80 and self.size <= 99:
            sizeType = "Huge"

        # Diet
        dietType = "ERROR"
        if self.diet >= 70:
            dietType = "Carnivore"
        elif self.diet >= 30 and self.diet <= 69:
            dietType = "Omnivore"
        elif self.diet <= 29:
            dietType = "Herbavore"

        # Movement 
        moveTypes = []
        if self.swim > 50:
            moveTypes.append("Swim")
        if self.walk > 50:
            moveTypes.append("Walk")
        if self.fly > 50:
            moveTypes.append("Fly")

        return "\n~~~~~Stats~~~~~ \nName: %s \nMeaning: %s \nOffense: %s \nDefense: %s \
                \nHeatRes: %s \nColdRes: %s \nSocial: %s \nSize: %s \nDiet: %s \
                \nMovement: %s" \
                % (self.name, self.meaning, self.offense, self.defense, self.heatRes, \
                self.coldRes, self.social, sizeType, dietType, moveTypes)

def nameSelect():
    # Dictionary of roots + meanings
    prefix = {
        "elasmo" : "metal plated",
        "thallasso" : "sea",
        "archaeo" : "ancient",
        "micro" : "small",
    }
    
    suffix = {
        "tops" : "face",
        "saur" : "lizard",
        "dactyl" : "reptile",
        "rex" : "king",
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