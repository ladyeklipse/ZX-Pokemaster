import shutil
from classes.zxdb_scraper import *
from classes.tosec_scraper import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
if __name__=='__main__':
    LOCAL_FTP_ROOT = os.path.join(os.getcwd(), 'ftp')
    if os.path.exists('pokemaster.db'):
        os.unlink('pokemaster.db')
    db = Database()
    with open('pokemaster_db_schema.sql', 'r', encoding='utf-8') as f:
        sql = f.read().split(';\n')
        for query in sql:
            if not query or 'COMMIT' in query:
                continue
            db.execute(query)
        db.commit()
    zxdb = ZXDBScraper()
    games = zxdb.getAllGames()
    zxdb.downloadMissingFilesForGames(games)
    zxdb.getInfoFromLocalFiles(games)
    for game in games:
        db.addGame(game)
    db.commit()
    if os.path.exists('zxdb/pokemaster_zxdb_only.db'):
        os.unlink('zxdb/pokemaster_zxdb_only.db')
    shutil.copy('pokemaster.db', 'zxdb/pokemaster_zxdb_only.db')
    import scrape_tosec