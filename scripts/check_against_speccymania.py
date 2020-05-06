import pyodbc
from classes.database import *

connStr = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\\ZX Pokemaster\\SpeccyMania.accdb;"
    )
con = pyodbc.connect(connStr)
cur = con.cursor()
games = cur.execute('SELECT * FROM Games')
not_scraped_zxdb_ids = []
db = Database()
db_zxdb_ids = [int(x['zxdb_id']) for x in db.execute('SELECT zxdb_id FROM game')]
print('Scraped:', len(db_zxdb_ids))
for game in games:
    if not game.V_Comment:
        continue
    zxdb_id = int(game.V_Comment[3:])
    if zxdb_id not in db_zxdb_ids:
        not_scraped_zxdb_ids.append(zxdb_id)
not_scraped_zxdb_ids = sorted(not_scraped_zxdb_ids)
for zxdb_id in not_scraped_zxdb_ids:
    print('http://www.worldofspectrum.org/infoseekid.cgi?id='+str(zxdb_id).zfill(7))
print('Not scraped:', len(not_scraped_zxdb_ids))
