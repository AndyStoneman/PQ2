from operator import truediv
from Ingredient import Ingredient
import re
import glob

class Recipe:
    """
    Builds a recipe object from a recipe input file or list of ingredients, allows recipe manipulation.
    It holds a name, a list of ingredient objects, and a fitness based on the number of ingredients.

    Args:
        name (str): The name of the recipe. Defaulted to nothing, but if a file is specified it will use the name
        of the file.

        ingredient_list (Ingredient[]): List of ingredient objects that are a part of the recipe. Defaulted to nothing
        if file is used instead.

        filename (str): File containing a recipe and its ingredients. Defaulted to nothing incase list of ingredients
        is used instead.

    Methods
    -----
        get_fitness():
            returns fitness
        add_ingredient(ingredient):
            adds ingredient to recipe and its name to list of names
        remove_ingredient(ingredient):
            removes ingredient in recipe if present
        get_name()
            gets recipe name
        get_ingredient_names()
            get list of ingredient names associated with recipe
    """
    def __init__(self, name='', ingredient_list=[], filename=""):
        self.filename = filename
        self.ingredients = []
        self.ingredient_names = []
        if filename != "":
            self.filename_components = self.filename.split(".")
            self.name = self.filename_components[0][8:]#8 to allow for "recipes"
            with open(filename, 'r') as f:
                my_line = f.readline()
                #may need to convert from one line to 
                while my_line:
                    ingredient = self.parse_line_for_recipe(my_line)
            
                    self.ingredient_names.append(ingredient.get_name())
                    self.ingredients.append(ingredient)
                    my_line = f.readline()
        else:
            self.ingredients = ingredient_list
            for i in range(len(self.ingredients)):
                self.ingredient_names.append(self.ingredients[i].get_name())
            self.name = name
            
        self.fitness = len(self.ingredients)
    
    def parse_line_for_recipe(self, line):
        """
        Parses line input into ingredient obj
        Returns ingredient if parseable, None if empty string passed.
        Two modes, csv for csv formatted files and other for the way Andy did it.
        """

        ingredient = line.split(",")
        # format ingredient as name, amount, unit

        for i in range(len(ingredient)):
            ingredient[i] = ingredient[i].strip()
            ingredient[i] = ingredient[i].lower()

        #standardizing common ingredients that appear with different names
        if "flour" in ingredient[2]:
            ingredient[2] = "all-purpose flour" #for now we removed cake flour
        if ingredient[2] == "unsalted butter":
            ingredient[2] = "butter"
        if ingredient[2] == "pure vanilla extract":
            ingredient[2] = "vanilla extract"
        if ingredient[2] == "sugar":
            ingredient[2] = "granulated sugar"
        if ingredient[2] == "ground cinnamon":
            ingredient[2] = "cinnamon"
        if ingredient[2] == "ground nutmeg":
            ingredient[2] = "nutmeg"
        if "cocoa power" in ingredient[2]:
            ingredient[2] = "cocoa powder"


        # Ingredient standardization
        if ingredient[1] == "cups":
            ingredient[1] = "cup"
        if ingredient[1] == "teaspoon" or ingredient[1] == "teaspoons":
            ingredient[1] = "tsp"
        if ingredient[1] == "tablespoon" or ingredient[1] == "tablespoons":
            ingredient[1] = "tbsp"
        if ingredient[1] == "ounces":
            ingredient[1] = "oz"

        ingred_obj = Ingredient(str(ingredient[2]), float(ingredient[0]),
                                str(ingredient[1]))
        return ingred_obj

    def read_unique(self): 
        #Add this functionality, so we can read the CSV file in 
        return None
    def calculate_fitness(self):
        # determine variation of elements NOT in common set
        """
        Common set
        [('baking powder', 26), ('cinnamon', 29), ('vanilla extract', 50), \
            ('granulated sugar', 51), \
            ('baking soda', 53), ('salt', 54), ('egg', 55), ('butter', 60),\
                 ('all-purpose flour', 73)]
        """
        common_set_appearances = {}
        name_list = []
        #set up keys
        for k,v in [('baking powder', 26), ('cinnamon', 29), ('vanilla extract', 50), \
            ('granulated sugar', 51), \
            ('baking soda', 53), ('salt', 54), ('egg', 55), ('butter', 60),\
                 ('all-purpose flour', 73)]:
            common_set_appearances[k] = 0
            name_list.append(k)
        
        for k in common_set_appearances.keys():
            if k in self.get_ingredient_names():
                common_set_appearances[k] += 1
            
        print(common_set_appearances)
        
        #now, for the "optional"
        #we allow for either vanilla OR cinnamon to make recipe fit
        #also allow for either baking soda OR baking powder or both

        #method 2:
        requiredIngredients = sum(common_set_appearances.values())

        if requiredIngredients >= 6:
             hasRequiredIngredients = True
        else:
            hasRequiredIngredients = False
        """
        hasRequiredIngredients = True
        if not(common_set_appearances["vanilla extract"] >= 1 or \
            common_set_appearances["cinnamon"] >= 1): 
            hasRequiredIngredients = False
        if not(common_set_appearances["baking soda"] >= 1 or \
            common_set_appearances["baking powder"] >= 1):
            hasRequiredIngredients = False
        """

        fitness = 0
        #now, for ingredient not in ingredients required core, give point
        for ingredient in self.get_ingredient_names():
            if ingredient not in common_set_appearances.keys():
                fitness += 1
      
        if hasRequiredIngredients:
            return fitness
        else:
            return 0
        

    
    def get_fitness(self):
        """
        A getter method for fitness of a recipe

        Returns:
            Fitness of recipe.
        """
        return self.fitness

    def add_ingredient(self, ingredient):
        """
        Adds an ingredient to the ingredients list if not present.

        Args:
            ingredient (Ingredient): The ingredient object that is being added to the recipe.

        Returns:
            True if added.

            False if not added because of duplicate.
        """
        if ingredient.get_name() not in self.ingredient_names:
            self.ingredients.append(ingredient)
            self.ingredient_names.append(ingredient.get_name())
            return True
        return False

    def remove_ingredient(self, ingredient):
        """
        Removes an ingredient from the ingredients list if present.

        Args:
            ingredient (Ingredient): The ingredient that is being removed from the recipe.

        Returns:
            True if removed.

            False if ingredient isn't in recipe.
        """
        if ingredient.get_name() in self.ingredient_names:
            self.ingredients.remove(ingredient)
            self.ingredient_names.remove(ingredient.get_name())
            return True

        return False

    def get_name(self):
        """
        Getter method for the name of a recipe.

        Returns:
            The recipe name.
        """
        return self.name

    def get_ingredient_names(self):
        """
        Getter method for the list of ingredient names.

        Returns:
            List of ingredient names.
        """
        return self.ingredient_names

    def __str__(self):
        """Returns a string representation of the ingredient."""
        return self.name + ": " + str(self.ingredients)

    def __repr__(self):
        """Returns a blueprint for a Recipe object."""
        return "Recipe('{0}', {1}, {2})\n".format(self.name, self.ingredients, self.filename)

# FOR TESTING (commented out)
    
#r = Recipe("gingerbread cookies", [],"recipes/Gingerbread Cookies1.txt")
#r2 = Recipe("Wyoming cowboy cookies", [], "recipes/Wyoming Cowboy Cookies3.txt")
#print(r)
#print(r2)

