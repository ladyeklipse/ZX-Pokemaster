from classes.tosec_dat import *
from classes.tipshop_scraper import *
from classes.zxdb_scraper import *
from classes.database import *
from classes.game import *
# from tipshop_excel_converter import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
def chunks(l, n):
    for i in range(0, len(l), n):
        yield l[i:i + n]

def getWosIDsOfTipshopGames(db=None):
    wos_ids_tipshop_pages_pairs = []
    ts = TipshopScraper()
    db = db if db else Database()
    db.loadCache()
    letters = ['0123']+[x for x in 'abcdefghijklmnopqrstuvwxyz']
    # letters='g'
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
            game.getPokFileContents(for_xlsx=True),
            game.tipshop_multiface_pokes_section,
            '0' if game.has_new_pokes else '1'
        ], mformat)
    workbook.close()

def updateTipshopPageColumn(wos_ids_tipshop_pages_pairs, db=None):
    db = db if db else Database()
    for pair in wos_ids_tipshop_pages_pairs:
        sql = 'UPDATE game SET tipshop_page=? WHERE wos_id=?'
        params = pair
        db.execute(sql, params)
    db.commit()

def getAllPokes(wos_ids=[]):
    db = Database()
    games = db.getAllGames('tipshop_page IS NOT NULL AND tipshop_page!="0"')
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
        print('left=', len(games)-i)
    if wos_ids:
        return [game for game in games if game.wos_id in wos_ids]
    return games

def updateMods():
    zxdb = ZXDBScraper()
    zxdb.cur.execute('''
    SELECT id, original_id FROM entries
    WHERE is_mod=1;
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
        for cheat in mod_of.cheats:
            mod_game.addCheat(cheat)
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
    # wos_ids_tipshop_pages_pairs = getWosIDsOfTipshopGames()
    # updateTipshopPageColumn(wos_ids_tipshop_pages_pairs)
    # print('total wos_ids = ', len(wos_ids))
    # games = getAllPokes()
    # games2xlsx(games, new_only=True)
    # updateMods()
    extractPokFiles()
    createPOKTOSECDat()
    # TEMPORARY BELOW
    # text = convertHexes('''
# some good
#5B00, #01 :
#5B01, #FE :
#5B02, #FB :
#5B03, #ED :
#5B04, #78 :
#5B05, #E6 :
#5B06, #02 :
#5B07, #20 :
#5B08, #0B :
#5B09, #01 :
#5B0A, #1D :
#5B0B, #00 :
#5B0C, #11 :
#5B0D, #A3 :
#5B0E, #7A :
#5B0F, #21 :
#5B10, #18 :
#5B11, #5B :
#5B12, #ED :
#5B13, #B0 :
#5B14, #C3 :
#5B15, #79 :
#5B16, #89 :
#5B17, #00
#5B18, #01 :
#5B19, #03 :
#5B1A, #01 :
#5B1B, #01 :
#5B1C, #01 :
#5B1D, #00 :
#5B1E, #0B :
#5B1F, #08 :
#5B20, 	#00 :
#5B21, 	#0C  :
#5B22, 	#0A  :
#5B23, 	#01  :
#5B24, 	#04  :
#5B25, 	#09  :
#5B26, 	#02  :
#5B27, 	#06 :
#5B28, 	#02  :
#5B29, 	#0D  :
#5B2A, 	#0A  :
#5B2B, 	#07  :
#5B2C, 	#06  :
#5B2D, 	#0A  :
#5B2E, 	#0E  :
#5B2F, 	#00 :
#5B30,	#00 :
#5B31, 	#00  :
#5B32, 	#03  :
#5B33, 	#03  :
#5B34, 	#00  :
#5B35, 	#00  :
#5B36, 	#00  :
#5B37, 	#00 :
# 34388, 0
# 34389, 91
#     ''')
#     print(text)
#     scrapePokesFromText(text)
    text = '''
Eugene not interested in guarding portal (Bug-Byte) 
POKE 36348,0: POKE 36349,0: POKE 36438,24 
Eugene not interested in guarding portal (Software Project)
POKE 36359,0: POKE 36360,0: POKE 36449,24 

Portal not required (Bug-Byte) 
POKE 36809,176: POKE 36810,128: POKE 36815,177: POKE 36816,128 
Portal not Required (Software Project)
POKE 36820,176: POKE 36821,128: POKE 36826,177: POKE 36827,128 

Eugene completely harmless (Bug-Byte) POKE 36408,0 
Eugene completely harmless (Software Project) 36419,0 

Skylabs harmless (Bug-Byte) POKE 36552,0 
Skylabs harmless (Software Project) POKE 36563,0 

Next cavern instead of loss of life (Bug-Byte) POKE 34799,40 POKE 34800,144 
Next cavern instead of loss of life (Software Project) 34805,51 POKE 34806,144 

Larger bonus for cavern completion (Bug-Byte) POKE 37051,45 
Larger bonus for cavern completion  (Software Project) POKE 37062,45 

Reduce air drain in Solar Power Generator (Bug-Byte) POKE 36236,0: POKE 36237,0: POKE 36238,0: POKE 36239,0: POKE 36240,0: POKE 36241,0 
Reduce air drain in Solar Power Generator (Software Project) POKE 36247,0: POKE 36248,0: POKE 36249,0: POKE 36250,0 : POKE 36251,0 : POKE 36252,0  
'''
    # scrapePokesFromText(text)