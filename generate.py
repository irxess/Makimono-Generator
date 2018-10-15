import os
from jinja2 import Template, Environment, FileSystemLoader
import lesscpy
import yaml
from PIL import Image
import timeline

# TODO add the description

class Ingredient:
    def __init__(self, amount):
        self.amount = amount
        self.rest_id = -1

class Thumbnail:
    def __init__(self, name, url, img, date):
        self.name = name
        self.url = '../'+url
        self.image = '../images/thumbnails/'+img
        self.date = date

class PaginationElement:
    def __init__(self, page_url, number):
        self.url = page_url
        self.current = False
        self.name = number

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
        print("*** Warning *** No image found for", yaml['recipe'], "\n  * Expecting", img_name + ".{png,jpg,jpeg}")
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
    svg = timeline.generate_svg(yaml_result)

    if not os.path.isdir('publish'):
        os.makedirs('publish')
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('recipe.html')
    # TODO Website will display "None" if description for a recipe is empty.
    output = template.render(r=yaml_result, path_to_base='.', all_recipes_path='all/page1.html')
    with open('publish/' + name + '.html', 'w') as f:
        print(output, file=f)
    return Thumbnail(yaml_result['recipe'], './'+name+'.html', yaml_result['image'], yaml_result['date'])


def split_thumbnail_list_into_pages(thumbnails):
    chunk_size = 4
    list_of_thumbnail_chunks = []
    pagination_list = []
    chunk_number = 1
    for i in range(0, len(thumbnails), chunk_size):
        list_of_thumbnail_chunks.append( thumbnails[i:i+chunk_size] )
        pagination_list.append( PaginationElement('page'+str(chunk_number)+'.html', chunk_number) )
        chunk_number += 1
    return list_of_thumbnail_chunks, pagination_list


def generate_browse_page(thumbnails):
    # TODO Add description on hover?
    thumbnails.sort(key=lambda t: t.date)
    thumbnails = thumbnails + thumbnails + thumbnails + thumbnails + thumbnails
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('list_of_all_recipes.html')
    if not os.path.isdir('publish/all'):
        os.makedirs('publish/all')

    thumbnail_chunks, pagination_list = split_thumbnail_list_into_pages(thumbnails)
    prev_page = PaginationElement('#', 1)
    for i in range(0,len(pagination_list)):
        thumbnails = thumbnail_chunks[i]
        current_page = pagination_list[i]
        current_page.current = True
        if (i<len(pagination_list)-1):
            next_page = pagination_list[i+1]
        else:
            next_page = PaginationElement('#', len(pagination_list))
        output = template.render(
            chunk_of_thumbnails = thumbnails,
            paginated_pages = pagination_list,
            previous_page = prev_page,
            next_page = next_page,
            path_to_base='..',
            all_recipes_path='all/page1.html',
        )
        with open('publish/all/page'+str(i+1)+'.html', 'w') as f:
            print(output, file=f)
        current_page.current = False
        prev_page = current_page


if __name__ == "__main__":
    thumbnails = []
    if not os.path.isdir('publish/images/thumbnails'):
        os.makedirs('publish/images/thumbnails')
    for filename in os.listdir('recipes'):
        name = filename.split('.')[0]
        if name != 'template':
            print("Generating files for", filename)
            t = generate_files_for_recipe(name)
            thumbnails.append(t)
    print("Generating browse pages")
    if not os.path.isdir('publish/all'):
        os.makedirs('publish/all')
    generate_browse_page(thumbnails)

    print("Generating CSS")
    if not os.path.isdir('publish/css'):
        os.makedirs('publish/css')
    compiled_css = lesscpy.compile(open('templates/main.less', 'r'))
    with open('publish/css/main.css', 'w') as f:
        print(compiled_css, file=f)

