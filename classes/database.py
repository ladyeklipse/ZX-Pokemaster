from settings import *
from classes.game import Game
from classes.game_release import GameRelease
from classes.game_file import GameFile, TOSEC_REGEX #, GAME_PREFIXES, putPrefixToEnd
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

def getSearchString(game_name):
    for prefix in GAME_PREFIXES:
        if game_name.startswith(prefix + ' '):
            game_name = game_name[len(prefix)+1:]
            break
        elif game_name.endswith(', '+prefix):
            game_name = game_name[:len(game_name)-len(prefix)-2]
    return ''.join(filter(str.isalnum, game_name.lower()))

class Database():

    cache_by_wos_id = {}
    cache_by_name = {}
    cache_by_md5 = {}

    def __init__(self):
        self.conn = sqlite3.connect('pokemaster.db')
        # self.conn.set_trace_callback(print)
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute('PRAGMA JOURNAL_MODE = OFF')

    def execute(self, sql, params=[]):
        return self.cur.execute(sql, params).fetchall()

    def loadCache(self, force_reload=False):
        if force_reload:
            self.cache_by_wos_id = {}
            self.cache_by_name = {}
            self.cache_by_md5 = {}
        if self.cache_by_name and self.cache_by_md5 and self.cache_by_wos_id:
            return
        print('started loading cache')
        games = self.getAllGames()
        print('got ', len(games), 'games')
        for game in games:
            self.cache_by_wos_id[game.wos_id]=game
            for release in game.releases:
                for name in release.getAllAliases():
                    name = getSearchString(name)
                    if not self.cache_by_name.get(name):
                        self.cache_by_name[name]=[game]
                    elif game not in self.cache_by_name[name]:
                        self.cache_by_name[name].append(game)
                for file in release.files:
                    self.cache_by_md5[file.md5]=game
        print('cache loaded')

    def addGame(self, game):
        # if not game.wos_id or not game.name:
        #     raise Exception('Cannot add game with corrupt data:'+game.getWosID()+','+game.getTOSECName())
        values = [game.wos_id if game.wos_id else None,
                  game.name,
                  game.publisher,
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
        if not game.wos_id:
            game.wos_id = self.cur.lastrowid
        for release in game.releases:
            values = [game.wos_id,
                      release.release_seq,
                      release.getName(),
                      release.year,
                      release.publisher,
                      release.country,
                      release.ingame_screen_gif_filepath,
                      release.ingame_screen_gif_filesize,
                      release.ingame_screen_scr_filepath,
                      release.ingame_screen_scr_filesize,
                      release.loading_screen_gif_filepath,
                      release.loading_screen_gif_filesize,
                      release.loading_screen_scr_filepath,
                      release.loading_screen_scr_filesize,
                      release.manual_filepath,
                      release.manual_filesize
                      ]
            sql = "INSERT OR REPLACE INTO game_release VALUES " \
                  "({})".format(','.join(['?'] * len(values)))
            self.cur.execute(sql, values)
            for file in release.files:
                try:
                    file.getMD5()
                    # file.getMD5(zipped=True)
                except:
                    print('Bad file:', file, 'for game:', game)
                    print(traceback.format_exc())
                    continue
                values = [game.wos_id,
                          release.release_seq,
                          file.wos_name,
                          file.wos_path if file.wos_name else '',
                          file.tosec_path,
                          file.machine_type,
                          file.format,
                          file.size,
                          file.content_desc,
                          file.is_demo,
                          file.part,
                          file.side,
                          file.language,
                          file.mod_flags,
                          file.notes,
                          file.getMD5(),
                          file.getCRC32(),
                          file.getSHA1()
                          ]
                sql = "INSERT OR REPLACE INTO game_file VALUES " \
                      "({})".format(','.join(['?'] * len(values)))
                self.cur.execute(sql, values)

    def commit(self):
        self.conn.commit()

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
            game_name = getSearchString(game_name)
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
            # ZxZVm - %REAL_GAME_NAME% (%YEAR%)(%PUBLISHER%) will have the same wos_id as ZxZVm
            # for game in games:
                # if game.name.split('-')[0]==game_name:
                #     return [game]
            print('Ambiguity not resolved for', game_name)
            # print(game)
            return None

    def getGameByFilePath(self, filepath):
        filename = os.path.basename(filepath)
        game_release = re.sub(TOSEC_REGEX, '', filename).strip()
        if self.cache_by_name:
            search_string = getSearchString(game_release)
            games = self.cache_by_name.get(search_string)
            if not games:
                # ZxZVm - %REAL_GAME_NAME% (%YEAR%)(%PUBLISHER%) will have the same wos_id as ZxZVm
                # search_string = getSearchString(game_release.split('-')[0].strip())
                search_string = getSearchString(game_release)
                games = self.cache_by_name.get(search_string)
        else:
            game_release = '%'.join([x for x in game_release.split(' ') if x not in GAME_PREFIXES])
            sql = SELECT_GAME_SQL_START
            sql += 'WHERE game.wos_id=' \
                   '(SELECT wos_id FROM game_release ' \
                   'WHERE game_release.name LIKE ?)'
            sql += SELECT_GAME_SQL_END
            raw_data = self.cur.execute(sql, [game_release]).fetchall()
            games = self.getGamesFromRawData(raw_data)
        if not games:
            return None
        if len(games)==1:
            return games[0]
        else:
            game_file = GameFile(filepath)
            candidates = []
            for game in games:
                if game.getPublisher() == game_file.game.getPublisher():
                    candidates.append(game)
            if len(candidates)==1:
                return candidates[0]
            else:
                for game in games:
                    if game.getYear() == game_file.game.getYear():
                        return game

    def getGamesFromRawData(self, raw_data):
        games = []
        game = Game()
        release = GameRelease()
        for row in raw_data:
            if game.wos_id != row['wos_id']:
                if game.wos_id:
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
        if game.wos_id:
            games.append(game)
        return games

    def getGameByWosID(self, wos_id):
        if self.cache_by_wos_id:
            return self.cache_by_wos_id.get(wos_id)
        sql = SELECT_GAME_SQL_START + \
              'WHERE game.wos_id=? ' + \
            SELECT_GAME_SQL_END
        raw_data = self.cur.execute(sql, [wos_id]).fetchall()
        return self.gameFromRawData(raw_data)

    def getGameByFile(self, file):
        md5 = file.getMD5()
        game = self.getGameByFileMD5(md5)
        if not game:
            game = self.getGameByFilePath(file.wos_path)
        return game

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
        game.setYear(row['year'])
        game.setGenre(row['genre'])
        game.setNumberOfPlayers(row['number_of_players'])
        game.setMultiplayerType(row['multiplayer_type'])
        game.setMachineType(row['machine_type'])
        game.setLanguage(row['language'])
        game.setAvailability(row['availability'])
        game.x_rated = row['x_rated']
        game.addRelease(self.releaseFromRow(row, game))
        game.tipshop_page = row['tipshop_page']
        if game.tipshop_page or row['pok_file_contents']:
            game.importPokFile(text=str(row['pok_file_contents']))
            game.tipshop_multiface_pokes_section = row['tipshop_multiface_pokes_section']
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
        release.ingame_screen_gif_filepath = row['ingame_screen_gif_filepath']
        release.ingame_screen_gif_size = row['ingame_screen_gif_filesize']
        release.ingame_screen_scr_filepath = row['ingame_screen_scr_filepath']
        release.ingame_screen_scr_size = row['ingame_screen_scr_filesize']
        release.loading_screen_gif_filepath = row['loading_screen_gif_filepath']
        release.loading_screen_gif_size = row['loading_screen_gif_filesize']
        release.loading_screen_scr_filepath = row['loading_screen_scr_filepath']
        release.loading_screen_scr_size = row['loading_screen_scr_filesize']
        release.manual_filepath = row['manual_filepath']
        release.manual_size = row['manual_filesize']
        if row['aliases']:
            aliases = row['aliases'].split('/')
            release.aliases = aliases
        return release


    def fileFromRow(self, row):
        if not row['md5']:
            return None
        file = GameFile()
        file.wos_name = row['wos_name']
        file.wos_path = row['wos_path']
        file.format = row['format']
        file.tosec_path = row['tosec_path']
        file.size = row['size']
        file.content_desc = row['content_desc']
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