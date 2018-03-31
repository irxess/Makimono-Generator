import os
from jinja2 import Template, Environment, FileSystemLoader
import yaml

file_loader = FileSystemLoader('templates')
env = Environment(loader=file_loader)

template = env.get_template('recipe.html')

# load variables from YAML
recipe = open('recipes/creme_suisse.yaml', 'r')
yaml_result = yaml.load(recipe)
print(yaml_result.keys())

output = template.render(r=yaml_result)
if not os.path.isdir("publish"):
	os.makedirs("publish")
with open('publish/generated_recipe.html', 'w') as f:
	print(output, file=f)
