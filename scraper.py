#python2
import requests
from bs4 import BeautifulSoup
import json
import parse_ingredient

#URL = "https://www.foodnetwork.com/recipes/food-network-kitchen/black-eyed-pea-soup-3361891"
#URL = "https://www.foodnetwork.com/recipes/food-network-kitchen/the-best-oatmeal-raisin-cookies-7197039"

run = True
recipe_counter = 0
recipe = {}

while(run):
    URL = input("Enter URL from Food Network to parse or write stop: ")

    if(URL == "stop"):
        print("Stopping program")
        exit()

    page = requests.get(URL)
    soup = BeautifulSoup(page.text, 'html.parser')

    title = str(soup.find(class_="o-AssetTitle__a-HeadlineText").text.strip())
    time = str(soup.find(class_="o-RecipeInfo__a-Description m-RecipeInfo__a-Description--Total").text) #1.text 2.str 3.split. 4.[0] 5.int
    servings = str(soup.find(class_="o-RecipeInfo__m-Yield").find(class_="o-RecipeInfo__a-Description").text)

    """Ingredients"""
    ingredients = soup.find_all(class_="o-Ingredients__a-Ingredient--CheckboxLabel")
    ingredients_recipe = []
    ingredients_tags = []

    for ingredient in ingredients[1:]:
        ingredients_recipe.append(ingredient.text)
        #ingredient_parsed = parse_ingredient.parse(ingredient.text).as_dict()
        #ingredient_name = ingredient_parsed["product"]
        #ingredients_tags.append(ingredient_name)
    #print(ingredients_tags)

    """Instructions"""
    instructions = soup.find_all(class_="o-Method__m-Step")
    instructions_recipe = {}
    instructions_counter = 1

    for instruction in instructions:
        instructions_recipe[instructions_counter] = instruction.text.strip()
        instructions_counter += 1

    """Categories"""
    categories = soup.find_all(class_="o-Capsule__a-Tag a-Tag")
    categories_recipe = []

    for category in categories:
        categories_recipe.append(category.text.strip())

    """Json encoding"""
    data = {"title": title, "time": time, "servings": servings, "ingredients": ingredients_recipe, "instructions": instructions_recipe, "categories": categories_recipe}
    recipe[recipe_counter] = data
    with open('data.json', 'w') as f:
        json.dump(recipe, f, indent=2)
    #{'title': title, 
    # 'time': time, 
    # 'servings': servings,
    # 'ingredients' : {'id': ingredient, 'id': ingredient},
    # 'instructions': {'step1': step, 'step2': step2},
    # 'categories': [cat1, cat2, cat3]}

    """Prints"""
    #print("title: ", title)
    #print("time: ", time)
    #print("servings: ", servings)
    #print("ingredients: ", ingredients_recipe)
    #print("instructions: ", instructions_recipe)
    #print("categories: ", categories_recipe)

    recipe_counter += 1

with open('data.json', 'w') as f:
        json.dump(recipe, f, indent=2)