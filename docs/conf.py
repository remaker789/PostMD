# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

import os
import sys

sys.path.insert(0,os.path.abspath(".."))  # must be .., ".." dir is D:\OneDrive\Github\MyRepos\PostMD




project = 'PostMD Documentation'
copyright = '2024, Shusong Zhang'
author = 'Shusong Zhang'
release = '0.0.3'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.todo",
    "sphinx.ext.viewcode",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon", # Google style docstring
    "sphinx_multiversion",
]

templates_path = ['_templates']
html_sidebars = {
    '**': [
        'versioning.html',
    ],
}
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']



# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']


# If true, the current module name will be prepended to all description
# unit titles (such as .. function::).
add_module_names = False