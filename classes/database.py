from settings import *
from classes.game import Game
from classes.game_file import GameFile, TOSEC_REGEX
import re
import sqlite3

GAME_PREFIXES = ['3D',
                 'A', 'The',
                 'La', 'Le', 'De', "L'",
                 'Les', 'Los', 'Las', 'El',
                 'Une', 'Una', 'Uno',
                 'Het',
                 'Der', 'Die', 'Das']

SELECT_GAME_SQL_START = 'SELECT *, ' \
                        'game.wos_id AS wos_id, ' \
                        'game_file.machine_type AS file_machine_type, ' \
                        'game_file.language AS file_language ' \
                        'FROM game ' \
              'LEFT JOIN game_file ' \
              'ON game_file.game_wos_id==game.wos_id ' \
              'LEFT JOIN game_release ' \
              'ON game_release.wos_id==game.wos_id '

class Database():

    def __init__(self):
        self.conn = sqlite3.connect('pokemaster.db')
        self.conn.row_factory = sqlite3.Row
        self.cur = self.conn.cursor()
        self.cur.execute('PRAGMA JOURNAL_MODE = OFF')

    def execute(self, sql, params=[]):
        return self.cur.execute(sql, params).fetchall()

    def addGame(self, game):
        values = [game.wos_id,
                  game.name,
                  game.publisher,
                  game.year,
                  game.genre,
                  game.number_of_players,
                  game.machine_type,
                  game.language,
                  game.availability,
                  game.ingame_screen_filename,
                  game.loading_screen_filename,
                  game.manual_filename,
                  game.has_tipshop_page,
                  game.getPokFileContents(),
                  game.tipshop_multiface_pokes_section]
        sql = "INSERT OR REPLACE INTO game VALUES " \
              "({})".format(','.join(['?']*len(values)))
        self.cur.execute(sql, values)
        for file in game.files:
            values = [game.wos_id,
                      file.wos_name,
                      file.wos_zipped_name,
                      file.tosec_name,
                      file.machine_type,
                      file.format,
                      file.size,
                      file.size_zipped,
                      file.part,
                      file.side,
                      file.language,
                      file.getMD5(),
                      file.getMD5(zipped=True)]
            sql = "INSERT OR REPLACE INTO game_file VALUES " \
                  "({})".format(','.join(['?'] * len(values)))
            self.cur.execute(sql, values)

    def commit(self):
        self.conn.commit()

    def getAllGames(self, condition=None):
        sql = SELECT_GAME_SQL_START
        if condition:
            sql += 'WHERE '+condition
        raw_data = self.cur.execute(sql).fetchall()
        games = self.getGamesFromRawData(raw_data)
        return games

    def getGameByFileName(self, filename):
        game_release = re.sub(TOSEC_REGEX, '', filename).strip()
        game_release = game_release.replace(' ', '%')
        for prefix in GAME_PREFIXES:
            if game_release.startswith(prefix+' '):
                game_release = ' '.join(game_release.split(' ')[1:]) + ', ' + prefix
                break
        sql = SELECT_GAME_SQL_START + \
            'where game.name LIKE ?'
        raw_data = self.cur.execute(sql, [game_release]).fetchall()
        games = self.getGamesFromRawData(raw_data)
        if not games:
            return None
        if len(games)==1:
            return games[0]
        else:
            game_file = GameFile(filename)
            candidates = []
            for game in games:
                if game.getYear()==game_file.game.getYear():
                    candidates.append(game)
            if len(candidates)==1:
                return candidates[0]
            else:
                for game in games:
                    if game.getPublisher()==game_file.game.getPublisher():
                        return game

    def getGamesFromRawData(self, raw_data):
        games = []
        game = Game()
        for row in raw_data:
            if game.wos_id == row['wos_id']:
                file = self.fileFromRow(row)
                game.addFile(file)
            else:
                game = self.gameFromRow(row)
                games.append(game)
        return games

    def getGameByWosID(self, wos_id):
        sql = SELECT_GAME_SQL_START + \
              'WHERE game.wos_id=?'
        raw_data = self.cur.execute(sql, [wos_id]).fetchall()
        return self.gameFromRawData(raw_data)

    def getGameByFile(self, file):
        # md5_zipped = file.getMD5(zipped=True)
        # game = self.getGameByFileMD5(md5_zipped)
        # if not game:
        md5 = file.getMD5()
        game = self.getGameByFileMD5(md5)
        if not game:
            game = self.getGameByFileName(file.getFileName())
        return game

    def getGameByFileMD5(self, md5, zipped=False):
        sql = SELECT_GAME_SQL_START
        if zipped:
            sql += 'WHERE game_file.md5_zipped="{}"'.format(md5)
        else:
            sql += 'WHERE game_file.md5="{}"'.format(md5)
        raw_data = self.cur.execute(sql).fetchall()
        return self.gameFromRawData(raw_data)

    def gameFromRawData(self, raw_data):
        if not raw_data:
            return None
        game = self.gameFromRow(raw_data[0])
        for row in raw_data:
            file = self.fileFromRow(row)
            game.addFile(file)
        return game

    def gameFromRow(self, row):
        game = Game(row['name'], int(row['wos_id']))
        game.setPublisher(row['publisher'])
        game.setYear(row['year'])
        game.setGenre(row['genre'])
        game.setNumberOfPlayers(row['number_of_players'])
        game.setMachineType(row['machine_type'])
        game.setLanguage(row['language'])
        game.setAvailability(row['availability'])
        game.ingame_screen_filename = row['ingame_screen_filename']
        game.loading_screen_filename = row['loading_screen_filename']
        game.manual_filename = row['manual_filename']
        game.has_tipshop_page = row['has_tipshop_page']
        if game.has_tipshop_page:
            game.importPokFile(text=str(row['pok_file_contents']))
            game.tipshop_multiface_pokes_section = row['tipshop_multiface_pokes_section']
        if row['md5']:
            game.addFile(self.fileFromRow(row))
        return game

    def fileFromRow(self, row):
        if not row['md5']:
            return None
        file = GameFile()
        file.wos_name = row['wos_name']
        file.wos_zipped_name = row['wos_zipped_name']
        file.format = row['format']
        file.md5 = row['md5']
        file.md5_zipped = row['md5_zipped']
        file.tosec_name = row['tosec_name']
        file.size = row['size']
        file.machine_type = row['file_machine_type']
        file.part = row['part']
        file.side = row['side']
        file.language = row['file_language']
        return file



