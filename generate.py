import os
from jinja2 import Template, Environment, FileSystemLoader
import lesscpy
import yaml
from PIL import Image
import timeline
import shutil

# TODO:
# Create mortar icon
# Image resizing: 70$ progressive jpg
# Add source "adapted from" if exists and not empty in yaml and if url
# Show the optional ingredient notes
# Check that each ingredient is used at least once
# Check that each step (exept the last one) is dependent on
# Check that the duration is filled for each step
# Ingredient scaling for non-gram units
# Show the time each step takes, and the total time (rounded to hours?)

# Add description on hover in browse all?
# Generic thumbnail if no image?

class Ingredient:
    def __init__(self, amount):
        self.amount = amount
        self.rest_id = -1

class Thumbnail:
    def __init__(self, name, url, img, date):
        self.name = name
        self.url = '../'+url
        if img != '':
            self.image = '../images/thumbnails/'+img
        else:
            self.image = ''
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
    for _,i in ingredients.items():
        if i.rest_id != -1:
            i.rest_id['amount'] = i.amount

def prepare_image(yaml):
    img_name = yaml['image']
    known_image_extensions = ['jpg', 'JPG', 'png', 'PNG', '.jpeg', 'JPEG']
    file_name = ""
    for extension in known_image_extensions:
        if os.path.isfile("publish/images/" + img_name + '.' + extension):
            file_name = img_name + '.' + extension
            break;
    if file_name == "":
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
    timeline.generate_svg(yaml_result)

    if not os.path.isdir('publish'):
        os.makedirs('publish')
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('recipe.html')

    output = template.render(
        r=yaml_result,
        path_to_base='.',
        all_recipes_path='all/page1.html',
        about_path='about.html'
    )
    with open('publish/' + name + '.html', 'w') as f:
        print(output, file=f)
    return Thumbnail(
        yaml_result['recipe'],
        './'+name+'.html',
        yaml_result['image'],
        yaml_result['date']
    )


def split_thumbnail_list_into_pages(thumbnails):
    chunk_size = 4 # This is the number of recipes that will be shown on the "All recipes"-page
    list_of_thumbnail_chunks = []
    pagination_list = []
    chunk_number = 1
    for i in range(0, len(thumbnails), chunk_size):
        list_of_thumbnail_chunks.append( thumbnails[i:i+chunk_size] )
        pagination_list.append( PaginationElement('page'+str(chunk_number)+'.html', chunk_number) )
        chunk_number += 1
    return list_of_thumbnail_chunks, pagination_list


def generate_browse_page(thumbnails):
    thumbnails.sort(key=lambda t: t.date)
    # Uncomment the following line to get more items in the "All recipes"-page. Usefull when debugging the pagination.
    # thumbnails = thumbnails + thumbnails + thumbnails + thumbnails + thumbnails # Pagination debugging
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
            about_path='about.html'
        )
        with open('publish/all/page'+str(i+1)+'.html', 'w') as f:
            print(output, file=f)
        current_page.current = False
        prev_page = current_page


def generate_about_page():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('about.html')
    if not os.path.isdir('publish'):
        os.makedirs('publish')

    output = template.render(
        path_to_base='.',
        all_recipes_path='all/page1.html',
        about_path='about.html'
    )

    with open('publish/about.html', 'w') as f:
        print(output, file=f)


if __name__ == "__main__":
    thumbnails = []
    if not os.path.isdir('publish/images/thumbnails'):
        os.makedirs('publish/images/thumbnails')
    for filename in os.listdir('recipes'):
        if filename[0] != '.':
            name,extension = filename.split('.')
            if name != 'template' and extension == 'yaml':
                print("Generating files for", filename)
                t = generate_files_for_recipe(name)
                thumbnails.append(t)

    print("Generating browse pages")
    if not os.path.isdir('publish/all'):
        os.makedirs('publish/all')
    generate_browse_page(thumbnails)

    print("Generating about-page")
    generate_about_page()
    shutil.copy('publish/about.html', 'publish/index.html')

    print("Generating CSS")
    if not os.path.isdir('publish/css'):
        os.makedirs('publish/css')
    compiled_css = lesscpy.compile(open('templates/main.less', 'r'))
    with open('publish/css/main.css', 'w') as f:
        print(compiled_css, file=f)

    print("Copying svg icons")
    if not os.path.isdir('publish/images/icons'):
        os.makedirs('publish/images/icons')
    for icon in os.listdir('templates/icons'):
        shutil.copy('templates/icons/'+icon, 'publish/images/icons/'+icon)
