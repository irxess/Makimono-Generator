import os
import yaml
from data import *

def create_ingredient_overview(recipe, ingredients):
    for step in recipe.steps:
        for ingr in step.ingredients_used:
            name = ingr.name
            amount = ingr.amount
            unit = ingr.unit
            comment = ingr.comment
            if not name in ingredients:
                ingredients[name] = IngredientsOverview(name, amount, unit, comment)
            else:
                ingredients[name].total_amount += amount
                if ingredients[name].unit != unit:
                    print("Multiple amount units used for {name} in {recipe.name}")
                ingredients[name].comment += comment
    for k,v in ingredients.items():
        recipe.ingredients.append(v)


def read_steps(yaml, recipe, ingredients):
    if 'steps' in yaml:
        id = 0
        for step in yaml['steps']:
            if 'time' in step:
                time = StepTime(step['time'], 0)
            else:
                time = StepTime(1,0)
            type = step['type']
            temperature = step['temp']
            step_data = Step(id, time, type, temperature, [], [], [])
            if 'short' in step:
                step_data.short = step['short']
            if 'long' in step:
                step_data.long = step['long']

            if 'ingredients' in step:
                for ingr in step['ingredients']:
                    name = ingr['name']
                    amount = ingr['amount'] # might fail?
                    ingredient = Ingredient(name, amount)
                    #if not name in ingredients:
                        #ingredients[name] = IngredientsOverview(name, 
                    if 'unit' in ingr:
                        ingredient.unit = ingr['unit']
                    if 'comment' in ingr:
                        ingredient.comment = ingr['comment']
                        #ingredients[name].comment = ingredient.comment
                    step_data.ingredients_used.append(ingredient)
            if 'refined_ingredients' in step:
                for ingr in step['refined_ingredients']:
                    ingredient = RefinedIngredient(ingr['name'])
                    if 'amount' in ingr:
                        ingredient.amount = ingr['amount']
                    if 'unit' in ingr:
                        ingredient.unit = ingr['unit']
                    step_data.refined_ingredients_used.append(ingredient)
            recipe.steps.append(step_data)
            id += 1
    else:
        print(f'Recipe {recipe.name} has no steps.')

def read_ingredients(yaml):
    ingredients = dict()
    if 'ingredients' in yaml:
        id = 0
        for i in yaml['ingredients']:
            name = i['name']
            amount = i['amount']
            ingredients[name] = Ingredient(id, name, amount)
            if 'unit' in i:
                ingredients[name].unit = i['unit']
            if 'comment' in i:
                ingredients[name].comment = i['comment']
            id += 1
    return ingredients

def read_recipe(yaml):
    name = yaml['recipe']
    created = yaml['date_created']
    if 'last_updated' in yaml:
        updated = yaml['last_updated']
    else:
        updated = created
    recipe = Recipe(name, created, updated, [], [])
    if 'image' in yaml:
        recipe.image = yaml['image']
    if 'description' in yaml:
        recipe.description = yaml['description']
    if 'source' in yaml:
        recipe.source = yaml['source']
    return recipe

def read_recipe_into_data(name):
    path = os.path.join('recipes', name+'.yaml')
    with open(path, 'r') as recipe_file:
        yaml_data = yaml.load(recipe_file)
    recipe = read_recipe(yaml_data)
    #ingredient_dict = read_ingredients(yaml_data)
    ingredient_dict = dict()
    read_steps(yaml_data, recipe, ingredient_dict)
    create_ingredient_overview(recipe, ingredient_dict)
    return recipe

if __name__ == "__main__":
    #r = read_recipe_into_data("simons-burger")
    #r = read_recipe_into_data("muffins-blueberry-and-basil")
    r = read_recipe_into_data("brown-cheese-sauce")
    print(r)
    for s in r.steps:
        print(s.short)
    for i in r.ingredients:
        print(f"{i.total_amount} {i.unit} {i.name}")

    import timeline
    timeline.generate_svg(r)
    timeline.print_nodes(r)

