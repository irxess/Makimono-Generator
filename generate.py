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
from jsonld import generate_jsonld
from sitemap import create_sitemap
from total_time_needed_for_recipe import calculate_total_time_needed

# TODO:
# Check that each ingredient is used at least once
# Check that each step (exept the last one) is dependent on
# Check that the duration is filled for each step
# Show the time each step takes, and the total time (rounded to hours?)

def remove_empty_lines(string):
    return "\n".join([s for s in string.splitlines() if s.strip()])


class Thumbnail:
    def __init__(self, name, url, img, updated, created):
        self.name = name
        self.url = get_url_friendly_name(url)
        if img != '':
            self.image = 'images/thumbnails/'+img
        else:
            self.image = ''
        self.updated = updated
        self.created = created

def get_url_friendly_name(name):
    return name.replace(' ', '-').replace('&', 'and').casefold()

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
    img_thumbnail = img_thumbnail.resize((200,200), Image.LANCZOS) # Note that Image.LANCZOS actually is Image.ANTIALIAS, they renamed it to be less descriptive for no good reason in pillow 10.0.0
    img_thumbnail.save("publish/images/thumbnails/" + file_name)


def generate_files_for_recipe(name):
    recipe = read_recipe_into_data(name)
    if recipe.not_ready_for_publish:
        print('Recipe not ready for publishing, skipping')
        return 'Skipped generating because not ready flag is set'

    prepare_image(recipe)
    timeline.generate_timeline_svg(recipe)
    recipe.url_name = get_url_friendly_name(name)
    calculate_total_time_needed(recipe)
    jsonld = generate_jsonld(recipe)

    if not os.path.isdir('publish/recipes'):
        os.makedirs('publish/recipes')
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('recipe.html.jinja')

    output = template.render(
        r=recipe,
        jsonld=jsonld,
        path_to_base='..',
        recipes_path='all/page-1.html',
        all_recipes_overview_path='all-recipes-overview.html',
        dilution_calculator_path='dilution_calculator.html',
        sous_vide_temperature_path='sous_vide_temperatures.html',
        sause_thickening_calculator_path='sause-thickening-calculator.html',
        about_path='about.html'
    )
    output = remove_empty_lines(output)
    with open('publish/recipes/' + recipe.url_name + '.html', 'w', encoding='utf-8') as f:
        print(output, file=f)
    return Thumbnail(
        recipe.name,
        'recipes/' + recipe.url_name + '.html', # Path to recipe from base used in pagination list
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
    chunk_size = 10 # This is the number of recipes that will be shown on the "All recipes"-page
    list_of_thumbnail_chunks = []
    pagination_list = []
    chunk_number = 1
    for i in range(0, len(thumbnails), chunk_size):
        list_of_thumbnail_chunks.append( thumbnails[i:i+chunk_size] )
        pagination_list.append( PaginationElement('all/page-'+str(chunk_number)+'.html', chunk_number) )
        chunk_number += 1
    return list_of_thumbnail_chunks, pagination_list


def generate_browse_page(thumbnails):
    thumbnails.sort(key=lambda t: t.updated, reverse=True) # Newest first
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('list_of_recipes.html.jinja')
    if not os.path.isdir('publish/all'):
        os.makedirs('publish/all')

    thumbnail_chunks, pagination_list = split_thumbnail_list_into_pages(thumbnails)

    # Make first page in list main landing page:
    current_page = pagination_list[0]
    current_page.current = True
    output = template.render(
        chunk_of_thumbnails = thumbnail_chunks[0],
        paginated_pages = pagination_list,
        previous_page = pagination_list[-1],
        next_page = pagination_list[1],
        path_to_base='.',
        recipes_path='all/page-1.html',
        all_recipes_overview_path='all-recipes-overview.html',
        dilution_calculator_path='dilution_calculator.html',
        sous_vide_temperature_path='sous_vide_temperatures.html',
        sause_thickening_calculator_path='sause-thickening-calculator.html',
        about_path='about.html'
    )
    output = remove_empty_lines(output)
    with open('publish/index.html', 'w', encoding='utf-8') as f:
        print(output, file=f)

    for i in range(0,len(pagination_list)):
        thumbnails = thumbnail_chunks[i]
        current_page = pagination_list[i]
        current_page.current = True
        prev_page = pagination_list[i-1]
        if (i<len(pagination_list)-1):
            next_page = pagination_list[i+1]
        else:
            next_page = pagination_list[0]
        output = template.render(
            chunk_of_thumbnails = thumbnails,
            paginated_pages = pagination_list,
            previous_page = prev_page,
            next_page = next_page,
            path_to_base='..',
            recipes_path='all/page-1.html',
            all_recipes_overview_path='all-recipes-overview.html',
            dilution_calculator_path='dilution_calculator.html',
            sous_vide_temperature_path='sous_vide_temperatures.html',
            sause_thickening_calculator_path='sause-thickening-calculator.html',
            about_path='about.html'
        )
        output = remove_empty_lines(output)
        with open('publish/all/page-'+str(i+1)+'.html', 'w', encoding='utf-8') as f:
            print(output, file=f)
        current_page.current = False


def generate_all_recipes_overview_page(thumbnails):
    thumbnails.sort(key=lambda t: t.name)
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('all_recipes_overview.html.jinja')
    output = template.render(
        thumbnails = thumbnails,
        path_to_base='.',
        recipes_path='all/page-1.html',
        all_recipes_overview_path='all-recipes-overview.html',
        dilution_calculator_path='dilution_calculator.html',
        sous_vide_temperature_path='sous_vide_temperatures.html',
        sause_thickening_calculator_path='sause-thickening-calculator.html',
        about_path='about.html'
    )
    output = remove_empty_lines(output)
    with open('publish/all-recipes-overview.html', 'w', encoding='utf-8') as f:
        print(output, file=f)


def generate_about_page():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('about.html.jinja')
    if not os.path.isdir('publish'):
        os.makedirs('publish')

    output = template.render(
        path_to_base='.',
        recipes_path='all/page-1.html',
        all_recipes_overview_path='all-recipes-overview.html',
        dilution_calculator_path='dilution_calculator.html',
        sous_vide_temperature_path='sous_vide_temperatures.html',
        sause_thickening_calculator_path='sause-thickening-calculator.html',
        about_path='about.html'
    )
    output = remove_empty_lines(output)
    with open('publish/about.html', 'w', encoding='utf-8') as f:
        print(output, file=f)

def generate_dilution_calculator():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('dilution_calculator.html.jinja')
    if not os.path.isdir('publish'):
        os.makedirs('publish')

    output = template.render(
        path_to_base='.',
        recipes_path='all/page-1.html',
        all_recipes_overview_path='all-recipes-overview.html',
        dilution_calculator_path='dilution_calculator.html',
        sous_vide_temperature_path='sous_vide_temperatures.html',
        sause_thickening_calculator_path='sause-thickening-calculator.html',
        about_path='about.html'
    )
    output = remove_empty_lines(output)
    with open('publish/dilution_calculator.html', 'w', encoding='utf-8') as f:
        print(output, file=f)

def generate_sous_vide_temperatures():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('sous_vide_temperatures.html.jinja')
    if not os.path.isdir('publish'):
        os.makedirs('publish')

    output = template.render(
        path_to_base='.',
        recipes_path='all/page-1.html',
        all_recipes_overview_path='all-recipes-overview.html',
        dilution_calculator_path='dilution_calculator.html',
        sous_vide_temperature_path='sous_vide_temperatures.html',
        sause_thickening_calculator_path='sause-thickening-calculator.html',
        about_path='about.html'
    )
    output = remove_empty_lines(output)
    with open('publish/sous_vide_temperatures.html', 'w', encoding='utf-8') as f:
        print(output, file=f)

def generate_sauce_thickening_calculator():
    file_loader = FileSystemLoader('templates')
    env = Environment(loader=file_loader)
    template = env.get_template('sause-thickening-calculator.html.jinja')
    if not os.path.isdir('publish'):
        os.makedirs('publish')

    output = template.render(
        path_to_base='.',
        recipes_path='all/page-1.html',
        all_recipes_overview_path='all-recipes-overview.html',
        dilution_calculator_path='dilution_calculator.html',
        sous_vide_temperature_path='sous_vide_temperatures.html',
        sause_thickening_calculator_path='sause-thickening-calculator.html',
        about_path='about.html'
    )
    output = remove_empty_lines(output)
    with open('publish/sause-thickening-calculator.html', 'w', encoding='utf-8') as f:
        print(output, file=f)


if __name__ == "__main__":
    thumbnails = []
    if not os.path.isdir('publish/images/thumbnails'):
        os.makedirs('publish/images/thumbnails')

    from rename_files_in_folder_to_lower_case import rename_files_in_folder_to_lower_case
    rename_files_in_folder_to_lower_case('publish/images')

    print("Copying JS")
    if not os.path.isdir('publish/js'):
        os.makedirs('publish/js')
    shutil.copy('templates/recipe-scaling.js', 'publish/js/')
    shutil.copy('templates/ingredient-list-shopping-list-mode-enhancements.js', 'publish/js/')

    for filename in os.listdir('recipes'):
        if filename[0] != '.':
            name,extension = filename.split('.')
            if name != 'template' and extension == 'yaml':
                print("Generating files for", filename)
                t = generate_files_for_recipe(name)
                if t != 'Skipped generating because not ready flag is set':
                    thumbnails.append(t)

    print("Generating browse pages")
    if not os.path.isdir('publish/all'):
        os.makedirs('publish/all')
    generate_browse_page(thumbnails)

    print("Generating all recipes overview page")
    generate_all_recipes_overview_page(thumbnails)

    print("Generating about-page")
    generate_about_page()

    print("Generating dilution calculator page")
    generate_dilution_calculator()

    print("Generating sous vide temperatures page")
    generate_sous_vide_temperatures()

    print("Generating sauce thickening calculator page")
    generate_sauce_thickening_calculator()

    print("Generating CSS")
    if not os.path.isdir('publish/css'):
        os.makedirs('publish/css')
    compiled_css = lesscpy.compile(open('templates/styles/main.less', 'r', encoding='utf-8'), xminify=True)
    with open('publish/css/main.css', 'w', encoding='utf-8') as f:
        print(compiled_css, file=f)

    print("Copying svg icons")
    if not os.path.isdir('publish/images/icons'):
        os.makedirs('publish/images/icons')
    for icon in os.listdir('templates/icons'):
        shutil.copy('templates/icons/'+icon, 'publish/images/icons/'+icon)

    print("Copying robots.txt and generating sitemap")
    shutil.copy('templates/robots.txt', 'publish/')
    sitemap = create_sitemap(thumbnails)
    with open('publish/sitemap.xml', 'w', encoding='utf-8') as f:
        print(sitemap, file=f)
