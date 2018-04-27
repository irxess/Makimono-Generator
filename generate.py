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
        print("Amount:", ingr['amount'])
        if ingr['amount'] == None:
            ingr['amount'] = ''
            print("Amount:", ingr['amount'])
        ingredients[ ingr['id'] ] = Ingredient( ingr['amount'] )
    for s in yaml['steps']:
        if 'ingredients' in s:
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

def generate_files_for_recipe(name):
    #recipe = open('recipes/scones.yaml', 'r')
    recipe = open(os.path.join('recipes', name + '.yaml'), 'r')
    yaml_result = yaml.load(recipe)
    add_ingredient_amounts_to_steps(yaml_result)

    if not os.path.isdir('publish'):
        os.makedirs('publish')
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('recipe.html')
    output = template.render(r=yaml_result)
    print(name)
    with open('publish/' + name + '.html', 'w') as f:
        print(output, file=f)


if __name__ == "__main__":
    for filename in os.listdir('recipes'):
        name = filename.split('.')[0]
        if name != 'template':
            print("Generating files for", filename)
            generate_files_for_recipe(name)
    #recipe = open('recipes/creme_suisse.yaml', 'r')

    if not os.path.isdir('publish/css'):
        os.makedirs('publish/css')
    compiled_css = lesscpy.compile(open('templates/main.less', 'r'))
    with open('publish/css/main.css', 'w') as f:
        print(compiled_css, file=f)

