import pyodbc
from classes.database import *

connStr = (
    r"DRIVER={Microsoft Access Driver (*.mdb, *.accdb)};"
    r"DBQ=C:\\ZX Pokemaster\\SpeccyMania.accdb;"
    )
con = pyodbc.connect(connStr)
cur = con.cursor()
games = cur.execute('SELECT * FROM Games')
not_scraped_wos_ids = []
db = Database()
db_wos_ids = [int(x['wos_id']) for x in db.execute('SELECT wos_id FROM game')]
print('Scraped:', len(db_wos_ids))
for game in games:
    if not game.V_Comment:
        continue
    wos_id = int(game.V_Comment[3:])
    if wos_id not in db_wos_ids:
        not_scraped_wos_ids.append(wos_id)
not_scraped_wos_ids = sorted(not_scraped_wos_ids)
for wos_id in not_scraped_wos_ids:
    print('http://www.worldofspectrum.org/infoseekid.cgi?id='+str(wos_id).zfill(7))
print('Not scraped:', len(not_scraped_wos_ids))
