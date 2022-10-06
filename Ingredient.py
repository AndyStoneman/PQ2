#For ingredients, we may want to add a "Unit" property 
#I have gone ahead and done so 
"""
Authors: Abby, Amanda 

Creates an Ingredient class with name, amount, and unit properties.
"""
class Ingredient:
    def __init__(self, name, amount, unit, score=1):
        """
        Construct an ingredient
        """
        self.name = name
        self.amount = amount
        self.unit = unit
        self.score = score

    def __str__(self):
        """Returns a string representation of the ingredient."""
        return self.name + ": " + str(self.amount)

    def __repr__(self):
        """Lets us make an object of the same value."""
        return "Ingredient('{0}', {1}, '{2}', {3})\n".format(self.name, self.amount,
        self.unit, self.score)

    def set_amount(self, new_amount):
        self.amount = new_amount

    def get_amount(self):
        return self.amount
    
    def set_name(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
    
    def get_unit(self):
        return self.unit
    
    def get_score(self):
        return self.score
