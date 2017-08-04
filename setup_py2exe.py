# import _memimporter
# _memimporter.get_verbose_flag = lambda: 2
from settings import *
# from classes.sorter import *
from distutils.core import setup
import py2exe
import sys
import os
import zipfile
sys.path.append("ui")
sys.path.append("classes")
sys.path.append("functions")
if __name__ == '__main__':
    sys.argv.append('py2exe')

setup(
    options=
    {'py2exe':
        {
        'bundle_files': 1,
        'compressed': True,
        'includes':['sip', 'PyQt4.QtCore', 'PyQt4.QtGui', '_ctypes'],
        # 'packages':['sorter']
        }
    },
    windows=[
        {
            'script': "pokemaster.py",
            'icon_resources':[(0, 'ui\\pokemaster.ico')]
        }
    ],
    data_files = [
        ('', ['README.txt',
              'pokemaster.db',
              'default_settings\\settings.json'
              ])
    ],
    zipfile=None,
)
zfname = '_'.join(('ZXPokemaster', sys.platform, ZX_POKEMASTER_VERSION))
zfpath = os.path.join('dist', zfname+'.zip')
with zipfile.ZipFile(zfpath, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('dist'):
        for file in files:
            if not file.endswith('.zip'):
                zf.write(os.path.join(root, file), file)