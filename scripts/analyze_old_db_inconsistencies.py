from classes.database import *
import os
if (os.getcwd().endswith('scripts')):
    os.chdir('..')


def showDeletedFiles(old_database_path, new_database_path='pokemaster.db'):
    new_db = Database(new_database_path)
    old_db = Database(old_database_path)
    old_db.loadCache()
    new_db.loadCache()
    deleted_files = 0
    for md5 in old_db.cache_by_md5.keys():
        if md5 in new_db.cache_by_md5.keys():
            continue
        else:
            game = old_db.getGameByFileMD5(md5)
            game_file = game.findFileByMD5(md5)
            print(game_file.wos_name, game_file.wos_path, game_file.tosec_path)
            deleted_files +=1
    print("Deleted", deleted_files, "files")

def restoreDeletedFiles(old_database_path):
    new_db = Database()
    old_db = Database(old_database_path)
    old_db.loadCache()
    new_db.loadCache()
    for md5 in old_db.cache_by_md5.keys():
        if md5 in new_db.cache_by_md5.keys():
            continue
        else:
            sql = "SELECT * FROM game_file WHERE md5=\"{}\"".format(md5)
            row = list(old_db.conn.execute(sql).fetchone())
            print(row)
            wos_id = row[0]
            if wos_id not in new_db.cache_by_wos_id:
                print("GAME ", wos_id, "WAS DELETED")
                continue
            sql = "INSERT INTO game_file VALUES " \
                  "({})".format(','.join(['?'] * len(row)))
            new_db.cur.execute(sql, row)
            print("executed.")
    new_db.conn.commit()


def diffDatabases(old_database_path, new_database_path='pokemaster.db'):
    new_db = Database(new_database_path)
    old_db = Database(old_database_path)
    old_db.loadCache()
    new_db.loadCache()
    for md5 in new_db.cache_by_md5.keys():
        new_game = new_db.cache_by_md5[md5]
        new_game_file = new_game.findFileByMD5(md5)
        new_tosec_name = new_game_file.getTOSECName()
        old_game =  old_db.cache_by_md5.get(md5)
        if not old_game:
            print('Added:', new_tosec_name)
            continue
        old_game_file = old_game.findFileByMD5(md5)
        old_tosec_name = old_game_file.getTOSECName()
        if new_tosec_name != old_tosec_name:
            print('Renamed:', old_tosec_name, '->', new_tosec_name)

if __name__=='__main__':
    # showDeletedFiles('pokemaster_v1.3-beta6.db')
    # restoreDeletedFiles('pokemaster_v1.3-beta6.db')
    # showDeletedFiles('pokemaster_v1.3-beta6.db')
    # diffDatabases('pokemaster_v1.4-alpha2.db')
    diffDatabases('pokemaster_v1.3-beta6.db')