from classes.database import *
from classes.game import Game
from classes.game_release import GameRelease
from classes.game_file import GameFile, ROUND_BRACKETS_REGEX
from classes.game_alias import GameAlias
from classes.scraper import *
from functions.game_name_functions import *
from mysql import connector
import time

def get_win_friendly_alias(alias):
    alias = ' '.join([x for x in alias.replace(':', ' : ').split(' ') if x])
    win_friendly_alias = filepath_regex.sub('-', alias)
    return win_friendly_alias

class RowConverter(connector.conversion.MySQLConverter):

    def row_to_python(self, row, fields):
        row = super(RowConverter, self).row_to_python(row, fields)
        def to_unicode(col):
            if type(col) == bytearray:
                return col.decode('utf-8')
            return col
        return[to_unicode(col) for col in row]

class ZXDBScraper():

    def __init__(self):
        self.conn = connector.connect(
                                user='root',
                                password='',
                                host='localhost',
                                database='zxdb',
                                charset='utf8',
                                converter_class=RowConverter
                                )
        self.cur = self.conn.cursor(dictionary=True, buffered=True)
        self.loadLookupTables()

    def loadLookupTables(self):
        self.file_exclusion_list = []
        with open('same_md5.csv', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.split(';')
                decision = line[7]
                if not decision.startswith('KEEP'):
                    self.file_exclusion_list.append(line[10])
        self.manually_corrected_content_descriptions = {}
        with open('content_desc_aliases.csv', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip().split(';')
                if len(line)<5 or not line[4]:
                    continue
                key = line[5]+'|'+line[4]
                if line[2].startswith('NONE'):
                    self.manually_corrected_content_descriptions[key] = 'NONE'
                elif line[2].startswith('ALT'):
                    self.manually_corrected_content_descriptions[key] = line[2]
        self.pok_file_paths = {}
        with open('AllTipshopPokes\\zxdb_update.csv', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip().split(';')
                if len(line)==2:
                    self.pok_file_paths[int(line[0])] = line[1].replace('/zxdb/sinclair/pokes', 'AllTipshopPokes')

    def update(self, script_path):
        self.cur.execute('SET FOREIGN_KEY_CHECKS = 0')
        requests = self.cur.execute(
            "SELECT concat('DROP TABLE IF EXISTS ', table_name, ';' "
            "FROM information_schema.tables WHERE table_schema = 'zxdb'")
        for request in requests:
            print(request)
            self.cur.execute(request)
        self.cur.execute('COMMIT')
        self.cur.execute('SET FOREIGN_KEY_CHECKS = 1')
        with open(script_path, 'r', encoding='utf-8') as f:
            sql = f.read().split(';\n')
            for query in sql:
                if not query or 'COMMIT' in query:
                    continue
                self.cur.execute(query)
            self.cur.execute('COMMIT')
        print('DB updated')

    def getAllGames(self):
        return self.getGames()

    def getGames(self, sql_where='', sql_limit=9999999):
        sql = 'SELECT entries.id AS wos_id, ' \
              'releases.release_seq AS release_seq, ' \
              'entries.title AS name, ' \
              'entries.library_title AS tosec_compliant_name, ' \
              'entries.is_xrated AS x_rated, ' \
              'relatedlinks.link AS tipshop_page, ' \
              'genretypes.text AS genre, ' \
              'entries.max_players AS number_of_players, ' \
              'entries.multiplaytype_id AS multiplayer_type, ' \
              'entries.idiom_id AS language, ' \
              'entries.availabletype_id AS availability, ' \
              'downloads.file_link AS file_link, ' \
              'downloads.file_size AS file_size, ' \
              'downloads.filetype_id AS file_type_id, ' \
              'downloads.formattype_id AS file_format_id, ' \
              'filetypes.text AS file_type, ' \
              'formattypes.text AS file_format,' \
              'entry_machinetype.text AS machine_type, ' \
              'download_machinetype.text AS file_machine_type, ' \
              'schemetypes.text AS protection_scheme, ' \
              'releases.release_seq AS release_id, ' \
              'aliases.library_title AS alt_name, ' \
              'aliases.idiom_id AS alt_language, ' \
              'publisher_labels.name AS publisher, ' \
              'publisher_labels.is_company AS publisher_is_company, ' \
              'author_labels.name AS author, ' \
              'author_labels.is_company AS author_is_company, ' \
              'releases.release_year AS year,' \
              'publisher_labels.country_id AS country ' \
              'FROM entries ' \
              'LEFT JOIN relatedlinks ON entries.id=relatedlinks.entry_id AND relatedlinks.website_id=9 ' \
              'LEFT JOIN releases ON entries.id=releases.entry_id ' \
              'LEFT JOIN downloads ON downloads.entry_id=entries.id AND downloads.release_seq=releases.release_seq ' \
              'LEFT JOIN publishers ON publishers.entry_id=entries.id AND publishers.release_seq=releases.release_seq  ' \
              'LEFT JOIN labels AS publisher_labels ON publisher_labels.id=publishers.label_id ' \
              'LEFT JOIN authors ON authors.entry_id=entries.id AND authors.author_seq=1  ' \
              'LEFT JOIN labels AS author_labels ON author_labels.id=authors.label_id ' \
              'LEFT JOIN aliases ON aliases.entry_id=entries.id AND aliases.release_seq=releases.release_seq ' \
              'LEFT JOIN filetypes ON downloads.filetype_id=filetypes.id ' \
              'LEFT JOIN formattypes ON downloads.formattype_id=formattypes.id ' \
              'LEFT JOIN genretypes ON genretypes.id=entries.genretype_id ' \
              'LEFT JOIN machinetypes download_machinetype ON download_machinetype.id=downloads.machinetype_id ' \
              'LEFT JOIN machinetypes entry_machinetype ON entry_machinetype.id=entries.machinetype_id ' \
              'LEFT JOIN schemetypes ON schemetypes.id=downloads.schemetype_id   ' \
              'WHERE (entries.id>4000000 OR entries.id<1000000) AND ' \
              '(publisher_seq IS NULL OR publisher_seq=1) AND ' \
              '(downloads.filetype_id IS NULL OR downloads.filetype_id!=-1)'
        if sql_where:
            sql += sql_where+' '
        sql +='ORDER BY wos_id, release_seq, entries.title IS NOT NULL ' \
              'LIMIT '+str(sql_limit)
        self.cur.execute(sql)
        game = Game()
        release = GameRelease()
        games = []
        for row in self.cur:
            #Skipping ZX80/ZX81 files
            if row['machine_type'] and row['machine_type'].startswith('ZX8'):
                continue
            if row['publisher'] == 'Creative.Radical.Alternative.Production Games':
                row['publisher'] = 'Creative Radical Alternative Production Games'
            if row['wos_id'] and row['name'] and row['wos_id']!=game.wos_id:
                game = self.gameFromRow(row)
                release = self.releaseFromRow(row, game)
                game.addRelease(release)
                games.append(game)
            if row['release_seq'] and row['release_seq']!=release.release_seq:
                release = self.releaseFromRow(row, game)
                game.addRelease(release)
            if row['file_link'] and not (row['file_link'].endswith('.mlt')):
                if row['file_type']=='Loading screen':
                    if row['file_format']=='Picture':
                        if release.loading_screen_gif_filepath and \
                                        release.loading_screen_gif_filepath!=row['file_link']:
                            pass
                        else:
                            release.loading_screen_gif_filepath = row['file_link']
                            release.loading_screen_gif_filesize = row['file_size']
                    elif row['file_format']=='Screen dump':
                        if release.loading_screen_scr_filepath and \
                                        release.loading_screen_scr_filepath!=row['file_link']:
                            pass
                        else:
                            release.loading_screen_scr_filepath = row['file_link']
                            release.loading_screen_scr_filesize = row['file_size']
                elif row['file_type']=='In-game screen':
                    if row['file_format']=='Picture':
                        if release.ingame_screen_gif_filepath and \
                                        release.ingame_screen_gif_filepath!=row['file_link']:
                            pass
                        else:
                            release.ingame_screen_gif_filepath = row['file_link']
                            release.ingame_screen_gif_filesize = row['file_size']
                    elif row['file_format'] == 'Screen dump':
                        if release.ingame_screen_scr_filepath and \
                                        release.ingame_screen_scr_filepath != row['file_link']:
                            pass
                        else:
                            release.ingame_screen_scr_filepath = row['file_link']
                            release.ingame_screen_scr_filesize = row['file_size']
                elif row['file_type']=='Instructions' and row['file_link'].endswith('.txt'):
                    if release.manual_filepath and \
                                    release.manual_filepath!=row['file_link']:
                        pass
                    else:
                        release.manual_filepath = row['file_link']
                        release.manual_filesize = row['file_size']
                elif row['file_format'] and \
                        ('snapshot' in row['file_format'] or \
                         'disk' in row['file_format'] or \
                         'tape' in row['file_format'] or \
                         'ROM' in row['file_format']):
                    game_file = self.gameFileFromRow(row, game)
                    if game_file.wos_path not in self.file_exclusion_list:
                        release.addFile(game_file)
                elif row['file_type']=='POK pokes file':
                    try:
                        pok_file_path = row['file_link'].replace('/zxdb/sinclair/pokes', 'AllTipshopPokes')
                        game.importPokFile(file_path=pok_file_path)
                    except FileNotFoundError:
                        pok_file_path = self.pok_file_paths.get(game.wos_id)
                        if not pok_file_path:
                            print('Poke not found for:', game)
                        else:
                            game.importPokFile(file_path=pok_file_path)
                if row['alt_name'] and row['alt_language'] in (None, 'en'):
                    alias = self.sanitizeAlias(row['alt_name'])
                    release.addAlias(alias)

        games.append(game)
        return games

    def gameFromRow(self, row):
        game_name = row.get('tosec_compliant_name', row['name'])
        game_name = self.sanitizeAlias(game_name)
        game = Game(game_name, int(row['wos_id']))
        publisher = self.publisherNameFromRow(row)
        game.setPublisher(publisher)
        game.setYear(row['year'])
        game.setGenre(row['genre'])
        game.x_rated = row['x_rated']
        game.setNumberOfPlayers(row['number_of_players'])
        game.setMultiplayerType(row['multiplayer_type'])
        game.setMachineType(row['machine_type'])
        game.setLanguage(row['language'])
        game.setAvailability(row['availability'])
        game.tipshop_page = row['tipshop_page']
        return game

    def releaseFromRow(self, row, game):
        release_name = row['alt_name'] if row['alt_name'] else game.name
        release_name = self.sanitizeAlias(release_name)
        publisher = self.publisherNameFromRow(row)
        release = GameRelease(row['release_seq'],
                              row['year'],
                              publisher,
                              row['country'],
                              game,
                              [release_name])
        if release.release_seq>0:
            release.addAlias(row['name'])
        # if row.get('name')!=game.name:
        #     alias = self.sanitizeAlias(row['name'])
        #     release.addAlias(alias)
        # for i, alias in enumerate(release.aliases):
        #     if alias.endswith(', 3D'):
        #         alias = '3D ' + alias[:-4]
        #     release.aliases[i] = remove_square_brackets_regex.sub('', alias).strip()
        return release

    def publisherNameFromRow(self, row):
        if row['publisher']:
            if row['publisher_is_company'] in (None, 1):
                return putPrefixToEnd(row['publisher'])
            elif row['publisher_is_company'] == 0:
                return putInitialsToEnd(row['publisher'])
        elif row['author']:
            if row['author_is_company'] in (None, 1):
                return putPrefixToEnd(row['author'])
            elif row['author_is_company'] == 0:
                return putInitialsToEnd(row['author'])

    def sanitizeAlias(self, alias):
        round_brackets_contents = re.findall(ROUND_BRACKETS_REGEX, alias)
        alias = remove_brackets_regex.sub('', alias).strip()
        alias = alias.replace('AlchNews', 'Alchemist News')
        alias = alias.replace('Zx Spectrum +', 'ZX Spectrum+')
        alias = ' - '.join([alias]+round_brackets_contents)
        if alias.endswith(', 3D'):
            alias = '3D ' + alias[:-4]
        return alias

    def gameFileFromRow(self, row, game):
        game_file = GameFile(row['file_link'], game=game, source='wos')
        game_file.size_zipped = row['file_size']
        game_file.setMachineType(row['machine_type'])
        game_file.setProtectionScheme(row['protection_scheme'])
        return game_file

    def downloadMissingFilesForGames(self, games):
        s = Scraper()
        for game in games:
            for file in game.getFiles():
                local_path = file.getLocalPath()
                if os.path.exists(local_path) and \
                        (os.path.getsize(local_path) == file.size_zipped or \
                        not file.size_zipped):
                    continue
                elif os.path.exists(local_path) and \
                                os.path.getsize(local_path) != file.size_zipped:
                    print('wrong file size:', local_path)
                else:
                    for mirror in WOS_MIRRORS:
                        try:
                            status = s.downloadFile(file.getWosPath(wos_mirror_root=mirror), local_path)
                            time.sleep(.5)
                        except:
                            print(traceback.format_exc())
                        if status == 200:
                            break
