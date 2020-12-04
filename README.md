# Makimono

Generate static webpages from YAML files for a foodblog.

You can find it at https://makimo.no/

# Setup

Make sure python (at least v 3.7) and the neccessary python packages are installed:

## Windows

### Using python's virtual environment

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

## Other OSs (tested on Linux)

### Using python's virtual environment

To set up the virtual environment:

`python -m venv venv_name`

To start the virtual environment:

`source venv_name/bin/activate`

To install the packages specified in the requirements-file:

`pip install -r requirements.txt`

After you are done working with the project, you can exit the virtual environment by running:

`deactivate`

### When not using virtual environments

> pip install pyyaml jinja2 lesscpy pillow

# Generating the content

Run generate.py:

> python generate.py

This will create a 'publish'-folder, which can be used as root for the published site.

Note that if you are using virtual environments, this should be executed while the virtual environment is active.

## Images

Note that the images referenced in the recipe files have to be places in the `publish/images/` folder.
You can create the `publish/images/` directory before you do the first generating.
The reason for this is that we do not want to bloat the git repository with binaries, and you will need to sort out the storage when you push the generated content anywhere anyways.

Beware that the referenced images have to be present before you run the generation, otherwise the thumbnail generating code will fail.
