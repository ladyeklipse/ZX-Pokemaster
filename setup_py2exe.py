from classes.sorter import *
from distutils.core import setup
import py2exe
import sys
sys.path.append("ui")
if __name__ == '__main__':
    sys.argv.append('py2exe')

setup(
    options=
    {'py2exe':
        {
        'bundle_files': 1,
        'compressed': True,
        'includes':['sip']
        }
    },
    windows=[
        {
            'script': "pokemaster.py",
            'icon_resources':[(0, 'pokemaster.ico')]
        }
    ],
    data_files = [
        ('', ['README.txt',
              'pokemaster.db'])
    ],
    zipfile=None,
)