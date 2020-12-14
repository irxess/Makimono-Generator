from data import *

jsonIndent = '  '
base_url = 'https://makimo.no'

def escape_json(string_to_escape):
    # Because we only have to consider these cases (I'm actually unsure about whether we need the backslash handling),
    # forgo all the work of maintaining an external dependency and just do it ourselves like this.
    escaped_string = string_to_escape
    escaped_string = escaped_string.replace('\\', '\\\\')
    escaped_string = escaped_string.replace('"', '\\"')
    escaped_string = escaped_string.replace("'", "\\'")
    return escaped_string

def convert_minutes_to_iso8601_duration(minutes_int):
    if minutes_int < 60:
        return f'PT{minutes_int}M'
    hours = int(minutes_int / 60)
    minutes = minutes_int % 60
    if hours < 24:
        return f'PT{hours}H{minutes}M'
    days = int(hours / 24)
    hours = hours % 24
    return f'P{days}DT{hours}H{minutes}M'

def initialize_jsonld(recipe):
    jsonld = '{'
    jsonld += \
f"""
{jsonIndent}"@context": "https://schema.org/",
{jsonIndent}"@type": "Recipe",
{jsonIndent}"name": "{escape_json(recipe.name)}",
{jsonIndent}"datePublished": "{recipe.date_created}",
{jsonIndent}"description": "{escape_json(recipe.description)}",
"""
    if recipe.image:
        jsonld += \
f"""
{jsonIndent}"image": [
{2*jsonIndent}"{base_url}/images/{recipe.image}",
{2*jsonIndent}"{base_url}/images/thumbnails/{recipe.image}"
{jsonIndent}],
"""
    if recipe.yields:
        yield_as_string = ''
        for yield_data in recipe.yields:
            if yield_data.qualification:
                yield_as_string += f' {yield_data.qualification}:'
            yield_as_string += f' {yield_data.amount} {yield_data.unit}.'
        yield_as_string = escape_json(yield_as_string.strip())
        jsonld += f'{jsonIndent}"recipeYield": "{yield_as_string}",\n'

    if recipe.time:
        jsonld += f'{jsonIndent}"totalTime":' + ' {\n'
        jsonld += f'{2*jsonIndent}"min": "{convert_minutes_to_iso8601_duration(recipe.time.lower_bound)}",\n'
        jsonld += f'{2*jsonIndent}"max": "{convert_minutes_to_iso8601_duration(recipe.time.upper_bound)}"\n'
        jsonld += f'{jsonIndent}' + "},\n"

    return jsonld

# TODO add author (@type Persons , can I add us both?)
# TODO remove newlines from description
# TODO add keywords, category, cuisine
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
        ingredients.append(f'{2*jsonIndent}"{escape_json(ingr_string)}"')
    jsonld += ',\n'.join(ingredients)
    jsonld += f'\n{jsonIndent}],\n'
    return jsonld

def add_steps(recipe, jsonld):
    # If we ever get multiple part recipes, look at adding HowToSections
    jsonld += f'{jsonIndent}"recipeInstructions": [\n'
    steps = []
    for step in recipe.steps:
        step_string = f'{2*jsonIndent}' + '{\n' + f'{3*jsonIndent}"@type": "HowToStep",\n'
        if step.long != '':
            step_string += f'{3*jsonIndent}"name": "{escape_json(step.short)}",\n'
            step_string += f'{3*jsonIndent}"text": "{escape_json(step.long)}"'
        else:
            step_string += f'{3*jsonIndent}"text": "{escape_json(step.short)}"'
        step_string += f',\n{3*jsonIndent}"url": "{base_url}/recipes/{recipe.url_name}.html#step_{step.id}"'
        timeRequired = step.time.active + step.time.passive
        if timeRequired > 0:
            step_string += f',\n{3*jsonIndent}"timeRequired": "{convert_minutes_to_iso8601_duration(timeRequired)}"'
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
