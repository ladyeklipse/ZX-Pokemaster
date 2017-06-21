from classes.tipshop_scraper import *
from classes.database import *

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def getWosIDsOfTipshopGames():
    wos_ids = []
    ts = TipshopScraper()
    letters = ['0123']+[x for x in 'abcdefghijklmnopqrstuvwxyz']
    for letter in letters:
        urls = ts.getList(letter)
        for url in urls:
            wos_id = ts.getWosIdFromUrl(url)
            if type(wos_id)==int:
                wos_ids.append(wos_id)
    return wos_ids

def update_has_tipshop_page_column(wos_ids):
    db = Database()
    for chunk in chunks(wos_ids, 500):
        sql = 'UPDATE game SET has_tipshop_page=1 WHERE wos_id in ('+','.join(['?']*len(chunk))+')'
        print(sql, chunk)
        db.execute(sql, chunk)
    db.commit()

def getAllPokes():
    db = Database()
    games = db.getAllGames('has_tipshop_page=1')
    # games = games[:10]
    ts = TipshopScraper()
    for i, game in enumerate(games):
        ts.scrapePokes(game)
        if game.cheats:
            db.addGame(game)
        print('left=', len(games)-i)
    db.commit()

def generateZXDBUpdate(wos_ids):
    with open('relatedlinks.update.sql', 'w+', encoding='utf-8') as f:
        f.write('INSERT INTO relatedlinks (website_id, entry_id, link) VALUES (\n')
        for wos_id in wos_ids:
            f.write('(8, '+str(wos_id)+', "http://www.the-tipshop.co.uk/cgi-bin/info.pl?name='+str(wos_id).zfill(7)+'"),\n')
        f.write(')')

def scrapePokesFromText(text):
    ts = TipshopScraper()
    game = Game()
    ts.getPokesFromStrings(game, text.split('\n'))
    game.exportPokFile('pokes.pok')
    with open('pokes.pok', 'r', encoding='utf-8') as f:
        print(f.read())

def convertHexes(text):
    hexes = re.findall(r'([a-fA-F0-9]{2,4}[,\s]{1})', text)
    print(hexes)
    for hexnum in hexes:
        hexnum = hexnum.strip().replace(',','')
        print('hexnum=',hexnum)
        if not hexnum:
            continue
        intnum = int(str(hexnum), 16)
        print(intnum)
        text = text.replace(hexnum, str(intnum))
    return text.replace('$', '').replace('#', '')

if __name__=='__main__':
    # wos_ids = getWosIDsOfTipshopGames()
    # generateZXDBUpdate(wos_ids)
    # print('total wos_ids = ', len(wos_ids))
    # update_has_tipshop_page_column(wos_ids)
    # getAllPokes()
    text = convertHexes('''
    [128K]Fix Sinclair joysticks
$9636,$01
$9638,$02
$963a,$04
$963c,$10
$963e,$08
''')
    print(text)
    scrapePokesFromText(text)
    text = '''
'''
    scrapePokesFromText(text)