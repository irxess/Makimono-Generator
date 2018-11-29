import os
from jinja2 import Template, Environment, FileSystemLoader
import lesscpy
import yaml
from PIL import Image
import timeline
import shutil
from dataclasses import dataclass
from read_from_yaml import read_recipe_into_data
from data import *

# TODO:
# Check that each ingredient is used at least once
# Check that each step (exept the last one) is dependent on
# Check that the duration is filled for each step
# Show the time each step takes, and the total time (rounded to hours?)

# Add description on hover in browse all?



class Thumbnail:
    def __init__(self, name, url, img, updated, created):
        self.name = name
        self.url = '../'+url
        if img != '':
            self.image = '../images/thumbnails/'+img
        else:
            self.image = ''
        self.updated = updated
        self.created = created

def prepare_image(recipe):
    img_name = recipe.image.casefold()
    known_image_extensions = ['jpg', 'png', 'jpeg']
    file_name = ""
    for extension in known_image_extensions:
        if os.path.isfile("publish/images/" + img_name + '.' + extension):
            file_name = img_name + '.' + extension
            break;
    if file_name == "":
        recipe.image = ""
        return ""
    recipe.image = file_name
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


def generate_files_for_recipe(name):
    recipe = read_recipe_into_data(name)

    prepare_image(recipe)
    timeline.generate_svg(recipe)

    if not os.path.isdir('publish'):
        os.makedirs('publish')
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('recipe.html')

    output = template.render(
        r=recipe,
        path_to_base='.',
        all_recipes_path='all/page-1.html',
        about_path='about.html'
    )
    with open('publish/' + name + '.html', 'w') as f:
        print(output, file=f)
    return Thumbnail(
        recipe.name,
        './'+recipe.name+'.html',
        recipe.image,
        recipe.date_updated,
        recipe.date_created,
    )


@dataclass
class PaginationElement:
    url: str = ""
    name: str = ""
    current = False

def split_thumbnail_list_into_pages(thumbnails):
    chunk_size = 4 # This is the number of recipes that will be shown on the "All recipes"-page
    list_of_thumbnail_chunks = []
    pagination_list = []
    chunk_number = 1
    for i in range(0, len(thumbnails), chunk_size):
        list_of_thumbnail_chunks.append( thumbnails[i:i+chunk_size] )
        pagination_list.append( PaginationElement('page-'+str(chunk_number)+'.html', chunk_number) )
        chunk_number += 1
    return list_of_thumbnail_chunks, pagination_list


def generate_browse_page(thumbnails):
    thumbnails.sort(key=lambda t: t.updated, reverse=True) # Newest first
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
            all_recipes_path='all/page-1.html',
            about_path='about.html'
        )
        with open('publish/all/page-'+str(i+1)+'.html', 'w') as f:
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
        all_recipes_path='all/page-1.html',
        about_path='about.html'
    )

    with open('publish/about.html', 'w') as f:
        print(output, file=f)


if __name__ == "__main__":
    thumbnails = []
    if not os.path.isdir('publish/images/thumbnails'):
        os.makedirs('publish/images/thumbnails')

    from rename_files_in_folder_to_lower_case import rename_files_in_folder_to_lower_case
    rename_files_in_folder_to_lower_case('publish/images')

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
