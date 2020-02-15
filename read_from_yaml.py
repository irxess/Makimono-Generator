import os
import yaml
from data import *

def create_sorted_ingredient_overview(recipe):
    ingredients = dict()
    for step in recipe.steps:
        for ingr in step.ingredients_used:
            name = ingr.name
            amount = 0
            if ingr.amount:
                amount = ingr.amount
            unit = ingr.unit
            comment = ''
            if ingr.comment:
                comment = ingr.comment
            if not name in ingredients:
                ingredients[name] = [(amount, unit, comment)]
            else:
                added = False
                for index,item in enumerate(ingredients[name]):
                    if unit == item[1]:
                        ingredients[name][index] = (item[0]+amount, unit, item[2]+comment)
                        added = True
                if not added:
                    index = 0
                    for item in ingredients[name]:
                        if item[0] > amount:
                            index += 1
                        else:
                            break
                    ingredients[name].insert(index, (amount, unit, comment))

    sorted_ingredients = sorted(ingredients.items(), key=lambda kv: kv[1][0], reverse=True)

    for kv in sorted_ingredients:
        name = kv[0]
        for value in kv[1]:
            amount = value[0]
            if amount == 0:
                amount = ''
            ingr_overview = IngredientsOverview(name=name, total_amount=amount, unit=value[1], comment=value[2])
            recipe.ingredients.append(ingr_overview)

def read_steps(yaml, recipe):
    if 'steps' in yaml:
        id = 0
        for step in yaml['steps']:
            active_time = 0
            passive_time = 0
            if 'active-time' in step:
                active_time = step['active-time']
            if 'passive-time' in step:
                passive_time = step['passive-time']
            time = StepTime(active=active_time, passive=passive_time)
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

def read_source(yaml_source):
    name = yaml_source['name']
    source = Source(name)
    if 'type' in yaml_source:
        source.originality = yaml_source['type']
    if 'author' in yaml_source:
        source.author = yaml_source['author']
    if 'publication' in yaml_source:
        source.publication = yaml_source['publication']
    if 'url' in yaml_source:
        source.url = yaml_source['url']
    if 'date' in yaml_source:
        source.date = yaml_source['date']
    return source

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
        recipe.source = read_source(yaml['source'])
    if 'result' in yaml:
        recipe.result = Yield(yaml['result']['amount'], yaml['result']['name'])
    return recipe

def read_recipe_into_data(name):
    path = os.path.join('recipes', name+'.yaml')
    with open(path, 'r', encoding='utf-8') as recipe_file:
        yaml_data = yaml.load(recipe_file, Loader=yaml.FullLoader)
    recipe = read_recipe(yaml_data)
    read_steps(yaml_data, recipe)
    create_sorted_ingredient_overview(recipe)
    return recipe

if __name__ == "__main__":
    #r = read_recipe_into_data("simons-burger")
    #r = read_recipe_into_data("muffins-blueberry-and-basil")
    r = read_recipe_into_data("saffron-knots")
    print(r)
    for s in r.steps:
        print(s.short)
    for i in r.ingredients:
        print(f"{i.total_amount} {i.unit} {i.name}")

    import timeline
    timeline.generate_svg(r)
    timeline.print_nodes(r)

