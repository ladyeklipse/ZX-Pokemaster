import sqlite3
import traceback
import os
import sys
import shutil
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
if os.path.exists('pokemaster.db'):
    os.unlink('pokemaster.db')
shutil.copy('zxdb/pokemaster_zxdb_only.db', 'pokemaster.db')