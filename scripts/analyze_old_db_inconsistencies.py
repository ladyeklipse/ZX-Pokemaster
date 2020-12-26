from classes.database import *
from classes.database_legacy import Database as OldDatabase
import os
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

def showDeletedFiles(old_database_path, new_database_path='pokemaster.db'):
    new_db = Database(new_database_path)
    if old_database_path>'pokemaster_v1.4-alpha6.db':
        old_db = Database(old_database_path)
    else:
        old_db = OldDatabase(old_database_path)
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
    if old_database_path>'pokemaster_v1.4-alpha6.db':
        old_db = Database(old_database_path)
    else:
        old_db = OldDatabase(old_database_path)
    old_db.loadCache()
    new_db.loadCache()
    for md5 in old_db.cache_by_md5.keys():
        if md5 in new_db.cache_by_md5.keys():
            continue
        else:
            sql = "SELECT * FROM game_file WHERE md5=\"{}\"".format(md5)
            row = list(old_db.conn.execute(sql).fetchone())
            print(row)
            zxdb_id = row[0]
            if zxdb_id not in new_db.cache_by_zxdb_id:
                print("GAME ", zxdb_id, "WAS DELETED")
                continue
            sql = "INSERT INTO game_file VALUES " \
                  "({})".format(','.join(['?'] * len(row)))
            new_db.cur.execute(sql, row)
            print("executed.")
    new_db.conn.commit()

def restoreUnknownTypes(old_database_path):
    new_db = Database()
    if old_database_path>'pokemaster_v1.4-alpha6.db':
        old_db = Database(old_database_path)
    else:
        old_db = OldDatabase(old_database_path)
    sql = "SELECT zxdb_id FROM game WHERE genre=''"
    zxdb_ids = new_db.conn.execute(sql).fetchall()
    for zxdb_id in zxdb_ids:
        sql = "SELECT genre FROM game WHERE wos_id={}".format(zxdb_id[0])
        print(sql)
        row = old_db.conn.execute(sql).fetchone()
        if not row:
            print("Genre not found for", zxdb_id)
        else:
            genre = row['genre']
            sql = "UPDATE game SET genre='{}' WHERE zxdb_id={}".format(genre, zxdb_id[0])
            print(sql)
            new_db.cur.execute(sql)
    # new_db.conn.commit()

def diffDatabases(old_database_path, new_database_path='pokemaster.db'):
    new_db = Database(new_database_path)
    if old_database_path>'pokemaster_v1.4-alpha6.db':
        old_db = Database(old_database_path)
    else:
        old_db = OldDatabase(old_database_path)
    old_db.loadCache()
    new_db.loadCache()
    for md5 in new_db.cache_by_md5.keys():
        new_game = new_db.cache_by_md5[md5]
        new_game_file = new_game.findFileByMD5(md5)
        new_tosec_name = new_game_file.getTOSECName()
        old_game =  old_db.cache_by_md5.get(md5)
        if not old_game:
            print('Added:', new_game.type + '/' + new_tosec_name)
            print(new_game.getSpectrumComputingURL())
            continue
        old_game_file = old_game.findFileByMD5(md5)
        old_tosec_name = old_game_file.getTOSECName()
        if old_game.type != new_game.type and new_tosec_name == old_tosec_name:
            print('Moved:', old_game.type + '/' + old_tosec_name, '->', new_game.type)
            print(new_game.getSpectrumComputingURL())
            # if new_game.type=='Unknown':
            #     print("Changed genre:", old_game.genre, '->', new_game.genre)
        elif old_game.type != new_game.type and new_tosec_name != old_tosec_name:
            print("Moved and renamed:", old_game.type + '/' + old_tosec_name, '->',
                  new_game.type + '/' + new_tosec_name)
            print(new_game.getSpectrumComputingURL())
            # if new_game.type == 'Unknown':
            #     print("Changed genre:", old_game.genre, '->', new_game.genre)
        elif new_tosec_name != old_tosec_name:
            print('Renamed:', old_game.type + '/' + old_tosec_name, '->', new_game.type + '/' + new_tosec_name)
            print(new_game.getSpectrumComputingURL())

if __name__=='__main__':
    diffDatabases('pokemaster_v1.4-RC1.db')
    # showDeletedFiles('pokemaster_v1.3-beta6.db')
    # restoreDeletedFiles('pokemaster_v1.3-beta6.db')
    # restoreUnknownTypes('pokemaster_v1.3-beta6.db')
    # showDeletedFiles('pokemaster_v1.3-beta6.db')
    # diffDatabases('pokemaster_v1.4-alpha9.db')
    # diffDatabases('pokemaster_v1.3-beta6.db')
    # showDeletedFiles('pokemaster_v1.4-alpha5.db')