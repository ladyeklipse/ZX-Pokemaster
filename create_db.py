from classes.database import *
from classes.zxdb_scraper import *
from classes.tosec_scraper import *
from classes.tipshop_scraper import *
from scrape_zxdb import *
from scrape_tipshop import *
from tipshop_excel_converter import *
from scrape_tosec import *
import sys

if __name__=='__main__':
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
    for game in games:
        for release in game.releases:
            release.getInfoFromLocalFiles()
        db.addGame(game)
    db.commit()
    # sys.exit()
    # ts = TOSECScraper(db)
    # ts.paths = ts.generateTOSECPathsArrayFromDatFiles()
    # ts.scrapeTOSEC()
