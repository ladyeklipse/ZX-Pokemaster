from classes.database import *
from classes.database_legacy import Database as OldDatabase
import os
import difflib

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
    if old_database_path.lower()>'pokemaster_v1.4-alpha6.db':
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
            if row[2]: #wos_name is present:
                row.insert(16, 0) #priority=0
            else:
                row.insert(16,1) #priority=1
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
    if not os.path.exists(old_database_path):
        print("DATABASE", old_database_path, "DOES NOT EXIST.")
        return None
    new_db = Database(new_database_path)
    if old_database_path>'pokemaster_v1.4-alpha6.db':
        old_db = Database(old_database_path)
    else:
        old_db = OldDatabase(old_database_path)
    old_db.loadCache()
    new_db.loadCache()
    f_old = open("sandbox/old.txt", 'w', encoding='utf-8')
    f_new = open("sandbox/new.txt", 'w', encoding='utf-8')
    renamed_tap_conversions = 0
    for md5 in new_db.cache_by_md5.keys():
        new_game = new_db.cache_by_md5[md5]
        new_game_file = new_game.findFileByMD5(md5)
        new_tosec_name = new_game_file.getTOSECName()
        old_game =  old_db.cache_by_md5.get(md5)
        new_record = new_game.type + '/' + new_tosec_name
        if not old_game:
            print('Added:', new_record)#new_game.type + '/' + new_tosec_name)
            print(new_game.getSpectrumComputingURL())
            f_old.write('\n')
            f_new.write(new_record + '\n')
            continue
        old_game_file = old_game.findFileByMD5(md5)
        old_tosec_name = old_game_file.getTOSECName()
        old_record = old_game.type + '/' + old_tosec_name
        if old_game.type != new_game.type and new_tosec_name == old_tosec_name:
            print('Moved:', old_record, '->', new_game.type)
            print(new_game.getSpectrumComputingURL())
            f_old.write(old_record + '\n')
            f_new.write(new_record + '\n')
        elif old_game.type != new_game.type and new_tosec_name != old_tosec_name:
            print("Moved and renamed:", old_record, '->',
                  new_record)
            print(new_game.getSpectrumComputingURL())
            f_old.write(old_record + '\n')
            f_new.write(new_record + '\n')
        elif new_tosec_name != old_tosec_name:
            print('Renamed:', old_record, '->', new_record)
            print(new_game.getSpectrumComputingURL())
            if '[m tzxtools]' in new_record:
                renamed_tap_conversions += 1
            f_old.write(old_record + '\n')
            f_new.write(new_record + '\n')
    f_old.close()
    f_new.close()
    print("renamed tap conversions:", renamed_tap_conversions)

def generateDiffFiles(old_db_name, new_db_name):
    f_old = open("sandbox/old.txt", 'r', encoding='utf-8')
    f_new = open("sandbox/new.txt", 'r', encoding='utf-8')
    f_old_contents = f_old.read()
    f_new_contents = f_new.read()
    print("contents read.")
    diff_file_contents = difflib.HtmlDiff(wrapcolumn=50).make_file(
        f_old_contents,
        f_new_contents,
        context=False, numlines=0)
    f_old.close()
    f_new.close()
    with open("sandbox/diff.html", "w", encoding="utf-8") as f:
        f.write(diff_file_contents)

if __name__=='__main__':
    # diffDatabases('pokemaster_v1.4-rc1.db')
    diffDatabases('pokemaster_v1.51.db')
    # generateDiffFiles("Old DB", "New DB")
    # showDeletedFiles('pokemaster_v1.3-beta6.db')
    # restoreDeletedFiles('pokemaster_v1.3-beta6.db')
    # restoreUnknownTypes('pokemaster_v1.3-beta6.db')
    # showDeletedFiles('pokemaster_v1.3-beta6.db')
    # diffDatabases('pokemaster_v1.4-alpha9.db')
    # diffDatabases('pokemaster_v1.3-beta6.db')
    # showDeletedFiles('pokemaster_v1.4-alpha5.db')