from classes.wos_scraper import *
from classes.tipshop_scraper import *
from classes.database import *
import traceback

def getGamesList():
    ws = WosScraper()
    letters = '1abcdefghijklmnopqrstuvwxyz'
    letter_by_letter_folders = ['games', 'textadv']
    single_page_folders = ['educatio', ]
    games_list = []
    for folder in letter_by_letter_folders:
        for letter in letters:
            letter_games = ws.loadGamesListForLetter(letter, folder)
            games_list += letter_games
    return games_list


def scrapeWos(scrape_tipshop=True):
    ws = WosScraper()
    ts = TipshopScraper()
    db = Database()
    letters = '1abcdefghijklmnopqrstuvwxyz'
    games_list = []
    folders = ['games', 'textadv']
    for folder in folders:
        for letter in letters:
            letter_games = ws.loadGamesListForLetter(letter, folder)
            games_list += letter_games
            for game in letter_games:
                print(game.name)
                game.getInfoFromDB(db)
                ws.scrapeGameData(game)
                ws.downloadFiles(game)
                game.getInfoFromLocalFiles()
                if scrape_tipshop and game.has_tipshop_pokes:
                    pokes = ts.scrapePokes(game)
                    if game.cheats:
                        game.mergeDescriptionsWithOldDBFile()
                db.addGame(game)
            db.commit()
            print('Committed')

if __name__=='__main__':
    scrapeWos()