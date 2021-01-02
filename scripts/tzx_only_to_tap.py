import os
import sys
import subprocess
import zipfile
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

from classes.database import *

db = Database()
games = db.getAllGames()
print(len(games))
conversion_list = {}
for game in games:
    tzx_found = False
    tap_found = False
    if game.name.startswith('ZZZ-UNK'):
        continue
    for game_file in game.getFiles():
        if game_file.format == 'tap':
            tap_found = True
        elif game_file.format == 'tzx':
            tzx_found = True
    if tzx_found and not tap_found:
        print("TZX without TAP found:", game)
        for game_file in game.getFiles():
            if game_file.format == 'tzx':
                if game_file.wos_path:
                    key = 'ftp' + game_file.wos_path
                elif game_file.tosec_path:
                    key = game_file.tosec_path
                    if not key.startswith('tosec'):
                        key = 'tosec/'+key
                if not os.path.exists(key): #tzx should be unzipped first:
                    print(key, "does not exist")
                    key = key.lower().replace('.tzx', '.zip')
                    print("will open", key)
                    with zipfile.ZipFile(key) as zf:
                        if game_file.wos_name:
                            data = zf.read(game_file.wos_name)
                        else:
                            data = zf.read(os.path.basename(game_file.tosec_path))
                        key = key.replace('.zip', 'tzx')
                        with open(key, 'wb') as f:
                            f.write(data)
                            print("saved", key)
                value = os.path.join('tosec', 'reviewed_files', 'tzx2tap', game_file.getTOSECName().replace('.tzx', '.tap'))
                conversion_list[key]=value
print(conversion_list)
print(len(conversion_list))
sys.exit()
for key, value in conversion_list.items():
    s = subprocess.Popen('tzxtap "{}" -o "{}"'.format(key, value))
    s.communicate()