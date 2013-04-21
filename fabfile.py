from fabric.api import local
from fabric.operations import prompt
import os


def create():
    """Creates a new presentation subdirectory"""
    presentation_name = prompt('Presentation Short Name: ')
    author_name = prompt('Author Short Name: ')
    dirname = presentation_name.replace(' ', '_') + '-' + author_name.replace(' ', '_')
    if not os.path.exists(dirname):
        os.makedirs(dirname)


def build():
    """Builds the presentation provided"""
    local("landslide -i fabric-godber/presentation.rst -d output/fabric-godber/index.html")
