import os, subprocess
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
                key = 'ftp' + game_file.wos_path if game_file.wos_path else \
                        game_file.tosec_path
                value = os.path.join('tosec', 'reviewed_files', 'tzx2tap', game_file.getTOSECName().replace('.tzx', '.tap'))
                conversion_list[key]=value
print(conversion_list)
print(len(conversion_list))
for key, value in conversion_list.items():
    s = subprocess.Popen('tzxtap "{}" -o "{}"'.format(key, value))
    s.communicate()