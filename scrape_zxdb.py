from classes.database import *
from classes.game import Game
from classes.game_release import GameRelease
from classes.game_file import GameFile
from classes.game_alias import GameAlias
from classes.scraper import *
from mysql import connector
import time

class RowConverter(connector.conversion.MySQLConverter):

    def row_to_python(self, row, fields):
        row = super(RowConverter, self).row_to_python(row, fields)
        def to_unicode(col):
            if type(col) == bytearray:
                return col.decode('utf-8')
            return col
        return[to_unicode(col) for col in row]

class ZXDB():

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

    def getAllGames(self):
        sql = 'SELECT entries.id AS wos_id, ' \
              'releases.release_seq AS release_seq, ' \
              'entries.title AS name, ' \
              'entries.is_xrated AS x_rated, ' \
              'genretypes.text AS genre, ' \
              'entries.max_players AS number_of_players, ' \
              'entries.multiplaytype_id AS multiplay_type, ' \
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
              'releases.release_seq AS release_id, ' \
              'aliases.title AS alt_name, ' \
              'aliases.idiom_id AS alt_language, ' \
              'labels.name AS publisher, ' \
              'releases.release_year AS year,' \
              'labels.country_id AS country ' \
              'FROM entries ' \
              'LEFT JOIN releases ON entries.id=releases.entry_id ' \
              'LEFT JOIN downloads ON downloads.entry_id=entries.id AND downloads.release_seq=releases.release_seq ' \
              'LEFT JOIN publishers ON publishers.entry_id=entries.id AND publishers.release_seq=releases.release_seq  ' \
              'LEFT JOIN labels ON labels.id=publishers.label_id ' \
              'LEFT JOIN aliases ON aliases.entry_id=entries.id AND aliases.release_seq=releases.release_seq ' \
              'LEFT JOIN filetypes ON downloads.filetype_id=filetypes.id ' \
              'LEFT JOIN formattypes ON downloads.formattype_id=formattypes.id ' \
              'LEFT JOIN genretypes ON genretypes.id=entries.genretype_id ' \
              'LEFT JOIN machinetypes download_machinetype ON download_machinetype.id=downloads.machinetype_id ' \
              'LEFT JOIN machinetypes entry_machinetype ON entry_machinetype.id=entries.machinetype_id ' \
              'WHERE (entries.id>4000000 OR entries.id<1000000) AND ' \
              '(publisher_seq IS NULL OR publisher_seq=1) ' \
              'ORDER BY wos_id, release_seq, entries.title IS NOT NULL ' \
              'LIMIT 1000000'
              # 'WHERE (downloads.filetype_id IS NULL OR ' \
              # 'downloads.filetype_id IN (-1, 0, 1, 2, 8, 10, 11, 17, 20, 21, 28)) AND ' \
              # '(publisher_seq IS NULL OR publisher_seq=1) ' \
              # 'ORDER BY wos_id, release_seq, entries.title IS NOT NULL ' \
              # 'LIMIT 500000'
        print(sql)
        self.cur.execute(sql)
        game = Game()
        release = GameRelease()
        games = []
        for row in self.cur:
            # print(row['wos_id'], row['release_seq'])
            # continue
            # print(row['wos_id'], row['release_seq'])
            if row['wos_id'] and row['name'] and row['wos_id']!=game.wos_id:
                # if game.wos_id:
                #     games.append(game)
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
                            # print(game, game.loading_screen_gif_filepath, row['file_link'])
                            # print('Duplicate loading screen GIF')
                        else:
                            release.loading_screen_gif_filepath = row['file_link']
                            release.loading_screen_gif_filesize = row['file_size']
                    elif row['file_format']=='Screen dump':
                        if release.loading_screen_scr_filepath and \
                                        release.loading_screen_scr_filepath!=row['file_link']:
                            pass
                            # print(game)
                            # print('Duplicate loading screen SCR')
                        else:
                            release.loading_screen_scr_filepath = row['file_link']
                            release.loading_screen_scr_filesize = row['file_size']
                elif row['file_type']=='In-game screen':
                    if row['file_format']=='Picture':
                        if release.ingame_screen_gif_filepath and \
                                        release.ingame_screen_gif_filepath!=row['file_link']:
                            pass
                            # print(game, game.ingame_screen_gif_filepath, row['file_link'])
                            # print('Duplicate ingame screen gif')
                        else:
                            release.ingame_screen_gif_filepath = row['file_link']
                            release.ingame_screen_gif_filesize = row['file_size']
                    elif row['file_format'] == 'Screen dump':
                        if release.ingame_screen_scr_filepath and \
                                        release.ingame_screen_scr_filepath != row['file_link']:
                            # print(game, game.ingame_screen_scr_filepath, row['file_link'])
                            # print('Duplicate ingame screen gif')
                            pass
                        else:
                            release.ingame_screen_scr_filepath = row['file_link']
                            release.ingame_screen_scr_filesize = row['file_size']
                elif row['file_type']=='Instructions' and row['file_link'].endswith('.txt'):
                    if release.manual_filepath and \
                                    release.manual_filepath!=row['file_link']:
                        pass
                        # print(game, game.manual_filepath, row['file_link'])
                        # print('Duplicate manual')
                    else:
                        release.manual_filepath = row['file_link']
                        release.manual_filesize = row['file_size']
                elif row['file_format'] and \
                        ('snapshot' in row['file_format'] or \
                         'disk' in row['file_format'] or \
                         'tape' in row['file_format']):
                    game_file = self.gameFileFromRow(row, game)
                    release.addFile(game_file)
                if row['alt_name']:
                    release.addAlias(row['alt_name'], row['alt_language'])
        games.append(game)
        return games

    def gameFromRow(self, row):
        game = Game(row['name'], int(row['wos_id']))
        game.setPublisher(row['publisher'])
        game.setYear(row['year'])
        game.setGenre(row['genre'])
        game.x_rated = row['x_rated']
        game.setNumberOfPlayers(row['number_of_players'])
        game.setMachineType(row['machine_type'])
        game.setLanguage(row['language'])
        game.setAvailability(row['availability'])
        return game

    def releaseFromRow(self, row, game):
        release = GameRelease(row['release_seq'],
                              row['year'],
                              row['publisher'],
                              row['country'],
                              game)
        return release

    def gameFileFromRow(self, row, game):
        game_file = GameFile(row['file_link'], game=game)
        game_file.setSize(row['file_size'], zipped=True)
        game_file.setMachineType(row['machine_type'])
        return game_file

if __name__=='__main__':
    zxdb = ZXDB()
    start_time = time.clock()
    games = zxdb.getAllGames()
    end_time = time.clock()
    print('got in:', end_time - start_time)
    db = Database()
    s = Scraper()
    for game in games:
        for file in game.getFiles():
            local_path = file.getLocalPath(zipped=True)
            if os.path.exists(local_path) and \
                    os.path.getsize(local_path):
                continue
            elif os.path.exists(local_path) and \
                os.path.getsize(local_path)!=file.size:
                print('wrong file size:', local_path)
            else:
                continue
                for mirror in WOS_MIRRORS:
                    try:
                        status = s.downloadFile(file.getWosPath(wos_mirror_root=mirror), local_path)
                    except:
                        print(traceback.format_exc())
                    if status == 200:
                        break

        for release in game.releases:
            try:
                release.getInfoFromLocalFiles()
            except:
                print(traceback.format_exc())
            continue
            if release.ingame_screen_gif_filesize:
                path = release.getIngameScreenFilePath('gif')
                local_path = LOCAL_FTP_ROOT+path
                if not os.path.exists(local_path) or \
                                os.path.getsize(local_path)==0:# != release.ingame_screen_gif_filesize:
                    for mirror in WOS_MIRRORS:
                        status = s.downloadFile(mirror+path, local_path)
                        if status==200:
                            break

            if release.loading_screen_scr_filesize:
                path = release.getLoadingScreenFilePath('scr')
                local_path = LOCAL_FTP_ROOT+path
                if not os.path.exists(local_path) or \
                                os.path.getsize(local_path)==0:# != release.loading_screen_scr_filesize:
                    for mirror in WOS_MIRRORS:
                        status = s.downloadFile(mirror+path, local_path)
                        if status==200:
                            break

            if release.loading_screen_gif_filesize:
                path = release.getLoadingScreenFilePath('gif')
                local_path = LOCAL_FTP_ROOT+path
                if not os.path.exists(local_path) or \
                                os.path.getsize(local_path)==0:# != release.loading_screen_gif_filesize:
                    for mirror in WOS_MIRRORS:
                        status = s.downloadFile(mirror+path, local_path)
                        if status==200:
                            break

            if release.manual_filesize:
                path = release.manual_filepath
                local_path = LOCAL_FTP_ROOT+path
                if not os.path.exists(local_path) or \
                        not os.path.getsize(local_path):
                        #os.path.getsize(local_path) != release.manual_filesize:
                    for mirror in WOS_MIRRORS:
                        status = s.downloadFile(mirror + path, local_path)
                        if status == 200:
                            break
                # else:
                #     print('File', local_path, 'OK')

        # print(game, len(game.releases))
        # for release in game.releases:
        #     print(release, release.files)
    for game in games:
        db.addGame(game)
    db.commit()
    print(len(games))
    print(len(set([game.wos_id for game in games])))
