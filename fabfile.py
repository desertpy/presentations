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

def clean():
    """Cleans up the build directory"""
    local("rm -r output")

def build():
    """Builds the presentation provided"""

    # Setup build directory
    local("mkdir -p output")
    local("echo presentations.desertpy.com > output/CNAME")

    # Fabric by godber
    local("mkdir -p output/fabric-godber")
    local("landslide -i fabric-godber/presentation.rst -d output/fabric-godber/index.html")

    # Python and MongoDB by wtolson
    local("cp -r python-and-mongodb output/")

def publish():
    """Publish the static content to Github Pages"""
    local("ghp-import -p output/")
