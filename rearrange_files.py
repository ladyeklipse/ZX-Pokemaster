import os
import shutil
from settings import *
for letter in ALPHABETIC_DIRNAMES:
    for dirname, dirnames, files in os.walk(os.path.join('wos_loading_screens', letter)):
        print(files, dirname, dirnames)
        for file in files:
            file_ext = os.path.splitext(file)[1]
            if file_ext == '.scr':
                dpath = os.path.join('wos_loading_screens', 'scr', letter)
            elif file_ext == '.gif':
                dpath = os.path.join('wos_loading_screens', 'gif', letter)
            fpath = os.path.join(dpath, file)
            if not os.path.exists(dpath):
                os.makedirs(dpath)
            shutil.move(os.path.join(dirname, file), fpath)
