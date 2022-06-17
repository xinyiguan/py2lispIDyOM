# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path
from shutil import copy

sys.path.insert(0, os.path.abspath('../'))
sys.path.insert(0, os.path.abspath('.'))
sys.path.insert(0, os.path.abspath('..'))
sys.path.insert(0, os.path.abspath('../..'))

URL = "https://github.com/xinyiguan/py2lispIDyOM"

# -- Copy README file --------------------------------------------------------
# copy(Path("../README.md"), Path("./README.md"))

# -- ensure_pandoc_installed -------------------------------------------------
from inspect import getsourcefile

# Get path to directory containing this file, conf.py.
DOCS_DIRECTORY = os.path.dirname(os.path.abspath(getsourcefile(lambda: 0)))


def ensure_pandoc_installed(_):
    import pypandoc

    # Download pandoc if necessary. If pandoc is already installed and on
    # the PATH, the installed version will be used. Otherwise, we will
    # download a copy of pandoc into docs/bin/ and add that to our PATH.
    pandoc_dir = os.path.join(DOCS_DIRECTORY, "bin")
    # Add dir containing pandoc binary to the PATH environment variable
    if pandoc_dir not in os.environ["PATH"].split(os.pathsep):
        os.environ["PATH"] += os.pathsep + pandoc_dir
    pypandoc.ensure_pandoc_installed(
        targetfolder=pandoc_dir,
        delete_installer=True,
    )

def setup(app):
    app.connect("builder-inited", ensure_pandoc_installed)


# -- Copy tutorial files --------------------------------------------------------
copy(Path("../tutorials/1_running_IDyOM_tutorial.ipynb"), Path("./tutorials/1_running_IDyOM_tutorial.ipynb"))
copy(Path("../tutorials/2a_data_preprocessing_extracting.ipynb"),
     Path("./tutorials/2a_data_preprocessing_extracting.ipynb"))
copy(Path("../tutorials/2b_data_preprocessing_exporting.ipynb"),
     Path("./tutorials/2b_data_preprocessing_exporting.ipynb"))
copy(Path("../tutorials/3_visualizing_outputs.ipynb"), Path("./tutorials/3_visualizing_outputs.ipynb"))

# -- Project information -----------------------------------------------------
project = 'py2lispIDyOM'
copyright = '2022, Xinyi Guan'
author = 'Xinyi Guan'

# -- General configuration ---------------------------------------------------
# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser',
    'sphinx.ext.autodoc',
    'sphinx.ext.doctest',
    'sphinx.ext.autosummary',
    'sphinx_autodoc_typehints',
    'autoclasstoc',
    'sphinx.ext.viewcode',
    'nbsphinx',
    'sphinx_gallery.load_style'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build']

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = "pydata_sphinx_theme"
html_theme = 'sphinx_rtd_theme'
html_theme_options = {"show_prev_next": False, "github_url": URL}

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".

# html_static_path = ['_static']
root_doc = 'index'
