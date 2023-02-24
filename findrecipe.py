# Open the recipe file and read its contents
with open("recipe.txt", "r") as file:
    recipe_list = file.readlines()

# Define a function to search for a given ingredient in a recipe
def has_ingredient(recipe, ingredient):
    return ingredient.lower() in recipe.lower()

# Ask the user for the ingredient they want to search for
search_ingredient = input("Enter an ingredient to search for: ")

# Loop through each recipe in the recipe list and store the title and instructions of any that contain the ingredient
recipes = []
seen_titles = set()  # Keep track of the titles we've already seen
for i in range(len(recipe_list)):
    if "Gerecht" in recipe_list[i]:  # The line containing the title has "Gerecht"
        title_number = recipe_list[i].split()[1]  # Extract the number from the line
        title = recipe_list[i].replace(f"Gerecht {title_number}:", "").strip()  # Extract the title from the line and remove whitespace
    elif has_ingredient(recipe_list[i], search_ingredient) and title not in seen_titles:
        seen_titles.add(title)
        instructions = []  # Initialize a list to store the recipe instructions
        for j in range(i+1, len(recipe_list)):
            if "Gerecht" in recipe_list[j]:
                recipes.append({"title": title, "instructions": instructions})  # Store the title and instructions in a dictionary and append it to the list of recipes
                break
            else:
                instructions.append(recipe_list[j].strip())  # Add the line to the instructions
    if len(recipes) == 5:  # Stop searching after the first 5 matches are found
        break

# Print the found options
if len(recipes) == 0:
    print("No recipes found containing", search_ingredient)
else:
    for i in range(len(recipes)):
        print(f"{i+1}. {recipes[i]['title']}")

    # Ask the user if they want to add any recipes to their boodschappenlijst
    response = input("Would you like to add any of these recipes to your boodschappenlijst? (y/n)").lower()
    if response == "y":
        # Open the boodschappenlijst file in append mode
        with open("boodschappenlijst.txt", "a") as file:
            while True:
                # Ask the user for the number of the recipe they want to add
                recipe_num = input("Enter the number of the recipe you want to add to your boodschappenlijst (or 'done' to exit): ")
                if recipe_num == "done":
                    break
                elif recipe_num.isdigit() and int(recipe_num) in range(1, len(recipes)+1):
                    # Write the recipe title and instructions to the file
                    recipe = recipes[int(recipe_num)-1]
                    file.write(f"{recipe['title']}:\n")
                    for instruction in recipe['instructions']:
                        file.write(f"\t{instruction}\n")
                    print(f"{recipe['title']} has been added to your boodschappenlijst.")
                else:
                    print("Invalid input. Please enter the number of the recipe you want to add.")
