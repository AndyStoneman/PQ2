# PQ2

## System Name: Cookaaae Maaaeker
### submission date: 10/25/22

## Project Description

Our cookie-recipe-making system uses a genetic algorithm which operates on a large inspiring set of around 70 cookie recipes gathered from the internet, from a few different cookie queries inspired by [this Allrecipes list](https://www.allrecipes.com/gallery/most-popular-types-of-cookies/). 
Each next generation is seeded by the top children and top performers from previous generations. 
Fitness is indicated by a combination of factors, including influence from a list of ingredients that we scored and selected as a group, as well as mixing in some ingredients from the inspiring set that aren't considered core ingredients or the "glue" of a cookie, but are fun additional ingredients.
Our GA walks through selection, recombination/crossover, as well as mutation (where we swap in ingredients, remove them, or add in something new up to an ingredient threshold, because more is not always better when it comes to ingredients in a cookie). 
Our fittest recipe is printed out at the end of running, alone with its fitness score and the percentage of positive mutations that contributed to the recipe turning out the way it did!

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

We took the top 30 links from each searcg, although not every link yielded a properly formatted recipe that worked with the recipe_scraper module and thus we didn't end up with hundreds of recipes. After, we examined the files to remove duplicate recipes (some popular recipes popped up under both queries) and
to format the list of ingredients into csv form for easy creation of Recipe objects.

Once we created Recipe objects from our inspiring set, we used pickle to bundle them all up into one inspiring set file that contained a list of Recipes, so that we could save the initial set in one place and not have to parse each file into a Recipe object each time we wanted to run our program.
(We had a read-from-pickle- file method to get the list back when we needed it).

## Creating our Personal Ingredient Set
We created a list of personal ingredients that we voted on as a group to give scores that indicated how important they were to include in the recipe.
This helped make our project personally meaningful, and also revealed different tastes among group members.
This personal ingredient set helped introduce some variety into the ingredients as well as give more indicators for fitness.

## Criteria for Recipes - Ensuring Some Typicality

We decided due to our very large inspiring set that normalizing ingredient values would be difficult. Luckily, the majority of our recipes has similar serving sizes. We also counted the occurence of different ingredients among our recipes to find our most common 9 (when trying to account for differences in ingredients that were semantically the same but written differently, eg in most recipes flour and all-purpose flour). 
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

At first, due to our fitness function rewarding the presence of "essential" ingredients and also highly or higher rated personal ingredients, we noticed the number of ingredients in our recipes ballooning. However, when it comes to preparing and eating a cookie, often less in more.
We decided to set a threshold of number ingredients for our recipes, which is set to the average number of ingredients across recipes in our inspiring set (this worked out to yield recipes of about length 10).

## Creativitiy Metrics


#Instructions to Run


1) Typicality - measuring this by number of ingredients being less than some threshold value and also reward common ingredient set in our fitness function.
2) Person (PPPPerspectives) - we have our personal ingredient set and that showcases our groups prefrences. Our system exhibits preferences and taste which are specific human cognitive traits and therefore we can view our system as a creative agent. 
3) Count number of positive mutations (mutations that increase fitness of recipe) -- 
    This goes along with "Generation of Results" in SPECS,
    Does the system create improvisations during the process (rather than replicating stored recipes)?
    Yes, it does, and we can count which improvisations are positive as well. 
