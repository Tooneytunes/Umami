import uvicorn
from fastapi import FastAPI
from jinja2 import Environment, FileSystemLoader
from fastapi.responses import HTMLResponse

# Open the recipe file and read its contents
with open("recipe.txt", "r") as file:
    recipe_list = file.readlines()


# Define a function to search for a given ingredient in a recipe
def has_ingredient(recipe, ingredient):
    return ingredient.lower() in recipe.lower()


def find_ingredient(search_ingredient):
    # Loop through each recipe in the recipe list and store the title and instructions of any that contain the ingredient
    recipes = []
    seen_titles = set()  # Keep track of the titles we've already seen
    for i in range(len(recipe_list)):
        if len(recipes) >= 5:  # Stop searching after the first 5 matches are found
            break
        if "Gerecht" in recipe_list[i]:  # The line containing the title has "Gerecht"
            title = recipe_list[i].replace(f"Gerecht:", "").strip()  # Extract the title from the line and remove whitespace
            start_line = i
            amount = recipe_list[start_line + 2]
        elif "Gehaald van:" in recipe_list[i]:
            url = recipe_list[i].replace(f"Gehaald van:", "").strip()
        elif (has_ingredient(recipe_list[i], search_ingredient) or has_ingredient(recipe_list[start_line], search_ingredient)) and title not in seen_titles:
            seen_titles.add(title)
            instructions = []  # Initialize a list to store the recipe instructions
            for j in range(start_line + 5, len(recipe_list)):
                if "Gerecht" in recipe_list[j] or j+1 == len(recipe_list):
                    recipes.append({"title": title, "url": url, "amount": amount, "instructions": instructions})  # Store the title and instructions in a dictionary and append it to the list of recipes
                    break
                else:
                    instructions.append(recipe_list[j].strip())  # Add the line to the instructions

    # Print the found options
    return recipes

app = FastAPI()

environment = Environment(loader=FileSystemLoader("templates/"))


@app.get('/')
def ingredient_view(search_ingredient=None):
    template = environment.get_template('index.html')

    if search_ingredient:
        recipe_list = find_ingredient(search_ingredient)
    else:
        recipe_list = []

    content = template.render(
        recipes=recipe_list,
        search_ingredient=search_ingredient
    )

    return HTMLResponse(
        content=content,
        status_code=200,
    )

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
