# Makimono
Generate static webpages from YAML files for a foodblog

# Setup

Make sure python (at least v 3.6) and the neccessary python packages are installed:

## Windows

(Might have to run from shell started as admin due to lack of suitable sudo functionality.)

> python -m pip install pyyaml jinja2 lesscpy pillow

## Other OSs

> pip install pyyaml jinja2 lesscpy pillow

# Generating the content

Run generate.py:

> python generate.py

This will create a 'publish'-folder, which can be used as root for the published site.
