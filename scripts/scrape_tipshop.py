from classes.tosec_dat import *
from classes.tipshop_scraper import *
from classes.zxdb_scraper import *
from classes.database import *
from classes.game import *
from scripts.tipshop_excel_converter import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def getWosIDsOfTipshopGames(db=None):
    zxdb_ids_tipshop_pages_pairs = []
    ts = TipshopScraper()
    db = db if db else Database()
    db.loadCache()
    letters = ['0123']+[x for x in 'abcdefghijklmnopqrstuvwxyz']
    # letters='d'
    missing_data = []
    for letter in letters:
        urls = ts.getList(letter)
        for url in urls:
            wos_game_data = ts.getWosIdFromUrl(url)
            if type(wos_game_data)==int:
                zxdb_ids_tipshop_pages_pairs.append((url, wos_game_data))
            else:
                game = db.getGameByName(wos_game_data)
                if game:
                    print('Game found:', wos_game_data, game)
                    zxdb_ids_tipshop_pages_pairs.append((url, game.zxdb_id))
                elif wos_game_data:
                    game = Game(wos_game_data, zxdb_id=99999999)
                    game.tipshop_page = url
                    ts.scrapePokes(game)
                    if game.cheats:
                        missing_data.append(wos_game_data)
    print("MISSING ZXDB IDS:")
    print('\n'.join(missing_data))
    return zxdb_ids_tipshop_pages_pairs

def games2xlsx(games, xlsx_filename='new_tipshop_pokes.xlsx', new_only=False):
    if new_only:
        games = [game for game in games if game.has_new_pokes]
    import xlsxwriter
    db = Database()
    sql = "SELECT zxdb_id, name, pok_file_contents, tipshop_multiface_pokes_section " \
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
            game.getPokFileContents(for_xlsx=True),
            game.tipshop_multiface_pokes_section,
            '0' if game.has_new_pokes else '1'
        ], mformat)
    workbook.close()

def updateTipshopPageColumn(zxdb_ids_tipshop_pages_pairs, db=None):
    db = db if db else Database()
    for pair in zxdb_ids_tipshop_pages_pairs:
        sql = 'UPDATE game SET tipshop_page=? WHERE zxdb_id=?'
        params = pair
        db.execute(sql, params)
    db.commit()

def getAllPokes(zxdb_ids=[]):
    db = Database()
    games = db.getAllGames('tipshop_page IS NOT NULL AND tipshop_page!="0"')
    ts = TipshopScraper()
    for i, game in enumerate(games):
        if zxdb_ids and game.zxdb_id not in zxdb_ids:
            continue
        old_cheats = [cheat for cheat in game.cheats]
        print(old_cheats)
        game.has_new_pokes = False
        ts.scrapePokes(game)
        print(game.cheats, old_cheats, [cheat for cheat in game.cheats if cheat not in old_cheats])
        for cheat in game.cheats:
            if cheat not in old_cheats:
                print('New cheat found:', cheat)
                game.has_new_pokes = True
                break
        print('left=', len(games)-i)
    if zxdb_ids:
        return [game for game in games if game.zxdb_id in zxdb_ids]
    return games

def updateMods():
    zxdb = ZXDBScraper()
    zxdb.cur.execute('''
    SELECT entry_id as id, original_id FROM relations
    WHERE relationtype_id='m';
    ''')
    db = Database()
    for mod in zxdb.cur:
        print(mod)
        if not str(mod['original_id']).isnumeric():
            continue
        mod_game = db.getGameByWosID(mod['id'])
        mod_of = db.getGameByWosID(mod['original_id'])
        if not mod_of:
            print('No game with id', mod['original_id'])
            continue
        if not mod_game:
            print('Game with ID', mod['id'], 'not found')
            continue
        for cheat in mod_of.cheats:
            mod_game.addCheat(cheat, modify_description_on_collision=True)
        for cheat in mod_of.cheats:
            if cheat.description=='Having already applied the poke simply add these':
                cheat.description = 'Moves invisible object from First Landing to The Hall'
            elif cheat.description == 'To prevent this from happening':
                cheat.description = 'No pitch decrease when life lost'
        for cheat in mod_game.cheats:
            if cheat.description=='Having already applied the poke simply add these':
                cheat.description = 'Moves invisible object from First Landing to The Hall'
            elif cheat.description == 'To prevent this from happening':
                cheat.description = 'No pitch decrease when life lost'
        db.addGame(mod_game)
    db.commit()
    db = Database()

def extractPokFiles():
    db = Database()
    games = db.getAllGames('pok_file_contents!=""')
    csv_contents = ''
    for letter in ALPHABETIC_DIRNAMES:
        folder = os.path.join('AllTipshopPokes', letter)
        if os.path.exists(folder):
            shutil.rmtree(folder)
    for game in games:
        print(game)
        filename = game.getTOSECName()+'.pok'
        path = os.path.join('AllTipshopPokes', getWosSubfolder(filename), filename)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        game.exportPokFile(path)
        csv_contents += game.getWosID()+';'+'/zxdb/sinclair/pokes/'+getWosSubfolder(filename)+'/'+filename+'\n'
    with open(os.path.join('AllTipshopPokes', 'zxdb_update.csv'), 'w', encoding='utf-8') as f:
        f.write(csv_contents)

def generateZXDBUpdate(zxdb_ids):
    with open('relatedlinks.update.sql', 'w+', encoding='utf-8') as f:
        f.write('INSERT INTO relatedlinks (website_id, entry_id, link) VALUES (\n')
        for zxdb_id in zxdb_ids:
            f.write('(8, '+str(zxdb_id)+', "http://www.the-tipshop.co.uk/cgi-bin/info.pl?name='+str(zxdb_id).zfill(7)+'"),\n')
        f.write(')')

def scrapePokesFromText(text):
    ts = TipshopScraper()
    game = Game()
    ts.getPokesFromStrings(game, text.split('\n'))
    game.exportPokFile('pokes.pok')
    with open('pokes.pok', 'r', encoding='utf-8') as f:
        print(f.read())

def convertHexes(text):
    text = text.replace('$', '#')
    hexes = re.findall(r'(\#[a-fA-F0-9]{2,4}[,\s]{1,})', text)
    print(hexes)
    for hexnum in hexes:
        hexnum = hexnum[1:].strip().replace(',','')
        print('hexnum=',hexnum)
        if not hexnum:
            continue
        intnum = int(str(hexnum), 16)
        print(intnum)
        text = text.replace('#'+hexnum, str(intnum), 1)
    return text

def createPOKTOSECDat():
    dat = TOSECDat('Sinclair ZX Spectrum - Pokes - [POK]')
    dat.allow_duplicates = True
    dat.files = []
    for root, dirs, files in os.walk('AllTipshopPokes'):
        for file in files:
            if not file.endswith('.pok'):
                continue
            filepath = os.path.join(root, file)
            # print(filepath)
            game_file = GameFile(filepath)
            game_file.setSize(os.path.getsize(filepath))
            game_file.format = 'pok'
            # print(game_file)
            dat.addFile(game_file)
    dat.export()
    shutil.copy(dat.getExportPath(),
                os.path.join('AllTipshopPokes', 'Sinclair ZX Spectrum - Pokes - [POK] (TOSEC).dat'))

if __name__=='__main__':
    #FIRST PART
    # zxdb_ids_tipshop_pages_pairs = getWosIDsOfTipshopGames()
    # updateTipshopPageColumn(zxdb_ids_tipshop_pages_pairs)
    # games = getAllPokes()
    # games2xlsx(games, new_only=True)
    # xlsx2db()
    #SECOND PART (after new_tipshop_pokes.xlsx edited and MANUALLY renamed to pokes.xlsx)
    xlsx2db()
    updateMods()
    extractPokFiles()
    createPOKTOSECDat()