import os
import yaml
from data import *

def create_ingredient_overview(recipe):
    ingredients = dict()
    for step in recipe.steps:
        for ingr in step.ingredients_used:
            name = ingr.name
            amount = 0
            if ingr.amount:
                amount = ingr.amount
            unit = ingr.unit
            comment = ingr.comment
            key_tuple = (name, unit) # Same ingredient but different units should get distinct entries in overview.
            if not key_tuple in ingredients:
                ingredients[key_tuple] = IngredientsOverview(name=name, total_amount=amount, unit=unit, comment=comment)
            else:
                ingredients[key_tuple].total_amount += amount
                if comment and ingredients[key_tuple].comment != comment:
                    ingredients[key_tuple].comment += comment
    ingredients_sorted_by_amount = sorted(ingredients.items(), key=lambda kv: kv[1].total_amount, reverse=True)
    for k,v in ingredients_sorted_by_amount:
        recipe.ingredients.append(v)


def read_steps(yaml, recipe):
    if 'steps' in yaml:
        id = 0
        for step in yaml['steps']:
            if 'time' in step:
                time = StepTime(active=step['time'], passive=0)
            else:
                time = StepTime(active=1, passive=0)
            type = step['type']
            temperature = step['temp']
            step_data = Step(id=id, time=time, step_type=type, temperature=temperature)
            if 'short' in step:
                step_data.short = step['short']
            if 'long' in step:
                step_data.long = step['long']

            if 'ingredients' in step:
                add_ingredients_from_step_to_step_data(step, step_data)
            if 'refined_ingredients' in step:
                add_refined_ingredients_from_step_to_step_data(step, step_data)
            if 'dependencies' in step:
                add_dependencies_to_step_data(step, step_data)

            recipe.steps.append(step_data)
            id += 1
    else:
        print(f'Recipe {recipe.name} has no steps.')

def add_ingredients_from_step_to_step_data(step, step_data):
    for ingr in step['ingredients']:
        name = ingr['name']
        amount = ingr['amount'] # might fail?
        ingredient = Ingredient(name=name, amount=amount)
        #if not name in ingredients:
            #ingredients[name] = IngredientsOverview(name,
        if 'unit' in ingr:
            ingredient.unit = ingr['unit']
        if 'comment' in ingr:
            ingredient.comment = ingr['comment']
            #ingredients[name].comment = ingredient.comment
        step_data.ingredients_used.append(ingredient)

def add_refined_ingredients_from_step_to_step_data(step, step_data):
    for ingr in step['refined_ingredients']:
        ingredient = RefinedIngredient(name=ingr['name'])
        if 'amount' in ingr:
            ingredient.amount = ingr['amount']
        if 'unit' in ingr:
            ingredient.unit = ingr['unit']
        step_data.refined_ingredients_used.append(ingredient)

def add_dependencies_to_step_data(step, step_data):
    for dep in step['dependencies']:
        step_data.depends_on.append( step_data.id + int(dep) )
    # Sort the list to try to make the generated graph look a bit prettier.
    # The desired effect is that the steps occurring earlier are processed earlier, so that earlier entries get smaller y values.
    step_data.depends_on.sort()

def read_recipe(yaml):
    name = yaml['recipe']
    created = yaml['date_created']
    if 'last_updated' in yaml:
        updated = yaml['last_updated']
    else:
        updated = created
    recipe = Recipe(name, created, updated)
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
    read_steps(yaml_data, recipe)
    create_ingredient_overview(recipe)
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

