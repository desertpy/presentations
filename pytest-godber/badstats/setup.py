try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

config = {
    'description': 'Sample Stats module for test demonstration purposes.',
    'author': 'Austin Godber',
    'author_email': 'godber@uberhip.com',
    'version': '0.1',
    'packages': ['badstats'],
    'name': 'badstats'
}

setup(**config)
