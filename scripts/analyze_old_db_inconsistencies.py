from classes.database import *
import os
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

def analyze():
    new_db = Database()
    old_db = Database('pokemaster_v1.21.db')
    old_db.loadCache()
    new_db.loadCache()
    for md5 in old_db.cache_by_md5.keys():
        if md5 in new_db.cache_by_md5.keys():
            continue
        else:
            game = old_db.getGameByFileMD5(md5)
            game_file = game.findFileByMD5(md5)
            print(game_file.wos_name, game_file.wos_path, game_file.tosec_path)

if __name__=='__main__':
    analyze()