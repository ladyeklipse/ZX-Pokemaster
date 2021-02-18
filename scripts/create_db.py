import shutil
from classes.zxdb_scraper import *
from classes.tosec_scraper import *
from analyze_old_db_inconsistencies import restoreDeletedFiles
from scripts.tipshop_excel_converter import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

def scrapeZXDB(download_missing=True):
    LOCAL_FTP_ROOT = os.path.join(os.getcwd(), 'ftp')
    if os.path.exists(POKEMASTER_DB_PATH):
        os.unlink(POKEMASTER_DB_PATH)
    if os.path.exists(POKEMASTER_MIN_DB_PATH):
        os.unlink(POKEMASTER_MIN_DB_PATH)
    db = Database()
    with open('pokemaster_db_schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read().split(';\n')
        for query in sql:
            if not query or 'COMMIT' in query:
                continue
            db.execute(query)
        db.commit()
    zxdb = ZXDBScraper()
    print("Getting all games from ZXDB...")
    games = zxdb.getAllGames()
    if download_missing:
        zxdb.downloadMissingFilesForGames(games)
    zxdb.getInfoFromLocalFiles(games)
    for game in games:
        db.addGame(game)
    db.commit()
    xlsx2db()
    if os.path.exists('zxdb/pokemaster_zxdb_only.db'):
        os.unlink('zxdb/pokemaster_zxdb_only.db')
    shutil.copy('pokemaster.db', 'zxdb/pokemaster_zxdb_only.db')

if __name__=='__main__':
    scrapeZXDB(download_missing=False)
    import scrape_tosec
    restoreDeletedFiles('pokemaster_v1.4-rc1.db')
    import scripts.create_tosec_dats
    import scripts.minify_database
