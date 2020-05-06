from settings import *
from classes.game import Game
from classes.game_release import GameRelease
from classes.game_file import GameFile, TOSEC_REGEX
from functions.game_name_functions import getSearchStringFromGameName
import re
import os
import sqlite3
import traceback

SELECT_GAME_SQL_START = 'SELECT *, ' \
                        'game.wos_id AS wos_id, ' \
                        'game_file.machine_type AS file_machine_type, ' \
                        'game_file.language AS file_language, ' \
                        'game_release.name AS aliases, ' \
                        'game_release.year AS release_year, ' \
                        'game_release.publisher AS release_publisher, ' \
                        'game_release.country AS release_country ' \
                        'FROM game ' \
              'LEFT JOIN game_release ' \
              'ON game_release.wos_id==game.wos_id ' \
              'LEFT JOIN game_file ' \
              'ON game_file.game_wos_id==game.wos_id AND ' \
              'game_file.game_release_seq=game_release.release_seq '
SELECT_GAME_SQL_END = ' ORDER BY game.wos_id, game_release.release_seq'

class Database():

    def __init__(self, path=POKEMASTER_DB_PATH):
        self.cache_by_zxdb_id = {}
        self.cache_by_name = {}
        self.cache_by_md5 = {}
        self.cache_by_crc32 = {}
        self.game_name_aliases = {}
        self.publisher_aliases = {}
        if os.path.exists(path):
            self.conn = sqlite3.connect(path)
            print("Connected to", path)
        elif os.path.exists(POKEMASTER_MIN_DB_PATH):
            self.conn = sqlite3.connect(POKEMASTER_MIN_DB_PATH)
            print("Connected to", POKEMASTER_MIN_DB_PATH)
        else:
            self.conn = sqlite3.connect(POKEMASTER_DB_PATH)
            print("Connected to", POKEMASTER_DB_PATH)
        # self.conn.set_trace_callback(print)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute('PRAGMA JOURNAL_MODE = OFF')

    def execute(self, sql, params=[]):
        return self.cur.execute(sql, params).fetchall()

    def loadCache(self, force_reload=False):
        if force_reload:
            self.cache_by_zxdb_id = {}
            self.cache_by_name = {}
            self.cache_by_md5 = {}
            self.cache_by_crc32 = {}
        if len(self.cache_by_md5):
            return
        print('started loading cache')
        games = self.getAllGames()
        print('got ', len(games), 'games')
        for game in games:
            self.loadGameInCache(game)
        print('cache loaded')

    def loadGameInCache(self, game):
        self.cache_by_zxdb_id[game.zxdb_id]=game
        for release in game.releases:
            for name in release.getAllAliases():
                name = getSearchStringFromGameName(name)
                if not self.cache_by_name.get(name):
                    self.cache_by_name[name]=[game]
                elif game not in self.cache_by_name[name]:
                    self.cache_by_name[name].append(game)
            for file in release.files:
                self.cache_by_md5[file.md5]=game
                if not self.cache_by_crc32.get(file.crc32):
                    self.cache_by_crc32[file.crc32] = []
                self.cache_by_crc32[file.crc32].append(game)

    def loadLookupTables(self):
        with open('publisher_aliases.csv', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip().split(';')
                if not line[1]:
                    break
                self.publisher_aliases[line[0]]=line[1]
        with open('game_name_aliases.csv', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.strip().split(';')
                if not line[1]:
                    break
                self.game_name_aliases[line[0]]=line[1]

    def addGame(self, game):
        if not self.publisher_aliases:
            self.loadLookupTables()
        if game.publisher in self.publisher_aliases:
            game.publisher = self.publisher_aliases[game.publisher]
        if game.author in self.publisher_aliases:
            game.author = self.publisher_aliases[game.author]
        if game.name in self.game_name_aliases:
            game.name = self.game_name_aliases[game.name]
        for release in game.releases:
            if release.getName() in self.game_name_aliases:
                release.aliases = [self.game_name_aliases[release.name]]
            if release.publisher in self.publisher_aliases:
                release.publisher = self.publisher_aliases[release.publisher]
            if not release.publisher or release.publisher=='-':
                release.publisher = game.publisher
        if  not game.zxdb_id:
            for file in game.getFiles():
                file.sortPublishers()
        values = [game.zxdb_id if game.zxdb_id else None,
                  game.name,
                  game.publisher,
                  game.author,
                  game.year,
                  game.genre,
                  game.x_rated,
                  game.number_of_players,
                  game.multiplayer_type,
                  game.machine_type,
                  game.language,
                  game.availability,
                  game.tipshop_page,
                  game.getPokFileContents(),
                  game.tipshop_multiface_pokes_section]
        sql = "INSERT OR REPLACE INTO game VALUES " \
              "({})".format(','.join(['?']*len(values)))
        self.cur.execute(sql, values)
        if not game.zxdb_id:
            game.zxdb_id = self.cur.lastrowid
        for release in game.releases:
            values = [game.zxdb_id,
                      release.release_seq,
                      release.getName(),
                      release.year,
                      release.publisher,
                      release.country,
                      ]
            sql = "INSERT OR REPLACE INTO game_release VALUES " \
                  "({})".format(','.join(['?'] * len(values)))
            self.cur.execute(sql, values)
            for file in release.files:
                try:
                    file.getMD5()
                except:
                    print('Bad file:', file, 'for game:', game)
                    print(traceback.format_exc())
                    continue
                file.sortModFlags()
                file.sortNotes()
                values = [game.zxdb_id,
                          release.release_seq,
                          file.wos_name,
                          file.wos_path if file.wos_name else '',
                          file.tosec_path,
                          file.machine_type,
                          file.format,
                          file.size,
                          file.content_desc,
                          file.is_demo,
                          file.release_date,
                          file.part,
                          file.side,
                          file.language,
                          file.mod_flags,
                          file.notes,
                          file.getMD5(),
                          file.getCRC32(),
                          file.getSHA1()
                          ]
                # print(file.tosec_path, file.getMD5())
                sql = "INSERT OR REPLACE INTO game_file VALUES " \
                      "({})".format(','.join(['?'] * len(values)))
                self.cur.execute(sql, values)
        if self.cache_by_md5:
            self.loadGameInCache(game)


    def commit(self):
        self.conn.commit()

    def getGameNameAliases(self):
        game_names = self.execute('SELECT wos_id, game_name FROM ')

    def getAllGames(self, condition=None):
        sql = SELECT_GAME_SQL_START
        if condition:
            sql += 'WHERE '+condition
        sql += SELECT_GAME_SQL_END
        raw_data = self.cur.execute(sql).fetchall()
        games = self.getGamesFromRawData(raw_data)
        return games

    def getGameByName(self, game_name):
        if self.cache_by_name:
            game_name = getSearchStringFromGameName(game_name)
            games = self.cache_by_name.get(game_name)
        else:
            sql = SELECT_GAME_SQL_START + \
                'WHERE game.name=? '
            sql += SELECT_GAME_SQL_END
            raw_data = self.cur.execute(sql, [game_name]).fetchall()
            games = self.getGamesFromRawData(raw_data)
        if not games:
            print('Game', game_name, 'not found')
            return None
        elif len(games)==1:
            return games[0]
        else:
            print('Ambiguity not resolved for', game_name)
            return None

    def getGameByFilePath(self, filepath):
        filename = os.path.basename(filepath)
        game_release = re.sub(TOSEC_REGEX, '', filename).strip()
        version = re.findall('v[0-9].*', game_release)
        if version:
            game_release = game_release.replace(version[0], '').strip()
        if self.cache_by_name:
            search_string = getSearchStringFromGameName(game_release)
            games = self.cache_by_name.get(search_string)
            if not games:
                if ' - ' in game_release:
                    search_string = getSearchStringFromGameName(game_release.split(' - ')[0])
                    games = self.cache_by_name.get(search_string)
                elif ' + ' in game_release:
                    search_string = getSearchStringFromGameName(game_release.split(' + ')[0])
                    games = self.cache_by_name.get(search_string)
        else:
            game_release = '%'+'%'.join([x for x in game_release.split(' ') if x not in GAME_PREFIXES])+'%'
            sql = SELECT_GAME_SQL_START
            sql += 'WHERE game.wos_id IN ' \
                   '(SELECT wos_id FROM game_release ' \
                   'WHERE game_release.name LIKE ?)'
            sql += SELECT_GAME_SQL_END
            raw_data = self.cur.execute(sql, [game_release]).fetchall()
            games = self.getGamesFromRawData(raw_data)
            if not games:
                if '%-%' in game_release:
                    game_release = game_release.split('%-%')[0]+"%"
                    raw_data = self.cur.execute(sql, [game_release]).fetchall()
                    games = self.getGamesFromRawData(raw_data)
                elif '%+%' in game_release:
                    game_release = game_release.split('%+%')[0]+"%"
                    raw_data = self.cur.execute(sql, [game_release]).fetchall()
                    games = self.getGamesFromRawData(raw_data)
        if not games:
            return None
        game_file = GameFile(filepath)
        if len(games)==1:
            game = games[0]
            for release in game.releases:
                if release.getYear() == game_file.game.getYear():
                    return game
                release_publisher = getSearchStringFromGameName(release.getPublisher())
                game_file_publisher = getSearchStringFromGameName(game_file.game.getPublisher())
                if release_publisher == game_file_publisher:
                    return game
        candidates = []
        for game in games:
            for release in game.releases:
                release_publisher = getSearchStringFromGameName(release.getPublisher())
                game_file_publisher = getSearchStringFromGameName(game_file.game.getPublisher())
                if game_file_publisher in release_publisher:
                    candidates.append(game)
        if len(candidates)==1:
            return candidates[0]
        else:
            for game in candidates:
                for release in game.releases:
                    if release.getYear() == game_file.game.getYear():
                        return game
        return None

    def getGamesFromRawData(self, raw_data):
        games = []
        game = Game()
        release = GameRelease()
        for row in raw_data:
            if game.zxdb_id != row['wos_id']:
                if game.zxdb_id:
                    games.append(game)
                game = self.gameFromRow(row)
                game.releases = []
                release = self.releaseFromRow(row, game)
                game.addRelease(release)
            if release.release_seq!=row['release_seq']:
                release = self.releaseFromRow(row, game)
                game.addRelease(release)
            file = self.fileFromRow(row)
            if file:
                game.addFile(file, release_seq = row['release_seq'])
                if file.part > game.parts:
                    game.parts = file.part
        if game.zxdb_id:
            games.append(game)
        return games

    def getGameByWosID(self, zxdb_id):
        if self.cache_by_zxdb_id:
            return self.cache_by_zxdb_id.get(zxdb_id)
        sql = SELECT_GAME_SQL_START + \
              'WHERE game.wos_id=? ' + \
            SELECT_GAME_SQL_END
        raw_data = self.cur.execute(sql, [zxdb_id]).fetchall()
        return self.gameFromRawData(raw_data)


    def getGameByFile(self, file):
        md5 = file.getMD5()
        game = self.getGameByFileMD5(md5)
        # print('got game by md5:', md5, game)
        if not game:
            game = self.getGameByFilePath(file.getPath())
        return game

    def getGamesByFileCRC32(self, crc32):
        if self.cache_by_crc32:
            return self.cache_by_crc32.get(crc32, [])
        sql = SELECT_GAME_SQL_START
        sql += 'WHERE game.wos_id IN ' \
               '(SELECT game_wos_id FROM game_file ' \
               'WHERE game_file.crc32="{}")'.format(crc32)
        sql += SELECT_GAME_SQL_END
        raw_data = self.cur.execute(sql).fetchall()
        return self.getGamesFromRawData(raw_data)

    def getGameByFileMD5(self, md5, zipped=False):
        if self.cache_by_md5:
            return self.cache_by_md5.get(md5)
        sql = SELECT_GAME_SQL_START
        sql += 'WHERE game.wos_id=' \
               '(SELECT game_wos_id FROM game_file ' \
               'WHERE game_file.md5="{}")'.format(md5)
        sql += SELECT_GAME_SQL_END
        raw_data = self.cur.execute(sql).fetchall()
        return self.gameFromRawData(raw_data)

    def gameFromRawData(self, raw_data):
        if not raw_data:
            return None
        game = self.gameFromRow(raw_data[0])
        for row in raw_data:
            if len(game.releases)==row['release_seq']:
                release = self.releaseFromRow(row, game)
                game.addRelease(release)
            file = self.fileFromRow(row)
            if file:
                game.addFile(file, release_seq=len(game.releases)-1)
                if file.part>game.parts:
                    game.parts=file.part
        return game

    def gameFromRow(self, row):
        game = Game(row['name'], int(row['wos_id']))
        game.setPublisher(row['publisher'])
        if 'author' in row.keys():
            game.setAuthor(row['author'])
        game.setYear(row['year'])
        game.setGenre(row['genre'])
        game.setNumberOfPlayers(row['number_of_players'])
        game.setMachineType(row['machine_type'])
        game.setLanguage(row['language'])
        game.setAvailability(row['availability'])
        game.x_rated = row['x_rated']
        game.addRelease(self.releaseFromRow(row, game))
        if 'multiplayer_type' in row.keys():
            game.setMultiplayerType(row['multiplayer_type'])
        if 'tipshop_page' in row.keys():
            game.tipshop_page = row['tipshop_page']
            game.tipshop_multiface_pokes_section = row['tipshop_multiface_pokes_section']
        if game.tipshop_page or row['pok_file_contents']:
            game.importPokFile(text=str(row['pok_file_contents']))
        if row['md5']:
            file = self.fileFromRow(row)
            game.addFile(file)
            if file.part > game.parts:
                game.parts = file.part
        return game

    def releaseFromRow(self, row, game):
        release = GameRelease(row['release_seq'],
                              row['release_year'],
                              row['release_publisher'],
                              row['release_country'],
                              game)
        if row['aliases']:
            aliases = row['aliases'].split('/')
            release.aliases = aliases
        return release

    def fileFromRow(self, row):
        if not row['md5']:
            return None
        file = GameFile()
        if 'wos_name' in row.keys():
            file.wos_name = row['wos_name']
            file.wos_path = row['wos_path']
        if 'tosec_path' in row.keys():
            file.tosec_path = row['tosec_path']
        file.format = row['format']
        file.size = row['size']
        file.content_desc = row['content_desc']
        file.release_date = row['release_date']
        file.is_demo = row['is_demo']
        file.setMachineType(row['file_machine_type'])
        file.part = row['part']
        file.side = row['side']
        file.language = row['file_language']
        file.mod_flags = row['mod_flags']
        file.notes = row['notes']
        file.md5 = row['md5']
        file.crc32 = row['crc32']
        file.sha1 = row['sha1']
        return file

if __name__=='__main__':
    os.chdir('..')
    from scripts.restore_db import *
    restoreDB()
    db = Database()
    game_file = GameFile("Sinclair ZX Spectrum\Games\[TAP]\Robin of the Wood (1985)(Odin Computer Graphics).tap")
    game_file.md5 = "f16538ac3cb55bbbb878c42c04b17de5"
    game = db.getGameByFile(game_file)
    print(game)