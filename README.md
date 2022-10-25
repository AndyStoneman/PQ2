# PQ2

## System Name: Cookaaae Maaaeker
### Submission Date: 10/25/22

## Project Description

Our cookie-recipe-making system uses a genetic algorithm which operates on a large inspiring set of around 70 cookie recipes gathered from the internet, from a few different cookie queries inspired by [this Allrecipes list](https://www.allrecipes.com/gallery/most-popular-types-of-cookies/). 
Each next generation is seeded by the top children and top performers from previous generations. 
We found the most common 9 ingredients across all recipes in our inspiring set and used those as the base ingredients. 6 of those should be included in every all cookies so they actually bake. Fitness was calculated through a combination of factors, including team-assigned scores of another, seperae ingredient list that we self selected and then scored based on personal preferences. We also added some ingredients from the inspiring set that aren't considered core ingredients, but are fun additional ingredients.

Our GA walks through selection, recombination/crossover, as well as mutation (where we swap in ingredients, remove them, or add in something new up to an ingredient threshold, because more is not always better when it comes to ingredients in a cookie). We did not allow ingredients to be deleted through mutation because we did not want the base/core set to be edited once the core group was choosen. 
Our fittest recipe is printed out at the end of running, alone with its fitness score and the percentage of positive mutations that contributed to the recipe turning out the way it did! We counted positive mutations by totalling the number of mutations, out of the total, that increased our fitness score and then reported that percentage. 
We capped our number of iterations around 50, we found that after about 100 the recipes converged and we wanted quality recipes but also a variety (hence picking partway on the way up to the convergence).

## Web Scraping Process - Creating the Inspiring Set

We based our recipe-specific web scraping methods off this [helpful British tutorial](https://practicaldatascience.co.uk/data-science/how-to-scrape-google-search-results-using-python), where we query google for cookie results.

Our queries list was as follows:
```
queries = [
    "snickerdoodle",
    "chocolate chip",
    "gingersnap",
    "shortbread",
    "peanut butter",
    "sugar",
    "molasses",
    "gingerbread",
    "butter",
    "spritz",
    "drop",
    "chocolate"
    ]
```
Notably, oatmeal raisin cookies were excluded due to disdain from 3 of 4 group members.

We performed google searches for "`query` cookies" and "`query` cookies recipe".
We then wrote the ingredients of these recipes to files, using the recipe_scraper python module to easily get a list of ingredients from the search.

We took the top 30 links from each search, although not every link yielded a properly formatted recipe that worked with the recipe_scraper module and thus we didn't end up with hundreds of recipes. After, we examined the files to remove duplicate recipes (some popular recipes popped up under both queries) and
to format the list of ingredients into csv form for easy creation of Recipe objects.

Once we created Recipe objects from our inspiring set, we used pickle to bundle them all up into one inspiring set file that contained a list of Recipes, so that we could save the initial set in one place and not have to parse each file into a Recipe object each time we wanted to run our program.
(We had a read-from-pickle- file method to get the list back when we needed it).

## Creating our Personal Ingredient Set - PPPPerspectives (Person)

We created a list of personal ingredients and then every person voted 1 (include), 0 (indifferent), or -1 (exclude). That meant every score was within the range -4 to 4. Some very polarizing ingredients like coffee or oatmeal had scores of 1, 0, or 1 as well as neutral ingredients like brown sugar. This way, the scores represent how important individual ingredients were to our group members, made the final recipe personally meaningful, and also revealed different tastes among group members. The personal ingredient set introduced some variety into the ingredients, as well as, provide more parameters for the fitness function. We should view our system as creative under the PPPPerspectives "Person/Producer" metric because our system has inherent human traits - preference for certain ingredients over others. Our system would be different for any other group of teammates and that makes this criteria meaningful for our particular creative system. 

## Criteria for Recipes - Ensuring Some Typicality

We decided due to our very large inspiring set that normalizing ingredient values would be difficult. Luckily, the majority of our recipes has similar serving sizes. We also counted the occurence of different ingredients among our recipes to find our most common 9 (when trying to account for differences in ingredients that were semantically the same but written differently, eg in most recipes flour and all-purpose flour). 
We used a function to find these but then we hard coded the common set to prevent making expensive calls to the common set finding algorithm which went through the whole recipe set.
We came up with the following dictionary of counts:
```
common_dict = [('baking soda', 50), ('baking powder', 50), \
                       ('vanilla extract', 50), \
                       ('sugar', 51), ('granulated sugar', 30),
                       ('salt', 54), ('egg', 55), ('butter', 60), \
                       ('all-purpose flour', 73)]

```
(Sugar here included things with sugar in the name that weren't granulated sugar, eg light brown sugar or dark brown sugar.
The spice cinnamon was also common (in top 10) but we decided to omit too many spices from this set of ingredients considered really important/that we wouldn't want to swap out to allow different flavors.

Since our fitness function rewarded the presence of "essential" ingredients and also highly rated personal ingredients, our system created very long recipes, but we know from personal experience that when it comes to preparing and eating a cookie, often less in more.
We decided to set a threshold of number ingredients for our recipes, which is set to the average number of ingredients across recipes in our inspiring set (this worked out to yield recipes of about length 10).

## Counting Positive Mutations 
To understand how our mutations changed the recipe, we counted the number of positive mutations, mutations that increase fitness of recipe. 
We wanted to ensure that the system created improvisations during the process rather than replicating stored recipes and so we could see how many changes were positive out of the total. This goes along with "Generation of Results" from SPECS. 
