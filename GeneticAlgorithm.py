import glob
import random
from Recipe import Recipe
from Ingredient import Ingredient
import pickle


class GeneticAlgorithm:
    """
    Class that runs through the genetic algorithm process for soup recipes. Includes selection, recombination, and
    mutation.

    Args:
        iterations (int): The number of iterations that the GA should run.

        input_recipes (Recipe[]): A list of recipe objects that are used as a starting initial population for the GA.
    
    Methods:
        run
            Synthesizes GA process including selection, recombination, mutation.
            Gives printed information about each iteration.
        selection()
            Selects twice number of recipes of initial set proportionally by fitness
        recombination(selected_recipes)

        check_fix_duplicates_recombination(first_half, second_half):
            Helper method that removes duplicate ingredients during recombination process
        
        4 different mutation submethods to change: ingredient name, ingredient amount,
        add or remove ingredient (each takes a recipe argument)

        normalize_ingredient_quantities(recipe, amt=100.0):
            normalizes quantities in the ingredient to 100oz
    """
    def __init__(self, iterations, input_recipes):
        self.iterations = iterations
        self.recipes = []
        self.inspiring_set_ingredient_names = set()
        #allow for passing null [] recipe list to create inspiring set

        for filename in glob.glob(input_recipes):
            recipe = Recipe(filename=filename)
            self.recipes.append(recipe)
            self.inspiring_set_ingredient_names.update(recipe.get_ingredient_names())
        self.inspiring_set_ingredient_length = len(list(self.inspiring_set_ingredient_names))

    def generate_random(self):
        return random.choice(self.recipes)

    def run(self):
        """
        The method that controls the entire overview of the GA process, running it the iterations of selection,
        recombination, and mutation, as well as printing useful information at the end of each iteration.
        """
        num_iteration = 0
        # Start iterations
        while num_iteration < self.iterations:
            original_list = self.recipes
            # Selection
            self.selection()
            # Recombination
            self.recombination(self.recipes)
            # Mutation
            for rec in self.recipes:
                probability = random.randint(0, 100)
                if probability < 80:
                    mutation_choice = random.randint(0, 4)
                    if mutation_choice == 0:
                        self.mutate_ingredient_amount(rec)
                    elif mutation_choice == 1:
                        self.mutate_ingredient_name(rec)
                    elif mutation_choice == 2:
                        self.mutate_add_recipe_ingredient(rec)
                    elif mutation_choice == 3:
                        self.mutate_remove_recipe_ingredient(rec)

                    # Normalization
                    self.normalize_ingredient_quantities(rec)

            # Combining top 50% of new and original recipes
            self.recipes.sort(key=lambda x: x.fitness)
            original_list.sort(key=lambda x: x.fitness)
            new_generation = self.recipes[(len(self.recipes) // 2):] + original_list[(len(original_list) // 2):]
            self.recipes = new_generation

            # Iteration print statements
            self.recipes.sort(key=lambda x: x.fitness)
            print("ITERATION: " + str(num_iteration + 1) + "\nFittest recipe:\nName: " + str(self.recipes[-1].get_name()) +
                  "\nFitness: " + str(self.recipes[-1].get_fitness()))
            num_iteration += 1

    def selection(self):
        """
        Runs the selection process, where twice the number of recipes in the initial population
        are selected proportionally to their fitness.
        """
        selected_recipes = []
        total = 0
        for j in range(len(self.recipes)):
            total += self.recipes[j].get_fitness()

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
        The selected recipes are recombined through single point crossover to form one child. At the completion of
        selection we are left with just one child per two parents.

        Args:
            selected_recipes (Recipe[]): A list of the recipes produced by selection, which is double the size of the
            initial population.
        """
        new_recipes = []
        for i in range(0, len(selected_recipes), 2):
            if selected_recipes[i].get_fitness() < selected_recipes[i + 1].get_fitness():
                random_index = random.randint(0, selected_recipes[i].get_fitness() - 1)
            else:
                random_index = random.randint(0, selected_recipes[i + 1].get_fitness() - 1)
            first_half = selected_recipes[i].ingredients[0:random_index]
            second_half = selected_recipes[i + 1].ingredients[random_index:]
            combined_list = self.check_fix_duplicates_recombination(first_half, second_half)
            new_recipe = Recipe(name="new_recipe_" + str(i // 2), ingredient_list=combined_list)
            new_recipes.append(new_recipe)
        self.recipes = new_recipes

    def check_fix_duplicates_recombination(self, first_half, second_half):
        """
        Helper method used to prevent duplicates during recombination. Does this by using a double loop that checks
        for duplicates, and if one is found, it just removes one of them.

        Args:
            first_half (Recipe[]): The first half of one of the parent candidates.

            second_half (Recipe[]): The second half of one of the parent candidates.

        Returns:
            The two lists (first_half and second_half) combined with no duplicates.
        """
        for x in range(len(first_half)):
            y = 0
            while y < len(second_half):
                if first_half[x].get_name() == second_half[y].get_name():
                    new_amount = first_half[x].get_amount() + second_half[y].get_amount()
                    first_half[x].set_amount(new_amount)
                    second_half.remove(second_half[y])
                else:
                    y += 1
        return first_half + second_half

    def mutate_ingredient_amount(self, recipe):
        """
        Mutation that changes an ingredient amount.
        Per assignment, 
        'an ingredient is selected uniformly at random from the recipe. 
         Its quantity is set to a new value somehow (up to you).'
         Right now either increase or decrease up to 20%, totally arbitrary

         Args:
             recipe (Recipe): The recipe that is having one of its ingredients mutated.
        """
        changing_ingredient = random.choice(recipe.ingredients)
        lower_scalar = random.uniform(0.8, 0.99)
        upper_scalar = random.uniform(1.01, 1.2) 
        random_scalar = random.choice([lower_scalar, upper_scalar])
        changed_quantity = changing_ingredient.get_amount() * random_scalar
        changing_ingredient.set_amount(changed_quantity)
    
    def mutate_ingredient_name(self, recipe):
        """
        Change of one ingredient to another: an ingredient is selected uniformly at random from the recipe.
        Its name is changed to that of another ingredient that is chosen at random from the ones we know in the
        inspiring set.

        Args:
             recipe (Recipe): The recipe that is having one of its ingredients mutated.
        
        """
        if len(recipe.ingredients) < self.inspiring_set_ingredient_length:
            changing_ingredient = random.choice(recipe.ingredients)

            inspiring_ingredients = list(self.inspiring_set_ingredient_names)
            new_ingredient = random.choice(inspiring_ingredients)
            while not recipe.add_ingredient(Ingredient(new_ingredient, changing_ingredient.get_amount())):
                new_ingredient = random.choice(inspiring_ingredients)
            recipe.remove_ingredient(changing_ingredient)

    def mutate_add_recipe_ingredient(self, recipe):
        """
        Mutation that adds an ingredient from the inspiring set.

        Args:
             recipe (Recipe): The recipe that is having one of its ingredients mutated.
        """
        if len(recipe.ingredients) < self.inspiring_set_ingredient_length:
            new_ingredient = random.choice(list(self.inspiring_set_ingredient_names))
            while not recipe.add_ingredient(Ingredient(new_ingredient, random.randint(0.0, 50.0))):
                new_ingredient = random.choice(list(self.inspiring_set_ingredient_names))
    
    def mutate_remove_recipe_ingredient(self, recipe):
        """
        Mutation that removes an ingredient from the recipe.

        Args:
             recipe (Recipe): The recipe that is having one of its ingredients mutated.
        """
        del_ingredient = random.choice(recipe.ingredients)
        recipe.remove_ingredient(del_ingredient)

    def normalize_ingredient_quantities(self, recipe, amt=100.0):
        """
        Normalizes ingredient quantities in a recipe to a specified amount.

        Args:
             recipe (Recipe): The recipe that is having one of its ingredients mutated.

             amt (int): The total amount the recipes should be normalized to. Defaulted to 100.
        """
        total_oz = 0
        for ingredient in recipe.ingredients:
            total_oz += ingredient.get_amount()

        ratio = amt / total_oz
        normalized_total = 0
        for ingredient in recipe.ingredients[:-1]:
            curr_amt = ingredient.get_amount()
            ingredient.set_amount(curr_amt * ratio)
            normalized_total += ingredient.get_amount()
        remainder = amt - normalized_total
        recipe.ingredients[-1].set_amount(remainder)
        normalized_total += remainder
    
    def save_recipe_to_file(self,recipe_list, file):
        """
        Saves a list of recipes to a file (allows us to save inspiring set)
        Inspired by https://stackoverflow.com/questions/20716812/saving-and-loading-multiple-objects-in-pickle-file
        """
        with open(file, 'wb') as f:
            pickle.dump(recipe_list, f)
        
    def load_recipe_list_from_file(self,filename):
        """
        Loads a recipe list from file using pickle.
        Also inspired by https://stackoverflow.com/questions/20716812/saving-and-loading-multiple-objects-in-pickle-file. 
        """
        with open(filename, "rb") as f:
            recipe_list = pickle.load(f)
        
        return recipe_list
    
    

    def __str__(self):
        """Returns a string representation of the GA."""
        return "Genetic Algorithm has " + str(self.iterations) + " iterations and " + str(len(self.recipes)) + \
               " recipes."

    def __repr__(self):
        """Returns a blueprint for a GeneticAlgorithm object."""
        return "GeneticAlgorithm('{0}', {1})".format(self.iterations, self.recipes)


def main():
    #For testing!
    ga = GeneticAlgorithm(1, "recipes/" + "*.txt")
    #print("x")

    '''
    all_recipes = []
    files = glob.glob("recipes/" + "*.txt")
    #print(files)
    for i in range(len(files)):
        #print(files[i])
        try:
            r = Recipe(files[i][8:len(files[i])-4], [], files[i])
            all_recipes.append(r)
        except:
            continue
    
    # ga.save_recipe_to_file(all_recipes, "recipe_objects_inspiring.pickle")
    #print("unpickle")
    #print(ga.load_recipe_list_from_file("recipe_objects_inspiring.pickle"))
    '''

    print(ga.generate_random())

main()