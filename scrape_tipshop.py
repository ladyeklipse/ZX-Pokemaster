from classes.tipshop_scraper import *
from classes.database import *
from classes.game import *
# from tipshop_excel_converter import *

def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def getWosIDsOfTipshopGames(db=None):
    wos_ids_tipshop_pages_pairs = []
    ts = TipshopScraper()
    db = db if db else Database()
    db.loadCache()
    letters = ['0123']+[x for x in 'abcdefghijklmnopqrstuvwxyz']
    # letters='a'
    missing_data = []
    for letter in letters:
        urls = ts.getList(letter)
        for url in urls:
            wos_game_data = ts.getWosIdFromUrl(url)
            if type(wos_game_data)==int:
                wos_ids_tipshop_pages_pairs.append((url, wos_game_data))
            else:
                game = db.getGameByName(wos_game_data)
                if game:
                    print('Game found:', wos_game_data, game)
                    wos_ids_tipshop_pages_pairs.append((url, game.wos_id))
                elif wos_game_data:
                    missing_data.append(wos_game_data)
    print('\n'.join(missing_data))
    return wos_ids_tipshop_pages_pairs

def games2xlsx(games, xlsx_filename='new_tipshop_pokes.xlsx', new_only=False):
    if new_only:
        games = [game for game in games if game.has_new_pokes]
    import xlsxwriter
    db = Database()
    sql = "SELECT wos_id, name, pok_file_contents, tipshop_multiface_pokes_section " \
          "FROM game WHERE pok_file_contents != ''"
    raw_data = db.execute(sql)
    workbook = xlsxwriter.Workbook(xlsx_filename)
    mformat = workbook.add_format()
    mformat.set_text_wrap()
    mformat.set_align('top')
    worksheet = workbook.add_worksheet()
    worksheet.set_default_row(200)
    worksheet.set_column('C:C', 40)
    worksheet.set_column('D:D', 40)
    for i, game in enumerate(games):
        worksheet.write_row(i, 0, [
            game.getWosID(),
            game.name,
            game.getPokFileContents(),
            game.tipshop_multiface_pokes_section,
            '0' if game.has_new_pokes else '1'
        ], mformat)
    workbook.close()

def updateTipshopPageColumn(wos_ids_tipshop_pages_pairs, db=None):
    db = db if db else Database()
    # for chunk in chunks(wos_ids_tipshop_pages_pairs, 500):
    #     sql = 'UPDATE game SET has_tipshop_page=1 WHERE wos_id in ('+','.join(['?']*len(chunk))+')'
    #     print(sql, chunk)
    #     db.execute(sql, chunk)
    for pair in wos_ids_tipshop_pages_pairs:
        sql = 'UPDATE game SET tipshop_page=? WHERE wos_id=?'
        params = pair
        db.execute(sql, params)
    db.commit()

def getAllPokes(wos_ids=[]):
    db = Database()
    games = db.getAllGames('tipshop_page IS NOT NULL')
    # games = games[:10]
    ts = TipshopScraper()
    for i, game in enumerate(games):
        if wos_ids and game.wos_id not in wos_ids:
            continue
        old_cheats = [cheat for cheat in game.cheats]
        print(old_cheats)
        # game.cheats = []
        game.has_new_pokes = False
        ts.scrapePokes(game)
        print(game.cheats, old_cheats, [cheat for cheat in game.cheats if cheat not in old_cheats])
        for cheat in game.cheats:
            if cheat not in old_cheats:
                print('New cheat found:', cheat)
                game.has_new_pokes = True
                break
        # if game.cheats:
        #     db.addGame(game)
        print('left=', len(games)-i)
    # db.commit()
    if wos_ids:
        return [game for game in games if game.wos_id in wos_ids]
    return games

def extractPokFiles():
    db = Database()
    games = db.getAllGames('pok_file_contents!=""')
    for game in games:
        print(game)
        filename = game.getTOSECName()+'.pok'
        path = os.path.join('AllTipshopPokes', getWosSubfolder(filename), filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        game.exportPokFile(path)

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
    wos_ids_tipshop_pages_pairs = getWosIDsOfTipshopGames()
    updateTipshopPageColumn(wos_ids_tipshop_pages_pairs)
    # print('total wos_ids = ', len(wos_ids))
    # games = getAllPokes()
    # games2xlsx(games, new_only=True)
    # extractPokFiles()
    # TEMPORARY BELOW
    # text = convertHexes('''''')
    # scrapePokesFromText(text)
    # text = ''''''
    # scrapePokesFromText(text)