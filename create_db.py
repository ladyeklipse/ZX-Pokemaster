from classes.database import *
from classes.zxdb_scraper import *
from classes.tosec_scraper import *
from classes.tipshop_scraper import *
from scrape_zxdb import *
from scrape_tipshop import *
from tipshop_excel_converter import *
from scrape_tosec import *

if __name__=='__main__':
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
    wos_ids_tipshop_pages_pairs = getWosIDsOfTipshopGames(db)
    ts = TOSECScraper(db)
    paths = ts.generateTOSECPathsArray()
    ts.scrapeTOSEC()
    paths = ts.showUnscraped()
    ts.paths = paths
    ts.scrapeTOSEC()
    updateTipshopPageColumn(wos_ids_tipshop_pages_pairs, db)
    xlsx2db()


