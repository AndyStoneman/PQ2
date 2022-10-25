"""
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
        has_score = hasattr(self, 'score')
        add_to_repr = 1
        if has_score:
            add_to_repr = self.score
        return "Ingredient('{0}', {1}, '{2}', {3})\n".format(self.name,
                                                             self.amount,
                                                             self.unit,
                                                             add_to_repr)

    def set_amount(self, new_amount):
        """Setter method for the amount of an ingredient."""
        self.amount = new_amount

    def get_amount(self):
        """
        Getter method for the amount of an ingredient.

        Returns:
            Amount of an ingredient.
        """
        return self.amount
    
    def set_name(self, name):
        """Setter method for the name of an ingredient."""
        self.name = name
    
    def get_name(self):
        """
        Getter method for the name of an ingredient.

        Returns:
            Name of an ingredient. 
        """
        return self.name
    
    def get_unit(self):
        """
        Getter method for the units of an ingredient amount.
        
        Returns:
            The unit of an ingredient.
        """
        return self.unit
    
    def get_score(self):
        """
        Getter method for the score corresponding to an ingredient.
        
        Returns:
            The score assigned to an ingredient. 
        """
        return self.score
    
    def set_score(self,score):
         """Setter method for the score of an ingredient."""
         self.score = score


