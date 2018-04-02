import os
from jinja2 import Template, Environment, FileSystemLoader
import lesscpy
import yaml

class Ingredient:
     def __init__(self, amount):
          self.amount = amount
          self.rest_id = -1

def add_ingredient_amounts_to_steps(yaml):
    ingredients = dict()
    for ingr in yaml['ingredients']:
        ingredients[ ingr['id'] ] = Ingredient( ingr['amount'] )
    for s in yaml['steps']:
        for i in s['ingredients']:
            if 'amount' in i:
                ingredients[i['id']].amount -= i['amount']
            else:
                if ingredients[i['id']].rest_id == -1:
                    ingredients[i['id']].rest_id = i
                else:
                    print("Ingredient ", i['id'], " in ", yaml.recipe, " has multiple unspecified steps")
                    # TODO: throw error to be caught in the going through recipes loop
    for _,i in ingredients.items():
        if i.rest_id != -1:
            i.rest_id['amount'] = i.amount


if __name__ == "__main__":
    recipe = open('recipes/creme_suisse.yaml', 'r')
    yaml_result = yaml.load(recipe)
    add_ingredient_amounts_to_steps(yaml_result)

    if not os.path.isdir('publish'):
        os.makedirs('publish')
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('recipe.html')
    output = template.render(r=yaml_result)
    with open('publish/generated_recipe.html', 'w') as f:
        print(output, file=f)

    if not os.path.isdir('publish/css'):
        os.makedirs('publish/css')
    compiled_css = lesscpy.compile(open('templates/main.less', 'r'))
    with open('publish/css/main.css', 'w') as f:
        print(compiled_css, file=f)

