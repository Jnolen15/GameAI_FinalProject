
# Species Class
class species:
    # A Species Stats
    def __init__(self, attack, defense):
        self.attack = attack
        self.defense = defense

    # Print functions
    def __repr__(self):
        return "species()"
    def __str__(self):
        return "Stats: Attack:%s Defense:%s" % (self.attack, self.defense)

