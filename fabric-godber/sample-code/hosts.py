from fabric.api import run
from fabric.decorators import hosts

@hosts('monk','zag.local','europa.local')
def name():
    """Print out the hostname and system information"""
    run('hostname')
    run('uname -a')
