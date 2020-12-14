import json
from data import *

def initialize_jsonld(recipe):
    jsonld = '{'
    jsonld += \
f"""
  "@context": "http://schema.org/",
  "@type": "Recipe",
  "name": "{recipe.name}",
  "datePublished": "{recipe.date_created}",
  "description": "{recipe.description}",
"""
    if recipe.image:
        jsonld += \
f"""
  "image": [
    "https://makimo.no/images/{recipe.image}",
    "https://makimo.no/images/thumbnails/{recipe.image}"
  ],
"""
    if recipe.yields:
        yield_as_string = ''
        for yield_data in recipe.yields:
            if yield_data.qualification:
                yield_as_string += f' {yield_data.qualification}:'
            yield_as_string += f' {yield_data.amount} {yield_data.unit}.'
        yield_as_string = json.dumps(yield_as_string.strip())
        jsonld += f'  "recipeYield": {yield_as_string},\n'
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
    jsonld += '  "recipeIngredient": [\n'
    ingredients = []
    for ingredient in recipe.ingredients:
        ingr_string = '    "'
        if ingredient.total_amount:
            ingr_string += f'{ingredient.total_amount} '
        if ingredient.unit != '':
            ingr_string += f'{ingredient.unit} '
        ingr_string += f'{ingredient.name}"'
        ingredients.append(ingr_string)
    jsonld += ',\n'.join(ingredients)
    jsonld += '\n  ],\n'
    return jsonld

def add_steps(recipe, jsonld):
    # If we ever get multiple part recipes, look at adding HowToSections
    jsonld += '  "recipeInstructions": [\n'
    steps = []
    for step in recipe.steps:
        step_string = '    {\n      "@type": "HowToStep",\n'
        if step.long != '':
            step_string += f'      "name": "{step.short}",\n'
            step_string += f'      "text": "{step.long}"'
        else:
            step_string += f'      "text": "{step.short}"'
        step_string += '\n    }'
        steps.append(step_string)
    jsonld += ',\n'.join(steps)
    jsonld += '\n  ]\n'
    return jsonld

def generate_jsonld(recipe):
    jsonld_string = initialize_jsonld(recipe)
    jsonld_string = add_ingredients(recipe, jsonld_string)
    jsonld_string = add_steps(recipe, jsonld_string)
    jsonld_string += "}"
    return jsonld_string

