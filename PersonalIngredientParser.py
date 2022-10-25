from Ingredient import Ingredient
"""
PersonalIngredientParser was used to parse a csv of personal ingredients and 
their respective ratings. After originally parsing the file, 
PersonalIngredientParser is not used. It is merely included for the sake of 
understanding our generation process. It could be used by future users
to generate their own personal ingredient lists, although the resulting file 
will have to be replaced in the Genetic Algorithm code.
"""

class PersonalIngredientParser:
    def __init__(self, filename):
        """
        Creates group ingredient object. 
        Seperate from the Ingredient class because we wanted to add the "score" parameter.   
        """
        self.filename = filename
        self.ingredients = []
        self.ingredient_names = []

        self.filename_components = self.filename.split(".")
        self.name = self.filename_components[0][8:]  # 8 to allow for "recipes"
        with open(filename, 'r') as f:
            f.readline()  # To skip first csv line
            my_line = f.readline()
            while my_line:
                ingredient = self.parse_line(my_line)
                if ingredient != None:
                    self.ingredient_names.append(ingredient.get_name())
                    self.ingredients.append(ingredient)
                my_line = f.readline()

    def parse_line(self, line):
        """
        Parses line input into group_ingredients obj
        Returns ingredient if parseable, None if empty string passed.
        """

        ingredient = line.split(",")
        # format ingredient as name, amount, unit
        for i in range(len(ingredient)):
            ingredient[i] = ingredient[i].strip()
            ingredient[i] = ingredient[i].lower()

        # amount, unit, name, score
        # 0, 1, 2, 3
        ingred_obj = Ingredient(str(ingredient[2]), float(ingredient[0]),
                                str(ingredient[1]), float(ingredient[3]))
        return ingred_obj

    def get_name(self):
        """
        Getter method for the name of a personal ingredient.

        Returns:
            The recipe name.
        """
        return self.name

    def __str__(self):
        """Returns a string representation of the ingredient."""
        return self.name + ": " + str(self.ingredients)

    def __repr__(self):
        """Returns a blueprint for a Recipe object."""
        return "PersonalIngredientParser('{0}', {1}, '{2}', {3})\n".format(self.name,
                                                                   self.amount,
                                                                   self.unit,
                                                                   self.score)
