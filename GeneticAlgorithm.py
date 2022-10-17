import glob
import random
from Recipe import Recipe
from Ingredient import Ingredient
from GroupIngredients import GroupIngredients
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
        self.positive_mutations = 0
        self.iterations = iterations
        self.recipes = []
        self.inspiring_set_ingredient_names = set()
        #allow for passing null [] recipe list to create inspiring set
        self.average_recipe_length = 0
        self.num_files = 0
        for filename in glob.glob(input_recipes):
            recipe = Recipe(filename=filename)
            if recipe:
                self.recipes.append(recipe)
                self.inspiring_set_ingredient_names.update(recipe.get_ingredient_names())
                self.average_recipe_length += len(recipe.get_ingredient_names())
                self.num_files += 1
        self.inspiring_set_ingredient_length = len(list(self.inspiring_set_ingredient_names))
        self.average_recipe_length /= self.num_files

    def generate_random(self):
        return random.choice(self.recipes)

    def run(self):
        """
        The method that controls the entire overview of the GA process, running it the iterations of selection,
        recombination, and mutation, as well as printing useful information at the end of each iteration.
        """
        num_iteration = 0
        num_mutations = 0
        # Start iterations
        while num_iteration < self.iterations:
            for recipe in self.recipes:
                recipe.calculate_fitness(self.average_recipe_length)
            original_list = self.recipes
            # Selection
            self.selection()
            # Recombination
            self.recombination(self.recipes)
            # Mutation
            for rec in self.recipes:
                old_fitness = rec.get_fitness()
                probability = random.randint(0, 100)
                if probability < 80:
                    mutation_choice = random.randint(1, 4)
                    '''
                    if mutation_choice == 0:
                        self.mutate_ingredient_amount(rec)
                    '''
                    num_mutations += 1
                    if mutation_choice == 1:
                        self.mutate_ingredient_name(rec)
                    elif mutation_choice == 2:
                        self.mutate_add_recipe_ingredient(rec)
                    elif mutation_choice == 3:
                        self.mutate_remove_recipe_ingredient(rec)


                    # Normalization
                    #self.normalize_ingredient_quantities(rec)
                rec.calculate_fitness(self.average_recipe_length)

                new_fitness = rec.get_fitness()
                if old_fitness < new_fitness:
                    self.positive_mutations += 1

            # Combining top 50% of new and original recipes
            self.recipes.sort(key=lambda x: x.fitness)
            original_list.sort(key=lambda x: x.fitness)
            new_generation = self.recipes[(len(self.recipes) // 2):] + original_list[(len(original_list) // 2):]
            self.recipes = new_generation
            # Iteration print statements
            self.recipes.sort(key=lambda x: x.fitness)
            self.recipes = new_generation
            print("ITERATION: " + str(num_iteration + 1) + "\nFittest recipe:\nName: " + str(self.recipes[-1].get_name()) +
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
                ingredient_amounts[ingredient] = ingredient_amounts.\
                                                     get(ingredient, 0) + 1
        common_list = sorted(ingredient_amounts.items(),
                             key=lambda item: item[1])[-9:]
        return common_list
    
    def create_inspiring_set_ingredients(self):
        """
        Creates a list of ingredients from the inspiring set that were
        not identified as "common set" ingredients, to be used in 
        mutation.
        Returns a list of 'non-core' ingredients.
        """
        common_list_ing_names = ['baking soda', 'baking powder', \
            'vanilla extract', 'sugar', 'granulated sugar', 'salt', 'egg', \
                'butter', 'all-purpose flour']
        non_core_ingredients = {}
        for rec in self.recipes:
            for ingredient in rec.ingredients:
                name = ingredient.get_name()
                if name not in common_list_ing_names:
                    if name not in non_core_ingredients:
                        non_core_ingredients[name] = [ingredient]
                    elif name in non_core_ingredients:
                        non_core_ingredients[name].append(ingredient)
        
        delete_list = []
        for item in non_core_ingredients.items():
            #filtering: remove any ingredient with only 1 appearance to get
            #rid of some typos
            if len(item[1]) <= 1:
                delete_list.append(item[0])
            if len(item[1]) > 1: #second part of tuple
                new_item = self.regulate_inspiring_ingredient(item[0],item[1])
                non_core_ingredients[item[0]] = new_item
       

        """
        Here, we'll want to filter the list further most likely.
        One way to do that is to eliminate any ingredient that only appears once
        in recipes (so delete all non core ingredients that initially had 
        len(item[1] above as == 1)). This change has been implemented below
        We also may need to change names to match against our personal 
        ingredients list to give them the same score as those ingredients.
        (There is some overlap, which isn't a bad thing bc this is still 
        ~organic~).
        """
    
    
        #manual filtering, water came from a frosting recipe
         #we previously had 3 different chocolate chip entries
        #all with about 1.5 cups, let's consolidate

        manual_keys = ["water", "eggs", "salted butter", 'semisweet chocolate chips', 'semi-sweet chocolate chips']
        for key in manual_keys:
            if key in non_core_ingredients:
                del non_core_ingredients[key]
        

        for key in non_core_ingredients.keys():
            if "sugar" in key or "salt" in key :
                delete_list.append(key)

        for key in delete_list:
            if key in non_core_ingredients:
                del non_core_ingredients[key]

        #change names and scores if it matches personal ingredient list item
        if "milk" in non_core_ingredients:
            non_core_ingredients["non fat milk"] = non_core_ingredients["milk"]
            non_core_ingredients["non fat milk"].set_score(3)
            del non_core_ingredients["milk"]
        #tragically this needs to match our typo

        if "cocoa powder" in non_core_ingredients and "unsweetened cocoa powder" in non_core_ingredients:
            non_core_ingredients["unsweetened coco powder"] = non_core_ingredients["cocoa powder"]
            non_core_ingredients["unsweetened coco powder"].set_score(4)
            del non_core_ingredients["cocoa powder"]
            del non_core_ingredients["unsweetened cocoa powder"]
        
        if "maple flavoring" in non_core_ingredients:
            non_core_ingredients["maple extract"] = non_core_ingredients["maple flavoring"]
            non_core_ingredients["maple extract"].set_score(2)
        
        if "nutmeg" in non_core_ingredients:
            non_core_ingredients["nutmeg"].set_score(4)
        
        #for testing 
        #print(non_core_ingredients)
          
        return non_core_ingredients
    
    def regulate_inspiring_ingredient(self,ing_name,ingredient_list):
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
        max_key = max(units, key= lambda x: len(units[x]))
        avg_amount = sum(units[max_key]) / len(units[max_key])
       
        #max key code inspired by:
        #https://stackoverflow.com/questions/21839208/dictionary-with-lists-as-values-find-longest-list 
        #name, amt, unit, score

        #do a check for ingredients that overlap with personal set to 
        #adjust score
        ingred = Ingredient(ing_name, avg_amount, max_key, 1)
    
        return ingred


    def selection(self):
        """
        Runs the selection process, where twice the number of recipes in the initial population
        are selected proportionally to their fitness.
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
        The selected recipes are recombined through single point crossover to form one child. At the completion of
        selection we are left with just one child per two parents.

        Args:
            selected_recipes (Recipe[]): A list of the recipes produced by selection, which is double the size of the
            initial population.
        """
        new_recipes = []
        for i in range(0, len(selected_recipes), 2):
            if selected_recipes[i].get_fitness() < selected_recipes[i + 1].get_fitness():
                random_index = random.randint(0, int(selected_recipes[i].get_fitness()))
            else:
                random_index = random.randint(0, int(selected_recipes[i + 1].get_fitness()))
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
                    new_amount = first_half[x].get_amount() 
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
        old_fitness = recipe.fitness
        
        personal_items = self.load_recipe_list_from_file("personalIngredientsList.pickle")
        inspiring_items = list(self.create_inspiring_set_ingredients().values())
        
        #mix of personal items and some pulled from recipes
        #may need to delete duplicates to avoid unfair weighting
        all_items = personal_items.ingredients
    
        for it in inspiring_items:
            all_items.append(it)
        new_ingredient = random.choice(all_items)
        #print(recipe.ingredients)
        ingredient_to_remove = random.choice(recipe.ingredients)

        common_dict = [('baking soda', 50), ('baking powder', 50),\
             ('vanilla extract', 50), \
            ('sugar', 51), ('granulated sugar', 30),
             ('salt', 54), ('egg', 55), ('butter', 60),\
                 ('all-purpose flour', 73)]
        common_list = []
        for k,v in common_dict:
            common_list.append(k)
        count = 0
        while ingredient_to_remove.get_name() in common_list and count == 8:
            ingredient_to_remove = random.choice(recipe.ingredients)
            if ingredient_to_remove.get_name() not in common_list:
                recipe.remove_ingredient(ingredient_to_remove)
                break
            else:
                ingredient_to_remove = random.choice(recipe.ingredients)
            count += 1

        while not recipe.add_ingredient(new_ingredient):
                new_ingredient = random.choice(all_items)
        
        new_fitness = recipe.fitness
        if new_fitness > old_fitness:
            self.positive_mutations += 1

    def mutate_add_recipe_ingredient(self, recipe, threshold=16):
        """
        Mutation that adds an ingredient from the inspiring set.

        Args:
             recipe (Recipe): The recipe that is having one of its ingredients mutated.
        """
        old_fitness = recipe.get_fitness()
        personal_items = self.load_recipe_list_from_file("personalIngredientsList.pickle")
        inspiring_items = list(self.create_inspiring_set_ingredients().values())
        
        #mix of personal items and some pulled from recipes
        #may need to delete duplicates to avoid unfair weighting
        all_items = personal_items.ingredients
    
        for it in inspiring_items:
            all_items.append(it)
   
        #new_ingredient = random.choice(personal_items.ingredients)
        new_ingredient = random.choice(all_items)
        
        if len(recipe.ingredients) + 1 <= threshold:
            while not recipe.add_ingredient(new_ingredient):
                #new_ingredient = random.choice(personal_items.ingredients)
                new_ingredient = random.choice(all_items)
        

        
        #if recipe old fitness < recipe new fitness, we count this as a positive mutation
    
    def mutate_remove_recipe_ingredient(self, recipe):
        """
        Mutation that removes an ingredient from the recipe.

        Args:
             recipe (Recipe): The recipe that is having one of its ingredients mutated.
        """

        common_dict = [('baking soda', 50), ('baking powder', 50), \
                       ('vanilla extract', 50), \
                       ('sugar', 51), ('granulated sugar', 30),
                       ('salt', 54), ('egg', 55), ('butter', 60), \
                       ('all-purpose flour', 73)]
        common_list = []
        for k, v in common_dict:
            common_list.append(k)
        del_ingredient = random.choice(recipe.ingredients)
        while del_ingredient.get_name() in common_list:
            del_ingredient = random.choice(recipe.ingredients)
            if del_ingredient.get_name() not in common_list:
                recipe.remove_ingredient(del_ingredient)
                break
            else:
                del_ingredient = random.choice(recipe.ingredients)


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
    
    def save_recipe_to_file(self, recipe_list, file):
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
    
    ga = GeneticAlgorithm(50, "recipes/" + "*.txt")
    #print("x")

    '''
    #SAVING 
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
    
    ga.save_recipe_to_file(all_recipes, "recipe_objects_inspiring.pickle")
    '''
    #personalIngredients = GroupIngredients("personalIngredients.csv")
    #ga.save_recipe_to_file(personalIngredients, "personalIngredientsList.pickle" )

    #print(personalIngredients)
    
    #print("unpickle")
    #print(ga.load_recipe_list_from_file("recipe_objects_inspiring.pickle"))
    #print(ga.generate_random())

    """
    To test abby's functions from 10/16:
    run the following line of code below, uncommented
    """
    print(ga.create_inspiring_set_ingredients())

    #rec = random.choice(ga.recipes)
    #for i in range(3):
        #print(rec)
        #ga.mutate_add_recipe_ingredient(rec)
        #print(rec)

    ga.run()
    print("Percentage of positive mutations: " + str(round(ga.positive_mutations * 100, 2)) + "%")
    #print(ga.recipes[-1].ingredients)
    #l = ga.load_recipe_list_from_file("recipe_objects_inspiring.pickle")
    #x = random.choice(l)

    """
    print(x.calculate_fitness())
    if not hasattr(x, 'score'):
        ga.mutate_add_recipe_ingredient(x)
        
        ga.mutate_ingredient_name(x)
        print(x)
        print(ga.create_common_list())

        print(ga.positive_mutations)
    """

main()
