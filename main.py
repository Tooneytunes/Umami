import requests, os
from bs4 import BeautifulSoup

# Read from recipe URL List
with open('recipe_urls.txt', 'r') as f:
    recipe_urls = f.readlines()

# Checking if file doesn't exist yet
if os.path.exists("recipe.txt"):
    os.remove("recipe.txt")
else:
    print("File is not present in system, making file")

# Make a file containing recipe information
with open('recipe.txt', 'a', encoding='utf-8') as f:

    # Loop through each url and extract recipe information
    for idx, url in enumerate(recipe_urls):
        # Get page content
        response = requests.get(url)
        soup = BeautifulSoup(response.content, 'html.parser')

        # Get recipe title
        recipe_title = soup.find('h1', class_='recipe-header_title__tG0JE').text

        # Get the count of people it's for
        amount = soup.find('p', class_='recipe-ingredients_count__zS2P-').text

        # Get ingredients & units
        ingredient_units = soup.find_all('p', class_='ingredient_unit__-ptEq')
        ingredients_list = soup.find_all('p', class_='ingredient_name__WXu5R')

        # Combine ingredients with their measurement units
        ingredients = [f"{unit.text} {ingredient.text}" for unit, ingredient in zip(ingredient_units, ingredients_list)]

        # Append this recipe to the file
        f.write(f"Gerecht: {recipe_title}\nGehaald van: {url}{amount}\n\nIngredienten:\n")
        print(f"Gerecht: {recipe_title} has been added")
        for idx_ingredients, ingredient in enumerate(ingredients):
            f.write(f"- {ingredient}\n")
            # Make sure that there is an enter at the end of the ingredient list
            if idx_ingredients == len(ingredients) - 1:
                f.write("\n")
