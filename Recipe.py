from Ingredient import Ingredient


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
            f = open(filename, 'r')
            my_line = f.readline()
            #may need to convert from one line to 
            while my_line:
                #add a call to a separate function to parse recipes ingredients
                #split by ' ', from the array stuff 
                ingredient_line = my_line.split(" oz ")
                ingredient_object = Ingredient(ingredient_line[1].strip(), float(ingredient_line[0].strip()))
                self.ingredient_names.append(ingredient_line[1].strip())
                self.ingredients.append(ingredient_object)
                my_line = f.readline()
            f.close()
        else:
            self.ingredients = ingredient_list
            for i in range(len(self.ingredients)):
                self.ingredient_names.append(self.ingredients[i].get_name())
            self.name = name
            
        self.fitness = len(self.ingredients)
    
    def parse_file_for_recipe(line):
        """
        Parses line input into recipe 
        """
        #remove [] from list
        line = line[1:len(line)-1]
        ing_list = line.split('\',')
        for i in range(len(ing_list)):
            ing_list[i] = ing_list[i][1:]
        print(ing_list)
        

    
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
