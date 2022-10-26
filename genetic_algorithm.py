import glob
import random
from Recipe import Recipe
from Ingredient import Ingredient
from personal_ingredient_parser import PersonalIngredientParser
import pickle


class GeneticAlgorithm:
    """
    Class that runs through the genetic algorithm process for soup recipes.
    Includes selection, recombination, and
    mutation.

    Args:
        iterations (int): The number of iterations that the GA should run.

        input_recipes (Recipe[]): A list of recipe objects that are used as a
        starting initial population for the GA.
    
    Methods:
        run
            Synthesizes GA process including selection, recombination,
            mutation. Gives printed information about each iteration.
        selection()
            Selects twice number of recipes of initial set proportionally by
            fitness

        recombination(selected_recipes)
            Recombines the recipes that have been selected to form a child
            offspring

        check_fix_duplicates_recombination(first_half, second_half):
            Helper method that removes duplicate ingredients during
            recombination process
        
        4 different mutation sub methods to change: ingredient name, ingredient
        amount, add or remove ingredient (each takes a recipe argument)

        normalize_ingredient_quantities(recipe, amt=100.0):
            normalizes quantities in the ingredient to 100oz
    """

    def __init__(self, iterations, input_recipes):
        self.positive_mutations = 0
        self.iterations = iterations
        self.recipes = []
        self.inspiring_set_ingredient_names = set()
        # allow for passing null [] recipe list to create inspiring set
        self.average_recipe_length = 0
        self.num_files = 0
        for filename in glob.glob(input_recipes):
            recipe = Recipe(filename=filename)
            if recipe:
                self.recipes.append(recipe)
                self.inspiring_set_ingredient_names.update(
                    recipe.get_ingredient_names())
                self.average_recipe_length += len(
                    recipe.get_ingredient_names())
                self.num_files += 1
        self.inspiring_set_ingredient_length = len(
            list(self.inspiring_set_ingredient_names))
        self.average_recipe_length /= self.num_files
        self.common_list = self.create_common_list()
        self.inspiring_items = list(
            self.create_inspiring_set_ingredients().values())

    def generate_random(self):
        return random.choice(self.recipes)

    def run(self):
        """
        The method that controls the entire overview of the GA process, running
        it the iterations of selection, recombination, and mutation, as well as
        printing useful information at the end of each iteration.
        """
        num_iteration = 0
        num_mutations = 0
        # Start iterations
        while num_iteration < self.iterations:
            for recipe in self.recipes:
                recipe.calculate_fitness(self.average_recipe_length,
                                         self.common_list)
            original_list = self.recipes
            self.selection()
            self.recombination(self.recipes)
            # Mutation
            for rec in self.recipes:
                old_fitness = rec.get_fitness()
                probability = random.randint(0, 100)
                if probability < 80:
                    mutation_choice = random.randint(1, 3)
                    num_mutations += 1
                    if mutation_choice == 1:
                        self.mutate_ingredient_name(rec)
                    elif mutation_choice == 2:
                        self.mutate_add_recipe_ingredient(rec)
                    elif mutation_choice == 3:
                        self.mutate_remove_recipe_ingredient(rec)

                    rec.calculate_fitness(self.average_recipe_length,
                                          self.common_list)

                    # Count positive mutations
                    new_fitness = rec.get_fitness()
                    if old_fitness < new_fitness:
                        self.positive_mutations += 1

                rec.calculate_fitness(self.average_recipe_length,
                                      self.common_list)

            # Combining top 50% of new and original recipes
            self.recipes.sort(key=lambda x: x.fitness)
            original_list.sort(key=lambda x: x.fitness)
            new_generation = self.recipes[(len(self.recipes) // 2):] + \
                             original_list[(len(original_list) // 2):]
            self.recipes = new_generation
            # Iteration print statements
            self.recipes.sort(key=lambda x: x.fitness)
            self.recipes = new_generation
            print("ITERATION: " + str(num_iteration + 1) +
                  "\nFittest recipe:\nName: " + str(self.recipes[-1].get_name()
                                                    ) +
                  "\nFitness: " + str(self.recipes[-1].get_fitness()))
            print(self.recipes[-1])
            num_iteration += 1
        self.positive_mutations /= num_mutations

    def create_common_list(self):
        """
        Used to create our list of common ingredients, which because of its
        length of 9, we have saved as constant variables elsewhere.
        """
        ingredient_amounts = {}
        for recipe in self.recipes:
            ingredients = recipe.get_ingredient_names()
            for ingredient in ingredients:
                ingredient_amounts[ingredient] = ingredient_amounts. \
                                                     get(ingredient, 0) + 1
        common_dict = sorted(ingredient_amounts.items(),
                             key=lambda item: item[1])[-9:]
        common_list = []
        for k, v in common_dict:
            common_list.append(k)
        # Remove cinnamon–we don't consider it as common ingredient
        common_list.remove("cinnamon")
        return common_list

    def create_inspiring_set_ingredients(self):
        """
        Creates a list of ingredients from the inspiring set that were
        not identified as "common set" ingredients, to be used in 
        mutation.
        Returns a list of 'non-core' ingredients.
        """
        non_core_ingredients = {}
        for rec in self.recipes:
            for ingredient in rec.ingredients:
                name = ingredient.get_name()
                if name not in self.common_list:
                    if name not in non_core_ingredients:
                        non_core_ingredients[name] = [ingredient]
                    elif name in non_core_ingredients:
                        non_core_ingredients[name].append(ingredient)

        delete_list = []
        for item in non_core_ingredients.items():
            # filtering: remove any ingredient with only 1 appearance to get
            # rid of some typos
            if len(item[1]) <= 1:
                delete_list.append(item[0])
            if len(item[1]) > 1:  # second part of tuple
                new_item = self.regulate_inspiring_ingredient(item[0], item[1])
                non_core_ingredients[item[0]] = new_item

        manual_keys = ["water", "eggs", "salted butter",
                       'semisweet chocolate chips',
                       'semi-sweet chocolate chips']
        for key in manual_keys:
            if key in non_core_ingredients:
                del non_core_ingredients[key]

        for key in non_core_ingredients.keys():
            if "sugar" in key or "salt" in key:
                delete_list.append(key)

        for key in delete_list:
            if key in non_core_ingredients:
                del non_core_ingredients[key]

        # change names and scores if it matches personal ingredient list item
        if "milk" in non_core_ingredients:
            non_core_ingredients["non fat milk"] = non_core_ingredients["milk"]
            non_core_ingredients["non fat milk"].set_score(3)
            del non_core_ingredients["milk"]
        # tragically this needs to match our typo

        if "cocoa powder" in non_core_ingredients and \
                "unsweetened cocoa powder" in non_core_ingredients:
            non_core_ingredients["unsweetened coco powder"] = \
                non_core_ingredients["cocoa powder"]
            non_core_ingredients["unsweetened coco powder"].set_score(4)
            del non_core_ingredients["cocoa powder"]
            del non_core_ingredients["unsweetened cocoa powder"]

        if "maple flavoring" in non_core_ingredients:
            non_core_ingredients["maple extract"] = non_core_ingredients[
                "maple flavoring"]
            non_core_ingredients["maple extract"].set_score(2)

        if "nutmeg" in non_core_ingredients:
            non_core_ingredients["nutmeg"].set_score(4)

        return non_core_ingredients

    def regulate_inspiring_ingredient(self, ing_name, ingredient_list):
        """
        Given an ingredient name and list of ingredients with same name
        and possibly different quantities, finds most common unit and averages
        the quantities of that unit used to create one "average occurence"
        of an ingredient.

        Param: ing_name is string of ingredient name
        param: ingredient_list is the list of the ingredients objects
        Returns a list of len 1 with the average ingredient inside
        """
        units = {}
        for ing in ingredient_list:
            unit = ing.get_unit()
            amount = ing.get_amount()
            if unit not in units:
                units[unit] = [amount]
            else:
                units[unit].append(amount)
        max_key = max(units, key=lambda x: len(units[x]))
        avg_amount = sum(units[max_key]) / len(units[max_key])

        # max key code inspired by:
        # https://stackoverflow.com/questions/21839208/dictionary-with-lists-
        # as-values-find-longest-list
        # name, amt, unit, score

        # Do a check for ingredients that overlap with personal set to
        # adjust score
        ingred = Ingredient(ing_name, avg_amount, max_key, 1)
        return ingred

    def selection(self):
        """
        Runs the selection process, where twice the number of recipes in the
        initial population are selected proportionally to their fitness.
        """
        selected_recipes = []
        total = 0
        for j in range(len(self.recipes)):
            total += int(self.recipes[j].get_fitness())

        self.recipes.sort(key=lambda x: x.fitness)
        for i in range(2 * len(self.recipes)):
            count = 0
            random_number = random.randint(0, total)
            for z in range(len(self.recipes)):
                count += self.recipes[z].get_fitness()
                if random_number <= count:
                    selected_recipes.append(self.recipes[z])
                    break
        self.recipes = selected_recipes

    def recombination(self, selected_recipes):
        """
        The selected recipes are recombined through single point crossover to
        form one child. At the completion of selection we are left with just
        one child per two parents.

        Args:
            selected_recipes (Recipe[]): A list of the recipes produced by
            selection, which is double the size of the initial population.
        """
        new_recipes = []
        for i in range(0, len(selected_recipes), 2):
            if selected_recipes[i].get_fitness() < \
                    selected_recipes[i + 1].get_fitness():
                random_index = random.randint(0, int(
                    selected_recipes[i].get_fitness()))
            else:
                random_index = random.randint(0, int(
                    selected_recipes[i + 1].get_fitness()))
            first_half = selected_recipes[i].ingredients[0:random_index]
            second_half = selected_recipes[i + 1].ingredients[random_index:]
            combined_list = self.check_fix_duplicates_recombination(first_half,
                                                                    second_half
                                                                    )
            new_recipe = Recipe(name="new_recipe_" + str(i // 2),
                                ingredient_list=combined_list)
            new_recipes.append(new_recipe)
        self.recipes = new_recipes

    def check_fix_duplicates_recombination(self, first_half, second_half):
        """
        Helper method used to prevent duplicates during recombination. Does
        this by using a double loop that checks for duplicates, and if one is
        found, it just removes one of them.

        Args:
            first_half (Recipe[]): The first half of one of the parent
            candidates.

            second_half (Recipe[]): The second half of one of the parent
            candidates.

        Returns:
            The two lists (first_half and second_half) combined with no
            duplicates.
        """
        for x in range(len(first_half)):
            y = 0
            while y < len(second_half):
                if first_half[x].get_name() == second_half[y].get_name():
                    new_amount = first_half[x].get_amount()
                    first_half[x].set_amount(new_amount)
                    second_half.remove(second_half[y])
                else:
                    y += 1
        return first_half + second_half

    def mutate_ingredient_name(self, recipe):
        """
        Change of one ingredient to another: an ingredient is selected
        uniformly at random from the recipe. Its name is changed to that of
        another ingredient that is chosen at random from the ones we know in
        the inspiring set.

        Args:
             recipe (Recipe): The recipe that is having one of its ingredients
             mutated.
        
        """
        personal_items = self.load_recipe_list_from_file(
            "personal_ingredients_list.pickle")

        all_items = personal_items.ingredients

        for it in self.inspiring_items:
            all_items.append(it)
        new_ingredient = random.choice(all_items)
        ingredient_to_remove = random.choice(recipe.ingredients)

        count = 0
        while ingredient_to_remove.get_name() in self.common_list and \
                count == 8:
            ingredient_to_remove = random.choice(recipe.ingredients)
            if ingredient_to_remove.get_name() not in self.common_list:
                recipe.remove_ingredient(ingredient_to_remove)
                break
            else:
                ingredient_to_remove = random.choice(recipe.ingredients)
            count += 1

        while not recipe.add_ingredient(new_ingredient):
            new_ingredient = random.choice(all_items)


    def mutate_add_recipe_ingredient(self, recipe, threshold=16):
        """
        Mutation that adds an ingredient from the inspiring set.

        Args:
             recipe (Recipe): The recipe that is having one of its
             ingredients mutated.

             threshold (int): Ensures recipe doesn't have to many
             ingredients.
        """
        personal_items = self.load_recipe_list_from_file(
            "personal_ingredients_list.pickle")


        all_items = personal_items.ingredients

        for it in self.inspiring_items:
            all_items.append(it)

        new_ingredient = random.choice(all_items)

        if len(recipe.ingredients) + 1 <= threshold:
            while not recipe.add_ingredient(new_ingredient):
                new_ingredient = random.choice(all_items)

    def mutate_remove_recipe_ingredient(self, recipe):
        """
        Mutation that removes an ingredient from the recipe.

        Args:
             recipe (Recipe): The recipe that is having one of its ingredients
             mutated.
        """

        del_ingredient = random.choice(recipe.ingredients)
        while del_ingredient.get_name() in self.common_list:
            del_ingredient = random.choice(recipe.ingredients)

        recipe.remove_ingredient(del_ingredient)

    def save_recipe_to_file(self, recipe_list, file):
        """
        Saves a list of recipes to a file (allows us to save inspiring set)
        Inspired by https://stackoverflow.com/questions/20716812/saving-and-
        loading-multiple-objects-in-pickle-file

        param recipe_list: list of Ingredient objects that make the "recipe"
        param file: file where it gets saved to 


        An example of how this code was run:
        personalIngredients = \
            PersonalIngredientParser("personalIngredients.csv")
        ga.save_recipe_to_file(personalIngredients, \
            "personal_ingredients_list.pickle" )
        """
        with open(file, 'wb') as f:
            pickle.dump(recipe_list, f)

    def load_recipe_list_from_file(self, filename):
        """
        Loads a recipe list from file using pickle.
        Also inspired by https://stackoverflow.com/questions/20716812/saving-
        and-loading-multiple-objects-in-pickle-file.

        param filename: file to be opened 
        """
        with open(filename, "rb") as f:
            recipe_list = pickle.load(f)

        return recipe_list

    def __str__(self):
        """Returns a string representation of the GA."""
        return "Genetic Algorithm has " + str(self.iterations) + \
               " iterations and " + str(len(self.recipes)) + " recipes."

    def __repr__(self):
        """Returns a blueprint for a GeneticAlgorithm object."""
        return "GeneticAlgorithm('{0}', {1})".format(self.iterations,
                                                     self.recipes)


def main():
    ga = GeneticAlgorithm(50, "recipes/" + "*.txt")
    ga.run()
    print("Percentage of positive mutations: " + str(
        round(ga.positive_mutations * 100, 2)) + "%")




main()
