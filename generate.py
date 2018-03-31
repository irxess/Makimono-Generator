import os
from jinja2 import Template, Environment, FileSystemLoader
import lesscpy
import yaml

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('recipe.html')

# load variables from YAML
recipe = open('recipes/creme_suisse.yaml', 'r')
yaml_result = yaml.load(recipe)
print(yaml_result.keys())

if not os.path.isdir('publish'):
	os.makedirs('publish')
output = template.render(r=yaml_result)
with open('publish/generated_recipe.html', 'w') as f:
	print(output, file=f)
if not os.path.isdir('publish/css'):
	os.makedirs('publish/css')
compiled_css = lesscpy.compile(open('templates/main.less', 'r'))
with open('publish/css/main.css', 'w') as f:
	print(compiled_css, file=f)
