from settings import *
from distutils.core import setup
import sys
import os
import zipfile
import py2exe
sys.path.append("ui")
sys.path.append("classes")
sys.path.append("functions")
if __name__ == '__main__':
    sys.argv.append('py2exe')
if os.path.exists(os.path.join('dist', POKEMASTER_DB_PATH)):
    os.remove(os.path.join('dist', POKEMASTER_DB_PATH))
setup(
    options=
    {'py2exe':
        {
        'bundle_files': 1,
        'compressed': True,
        'includes':['sip', 'PyQt4.QtCore', 'PyQt4.QtGui', '_ctypes'],
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
              POKEMASTER_MIN_DB_PATH,
              '7z.exe',
              '7z.dll',
              'default_settings\\settings.json'
              ])
    ],
    zipfile=None,
)
os.rename(os.path.join('dist', POKEMASTER_MIN_DB_PATH), os.path.join('dist', POKEMASTER_DB_PATH))
zfname = '_'.join(('ZXPokemaster', sys.platform, ZX_POKEMASTER_VERSION))
zfpath = os.path.join('dist', zfname+'.zip')
with zipfile.ZipFile(zfpath, 'w', zipfile.ZIP_DEFLATED) as zf:
    for root, dirs, files in os.walk('dist'):
        for file in files:
            if file.endswith('.zip'):
                continue
            elif file.endswith('.log'):
                continue
            else:
                zf.write(os.path.join(root, file), file)