
import requests
import pandas as pd
import urllib
from pathlib import Path 

from requests_html import HTML
from requests_html import HTMLSession
from recipe_scrapers import scrape_me
#https://practicaldatascience.co.uk/data-science/how-to-scrape-google-search-results-using-python



def get_page_source(url):
    """Return the source code for the provided URL. 
    This code comes directly from Practical Data Science

    Args: 
        url (string): URL of the page to scrape.

    Returns:
        response (object): HTTP response object from requests_html. 
    """
    try:
        session = HTMLSession()
        response = session.get(url)
        return response

    except requests.exceptions.RequestException as e:
        print(e)

def get_recipes_from_google_url(search, num_recipes=30):
    """
    Gets recipes from a given google search 
    """
    query = urllib.parse.quote_plus(search)
    response = get_page_source("https://www.google.com/search?q=" + query)
    links = list(response.html.absolute_links)
    google_domains = ('https://www.google.', 
                      'https://google.', 
                      'https://webcache.googleusercontent.', 
                      'http://webcache.googleusercontent.', 
                      'https://policies.google.',
                      'https://support.google.',
                      'https://maps.google.',
                      'https://www.youtube',
                      'https://youtube')

    for url in links[:]:
        if url.startswith(google_domains):
            links.remove(url)

    return links

def get_recipe_from_url(url):
    
    try:
        recipe = scrape_me(url)
        

    except:
        return None
    
    #print(recipe.title(), recipe.ingredients())
    return recipe


def main():
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

    searches = {}
    for q in queries:
        query = q + " cookies"
        #searches[query] = []
        url_list = get_recipes_from_google_url(query)
        #print(url_list)
        searches[query] = url_list
    
    curr_path = Path(__file__).parent.resolve()
    #print("searches are", searches)
    for links in searches.values():
        count = 0
        for link in links:
            count += 1
            try:
                recipe = get_recipe_from_url(link)
                if recipe != None:
                    f = open("recipes/" + str(recipe.title()) + str(count) +".txt", "w")
                    f.write(str(recipe.ingredients()))
                    f.close()
                else:
                    print(links, "fail")
            except AttributeError:
                print("attr error")
            except:
                print("general error ")
            


if __name__ == "__main__":
    main()