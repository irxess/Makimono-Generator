import os
from jinja2 import Template, Environment, FileSystemLoader
import lesscpy
import yaml
from PIL import Image

class Ingredient:
    def __init__(self, amount):
        self.amount = amount
        self.rest_id = -1

class Thumbnail:
    def __init__(self, name, url, img, date):
        self.name = name
        self.url = url
        self.image = img
        self.date = date

def add_ingredient_amounts_to_steps(yaml):
    ingredients = dict()
    for ingr in yaml['ingredients']:
        if ingr['amount'] == None:
            ingr['amount'] = ''
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

def prepare_image(yaml):
    img_name = yaml['image']
    if os.path.isfile( "publish/images/" + img_name + ".png"):
        file_name = img_name + '.png'
    elif os.path.isfile( "publish/images/" + img_name + ".jpg"):
        file_name = img_name + '.jpg'
    elif os.path.isfile( "publish/images/" + img_name + ".jpeg"):
        file_name = img_name + '.jpeg'
    else:
        print("Warning: No image found for", yaml['recipe'], "\nExpecting", img_name + ".{png,jpg,jpeg}")
        yaml['image'] = ""
        return ""
    yaml['image'] = file_name
    # generate thumbnail, if not exists
    img = Image.open("publish/images/" + file_name)

    # make image square
    center_x = img.size[0] / 2
    center_y = img.size[1] / 2
    if center_x < center_y:
        offset = center_x
    else:
        offset = center_y
    img_thumbnail = img.crop(
         (
              center_x - offset,
              center_y - offset,
              center_x + offset,
              center_y + offset
         )
    )

    # resize the square image
    img_thumbnail = img_thumbnail.resize((200,200), Image.ANTIALIAS)
    img_thumbnail.save("publish/images/thumbnails/" + file_name)

    return file_name


def generate_files_for_recipe(name):
    recipe = open(os.path.join('recipes', name + '.yaml'), 'r')
    yaml_result = yaml.load(recipe)
    add_ingredient_amounts_to_steps(yaml_result)
    prepare_image(yaml_result)

    if not os.path.isdir('publish'):
        os.makedirs('publish')
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('recipe.html')
    output = template.render(r=yaml_result)
    with open('publish/' + name + '.html', 'w') as f:
        print(output, file=f)
    return Thumbnail(yaml_result['recipe'], './'+name+'.html', yaml_result['image'], yaml_result['date'])


def generate_browse_page(thumbnails):
    thumbnails.sort(key=lambda t: t.date)
    for t in thumbnails:
        print(t.name, "has date", t.date)

if __name__ == "__main__":
    thumbnails = []
    for filename in os.listdir('recipes'):
        name = filename.split('.')[0]
        if name != 'template':
            print("Generating files for", filename)
            t = generate_files_for_recipe(name)
            thumbnails.append(t)
    generate_browse_page(thumbnails)

    if not os.path.isdir('publish/css'):
        os.makedirs('publish/css')
    compiled_css = lesscpy.compile(open('templates/main.less', 'r'))
    with open('publish/css/main.css', 'w') as f:
        print(compiled_css, file=f)

