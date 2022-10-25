from Ingredient import Ingredient
import pickle

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
                    if ingredient:
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
        Parses line input into ingredient object.

        Args:
            line (str): An ingredient in a line of a recipe file.
        Returns:
            Ingredient object with information from the specified line, and
            None if the string is empty.
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

    def calculate_fitness(self, avg_recipe_length, common_list):
        """
        Calculates and rewards recipes that have 6 core ingredients, personal
        ingredients that have high scores, and are under the threshold value
        which represents the average number of ingredients per recipe.

        Args:
            avg_recipe_length (int): Average number of ingredients per recipe
            from our inspiring set.

            common_list (list): List of common set ingredients given by GA.
        """
        
        common_set_appearances = 0
        common_dict = ['baking soda', 'baking powder', 'vanilla extract',
                       'sugar', 'salt', 'egg', 'butter', 'all-purpose flour']

        for i in common_list:
            if i in self.get_ingredient_names():
                common_set_appearances += 1

        required_ingredients = common_set_appearances / (len(common_list))
        file = "personalIngredientsList.pickle"

        special_count = 0
        with open(file, "rb") as f:
            personal = pickle.load(f)  # Load personal ingredient object
            for ing in personal.ingredients:
                if ing.get_name() in self.get_ingredient_names():
                    special_count += ing.score  # Reward the polarizing

        difference = abs(len(self.ingredients) - avg_recipe_length)
        self.fitness = (1 + special_count * required_ingredients) * \
                       (1 / difference)

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
