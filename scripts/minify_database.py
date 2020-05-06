import os
from classes.database import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
import sqlite3

def createMiniDB():
    if os.path.exists(POKEMASTER_MIN_DB_PATH):
        os.unlink(POKEMASTER_MIN_DB_PATH)
    min_db =  sqlite3.connect(POKEMASTER_MIN_DB_PATH)
    with open('pokemaster_min_db_schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read().split(';\n')
        for query in sql:
            if not query or 'COMMIT' in query:
                continue
            min_db.cursor().execute(query)
        min_db.commit()
    return min_db

def getTableColumns(db, tableName):
    columns = []
    sql = 'pragma table_info({})'.format(tableName)
    raw_data = db.cursor().execute(sql).fetchall()
    for entry in raw_data:
        columns.append(entry[1])
    return columns

def copyData():
    if not os.path.exists(POKEMASTER_DB_PATH):
        raise Exception('No database')
    old_db = sqlite3.connect(POKEMASTER_DB_PATH)
    min_db = sqlite3.connect(POKEMASTER_MIN_DB_PATH)
    min_db.execute('PRAGMA JOURNAL_MODE = OFF')
    for tableName in ['game', 'game_release', 'game_file']:
        old_columns = getTableColumns(old_db, tableName)
        min_columns = getTableColumns(min_db, tableName)
        if tableName=='game':
            order = 'zxdb_id'
        elif tableName == 'game_release':
            order = 'zxdb_id, release_seq'
        elif tableName == 'game_file':
            order = 'game_zxdb_id, game_release_seq'
        sql = 'SELECT * FROM {} ORDER BY {}'.format(tableName, order)
        rows = old_db.execute(sql).fetchall()
        for row in rows:
            values = []
            for i, column in enumerate(old_columns):
                if column in min_columns:
                    value = row[i]
                    if value==None:
                        value = 'NULL'
                    else:
                        value = '"'+str(row[i]).replace('"', '""')+'"'
                    values.append(value)
            values = ','.join(values)
            sql = 'INSERT INTO {} VALUES ({});'.format(tableName, values)
            # print(sql)
            min_db.execute(sql)
    min_db.commit()

min_db = createMiniDB()
min_db.close()
copyData()
