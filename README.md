# Makimono
Generate static webpages from YAML files for a foodblog

# Setup

Make sure python (at least v 3.7) and the neccessary python packages are installed:

## Windows

### Using python virtual environment

Official docs per 2020-02-15 for venv can be found here:
https://packaging.python.org/guides/installing-using-pip-and-virtual-environments/

To set up the virtual environment:

`python -m venv path/to/repo-directory/`

To start the virtual environment:

`./Scripts/activate`

After you are done working with the project, you can exit the virtual environment by running:

`deactivate`

To install the packages specified in the requirements-file:

`pip install -r requirements.txt`

### When not using virtual environments

(Might have to run from shell started as admin due to lack of suitable sudo functionality.)

> python -m pip install pyyaml jinja2 lesscpy pillow

## Other OSs

> pip install pyyaml jinja2 lesscpy pillow

# Generating the content

Run generate.py:

> python generate.py

This will create a 'publish'-folder, which can be used as root for the published site.

Note that if you are using virtual environments, this should be executed while the virtual environment is active.
