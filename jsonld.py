import json
from data import *

jsonIndent = '  '

def initialize_jsonld(recipe):
    jsonld = '{'
    # print(json.dumps(recipe.name))
    jsonld += \
f"""
{jsonIndent}"@context": "http://schema.org/",
{jsonIndent}"@type": "Recipe",
{jsonIndent}"name": {json.dumps(recipe.name)},
{jsonIndent}"datePublished": "{recipe.date_created}",
{jsonIndent}"description": {json.dumps(recipe.description)},
"""
    if recipe.image:
        jsonld += \
f"""
{jsonIndent}"image": [
{2*jsonIndent}"https://makimo.no/images/{recipe.image}",
{2*jsonIndent}"https://makimo.no/images/thumbnails/{recipe.image}"
{jsonIndent}],
"""
    if recipe.yields:
        yield_as_string = ''
        for yield_data in recipe.yields:
            if yield_data.qualification:
                yield_as_string += f' {yield_data.qualification}:'
            yield_as_string += f' {yield_data.amount} {yield_data.unit}.'
        yield_as_string = json.dumps(yield_as_string.strip())
        jsonld += f'{jsonIndent}"recipeYield": {yield_as_string},\n'
    return jsonld

# TODO add author (@type Persons , can I add us both?)
# TODO remove newlines from description
# TODO add time, keywords, category, cuisine
#    "prepTime": "PT40M",
#    "cookTime": "PT30M",
#    "totalTime": "PT1H10M",
#    "keywords": "cake for a party, coffee",
#    "recipeCategory": "Dessert",
#    "recipeCuisine": "American",


def add_ingredients(recipe, jsonld):
    jsonld += f'{jsonIndent}"recipeIngredient": [\n'
    ingredients = []
    for ingredient in recipe.ingredients:
        ingr_string = ''
        if ingredient.total_amount:
            ingr_string += f'{ingredient.total_amount} '
        if ingredient.unit != '':
            ingr_string += f'{ingredient.unit} '
        ingr_string += f'{ingredient.name}'
        ingredients.append(f'{2*jsonIndent}{json.dumps(ingr_string)}')
    jsonld += ',\n'.join(ingredients)
    jsonld += f'\n{jsonIndent}],\n'
    return jsonld

def add_steps(recipe, jsonld):
    # If we ever get multiple part recipes, look at adding HowToSections
    jsonld += '  "recipeInstructions": [\n'
    steps = []
    for step in recipe.steps:
        step_string = f'{2*jsonIndent}' + '{\n' + f'{3*jsonIndent}"@type": "HowToStep",\n'
        if step.long != '':
            step_string += f'{3*jsonIndent}"name": {json.dumps(step.short)},\n'
            step_string += f'{3*jsonIndent}"text": {json.dumps(step.long)}'
        else:
            step_string += f'{3*jsonIndent}"text": {json.dumps(step.short)}'
        step_string += '\n' + f'{2*jsonIndent}' + '}'
        steps.append(step_string)
    jsonld += ',\n'.join(steps)
    jsonld += f'\n{jsonIndent}]\n'
    return jsonld

def generate_jsonld(recipe):
    jsonld_string = initialize_jsonld(recipe)
    jsonld_string = add_ingredients(recipe, jsonld_string)
    jsonld_string = add_steps(recipe, jsonld_string)
    jsonld_string += "}"
    return jsonld_string

