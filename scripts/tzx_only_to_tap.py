import os
import sys
import subprocess
import zipfile
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

from classes.database import *

db = Database('pokemaster_v1.5-alpha3.db')
# games = db.getAllGames()
games = db.getAllGames("game.zxdb_id=2176")
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
        # print("TZX without TAP found:", game)
        for game_file in game.getFiles():
            if game_file.format == 'tzx':
                # if game_file.wos_path:
                #     key = 'ftp' + game_file.wos_path
                # elif game_file.tosec_path:
                #     key = game_file.tosec_path
                #     if not key.startswith('tosec'):
                #         key = 'tosec/'+key
                # if not os.path.exists(key): #tzx should be unzipped first:
                #     print(key, "does not exist")
                #     key = key.lower().replace('.tzx', '.zip')
                #     print("will open", key)
                #     with zipfile.ZipFile(key) as zf:
                #         if game_file.wos_name:
                #             data = zf.read(game_file.wos_name)
                #         else:
                #             data = zf.read(os.path.basename(game_file.tosec_path))
                #         key = key.replace('.zip', 'tzx')
                #         with open(key, 'wb') as f:
                #             f.write(data)
                #             print("saved", key)
                # if not os.path.exists(key):
                key = 'sorted/tzx_only/' + game_file.getOutputName("{Type}\\{TOSECName}")
                if not os.path.exists(key):
                    print(key, "does not exist.")
                value = os.path.join('tosec', 'reviewed files', 'tzx2tap',
                                     game_file.getOutputName("{Type}\\{TOSECName}").replace('.tzx', '[m tzxtools].tap'))
                # print(value)
                conversion_list[key]=value
# print(conversion_list)
print(len(conversion_list))
# sys.exit()
existing_tap_convertions = [value for value in conversion_list.values() if os.path.exists(value)]
for root, dirs, files in os.walk("tosec\\reviewed files\\tzx2tap"):
    for file in files:
        path = os.path.join(root, file)
        for value in existing_tap_convertions:
            if os.path.abspath(path)==os.path.abspath(value):
                print("Should delete", value)
sys.exit()
for key, value in conversion_list.items():
    os.makedirs(os.path.dirname(value), exist_ok=True)
    if os.path.exists(value):
        if os.path.getsize(value):
            # print("will skip", value)
            continue
        else: #size=0
            os.unlink(value)
    command = 'tzxtap "{}" -o "{}" --ignore'.format(key, value)
    print(command)
    # continue
    s = subprocess.Popen(command)
    s.communicate()
    if not os.path.exists(value):
        print("Failed to create", value)
    elif not os.path.getsize(value):
        print("Failed to convert", key)
        os.unlink(value)
    else:
        print("Successfully created:", value)
