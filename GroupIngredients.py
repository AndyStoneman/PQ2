from Ingredient import Ingredient 

class GroupIngredients:
    def __init__(self, filename):
        self.filename = filename
        self.ingredients = []
        self.ingredient_names = []
        
        self.filename_components = self.filename.split(".")
        self.name = self.filename_components[0][8:]#8 to allow for "recipes"
        with open(filename, 'r') as f:
            my_line = f.readline()
            my_line = f.readline() #to skip first csv line
            #may need to convert from one line to 
            while my_line:
                ingredient = self.parse_line(my_line)
                if ingredient != None:
                    self.ingredient_names.append(ingredient.get_name())
                    self.ingredients.append(ingredient)
                my_line = f.readline()
            
            
    def parse_line(self, line):
        """
        Parses line input into Groupingredients obj
        Returns ingredient if parseable, None if empty string passed.
        """
        
        ingredient = line.split(",")
        # format ingredient as name, amount, unit

        for i in range(len(ingredient)):
            ingredient[i] = ingredient[i].strip()
            ingredient[i] = ingredient[i].lower()

        # amount, unit, name, score
        #0, 1, 2, 3,
        # def __init__(self, name, amount, unit, score=1):
        ingred_obj = Ingredient(str(ingredient[2]), float(ingredient[0]),
                                str(ingredient[1]), float(ingredient[3]))
        
        return ingred_obj
    
    def get_name(self):
        return self.name
    def __str__(self):
        """Returns a string representation of the ingredient."""
        return self.name + ": " + str(self.ingredients)

    def __repr__(self):
        """Returns a blueprint for a Recipe object."""
        return "GroupIngredients('{0}', {1}, '{2}', {3})\n".format(self.name, self.amount,
        self.unit, self.score)
        