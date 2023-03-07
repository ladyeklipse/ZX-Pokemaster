from classes.game_file import *
from classes.game import *
from classes.database import *
from lxml import etree
from copy import copy
import pickle

def refresh_tosec_aliases():
    with open('tosec_aliases.bak', 'r', encoding='utf-8') as f:
        with open('tosec_aliases.csv', 'w', encoding='utf-8') as fn:
            for line in f.readlines():
                if len(line.split(';')>1):
                    fn.write(line)
    os.rename('tosec_aliases.bak', 'tosec_aliases.bak.bak')

class TOSECScraper():

    paths = []
    manually_entered_tosec_aliases = {}
    manually_corrected_content_descriptions = {}
    manually_corrected_notes = {}
    file_exclusion_list = []
    wrong_releases = [
        ['Wrong release chosen:'],
        ['tosec_path', 'zxdb_path', 'zxdb_id', 'ZXDB TOSEC-compliant name', 'Problem']
    ]
    inconsistencies = [
        ['Presumably wrong game chosen:'],
        ['tosec_path', 'zxdb_path', 'zxdb_id', 'ZXDB TOSEC-compliant name', 'Problem']
    ]
    unscraped_file_paths = []

    def __init__(self, cache=True, db=None):
        self.getManuallyEnteredTOSECAliases()
        self.getManuallyCorrectedContentDescriptionsAndNotes()
        self.getSameMD5ExclusionList()
        # self.getPublisherAliases()
        self.db = db if db else Database()
        if cache:
            self.db.loadCache()

    def generateTOSECPathsArrayFromFolder(self, folder):
        paths = []
        cache_file = os.path.join(folder, 'cache.dump')
        if os.path.exists(cache_file):
            with open(cache_file, 'rb') as f:
                paths = pickle.load(f)
            return paths
        for root, dirs, files in os.walk(folder):
            for filename in files:
                file_path_dict = {}
                filepath = os.path.join(root, filename)
                ext = os.path.splitext(filepath)[1][1:].lower()
                if ext not in GAME_EXTENSIONS+['zip']:
                    continue
                game_file = GameFile(filepath, source='tosec')
                filename = os.path.basename(filepath)
                file_path_dict['name'] = filename
                file_path_dict['path'] = filepath
                if ext!='zip':
                    file_path_dict['size'] = os.path.getsize(filepath)
                else:
                    with zipfile.ZipFile(filepath, 'r') as zf:
                        for zfname in zf.namelist():
                            file_path_dict['size'] = zf.getinfo(zfname).file_size
                            break
                file_path_dict['md5'] = game_file.getMD5()
                file_path_dict['crc32'] = game_file.getCRC32()
                file_path_dict['sha1'] = game_file.getSHA1()
                paths.append(file_path_dict)
        with open(cache_file, 'wb') as f:
            pickle.dump(paths, f)
        print('Paths cached.')
        return paths

    def generateTOSECPathsArrayFromList(self, list):
        paths = []
        for filepath in list:
            file_path_dict = {}
            filename = os.path.basename(filepath)
            game_file = GameFile(filepath, source='tosec')
            file_path_dict['name'] = filename
            file_path_dict['path'] = filepath
            file_path_dict['size'] = os.path.getsize(filepath)
            file_path_dict['md5'] = game_file.getMD5()
            file_path_dict['crc32'] = game_file.getCRC32()
            file_path_dict['sha1'] = game_file.getSHA1()
            paths.append(file_path_dict)
        return paths

    def generateTOSECPathsArrayFromDatFiles(self, dat_files=[]):
        paths = []
        if not dat_files:
            root, dirs, files = next(os.walk('tosec\\2017 official dats'))
            dat_files = [file for file in files if file.endswith('.dat')]
        else:
            root = ''
        for dat_file in dat_files:
            dat_file = os.path.join(root, dat_file)
            for ext in GAME_EXTENSIONS:
                if '[%s]' % ext.upper() in dat_file:
                    paths += self.getPathsFromDatFile(dat_file)
        return paths

    def getPathsFromDatFile(self, dat_file):
        paths = []
        with open(dat_file, 'rb') as f:
            # print(dat_file)
            contents = f.read()
            root = etree.XML(contents)
            header = root[0]
            dirname = os.path.join(*header[0].text.split(' - '))
            games = [tag for tag in root[1:] if tag.tag in ['game', 'machine']]
            for game in games:
                roms = [tag for tag in game if tag.tag=='rom']
                if len(roms)>1:
                    print(dirname, game.attrib['name'], len(roms))
                for rom in roms:
                    file_path_dict = {}
                    file_path_dict['name'] = rom.attrib['name']
                    filename = rom.attrib['name']
                    file_path_dict['path'] = os.path.join(dirname, filename)
                    file_path_dict['size'] = rom.attrib['size']
                    file_path_dict['md5'] = rom.attrib['md5']
                    file_path_dict['crc32'] = rom.attrib['crc'].zfill(8)
                    file_path_dict['sha1'] = rom.attrib['sha1']
                    paths.append(file_path_dict)
        return paths

    def sortPaths(self):
        paths = self.paths
        paths = sorted(paths, key=lambda path_dict: (path_dict['name'], path_dict['crc32']))
        paths = sorted(paths, key=lambda path_dict: ('Compilation' in path_dict['path']))
        self.paths = paths

    def showSameMD5WarningsForFolder(self, folder):
        reviewed_files =  self.generateTOSECPathsArrayFromFolder(folder)
        tosec_md5s = {}
        for tosec_file in self.paths:
            tosec_md5s[tosec_file['md5']] = GameFile(tosec_file['name']).game.name
        warnings = 0
        for i, file in enumerate(reviewed_files):
            md5 = file['md5']
            game_name = GameFile(file['name']).game.name
            for tosec_md5 in tosec_md5s:
                tosec_game_name = tosec_md5s.get(tosec_md5)
                if md5 == tosec_md5 and game_name.lower() != tosec_game_name.lower():
                    print(i, '/', len(reviewed_files))
                    print(md5, game_name, '|', tosec_game_name)
                    warnings += 1
        print(warnings)

    def scrapeTOSEC(self):
        if not self.paths:
            raise Exception('TOSECScraper has no paths to scrape.')
        games_found = 0
        current_game = None
        current_tosec_name = ''
        for i, file_path in enumerate(self.paths):
            # print('file_path=', file_path)
            if type(file_path)==str:
                game_file = self.getGameFileFromFilePath(file_path)
            elif type(file_path)==dict:
                game_file = self.getGameFileFromFilePathDict(file_path)
            if game_file.format not in GAME_EXTENSIONS:
                continue
            if game_file.tosec_path in self.file_exclusion_list:
                print(game_file.tosec_path, 'in exclusion list.')
                continue
            if 'Covertape' in file_path['path']:
                self.setCovertapeNote(game_file)
            new_tosec_name = game_file.game.getTOSECName()
            # print(current_tosec_name, new_tosec_name)
            # print(file_path['name'])
            if current_tosec_name and current_tosec_name != new_tosec_name:
                if current_game.zxdb_id:
                    self.addGameToLocalDB(current_game)
                    games_found += 1
                current_game.files = []
                current_game = None
                if games_found and games_found % 1000 == 0:
                    print('Committing ', games_found)
                    self.db.commit()
            if not current_game:
                current_game = game_file.game
                current_tosec_name = current_game.getTOSECName()
            if current_game.zxdb_id:
                game_by_md5 = self.db.getGameByFileMD5(game_file.getMD5())
                if game_by_md5 and game_by_md5.zxdb_id!=current_game.zxdb_id:
                    current_game = game_file.game
                    current_tosec_name = current_game.getTOSECName()
            if not current_game.zxdb_id:
                game_name = game_file.game.getTOSECName()
                if game_name in self.manually_entered_tosec_aliases.keys():
                    game_zxdb_id = int(self.manually_entered_tosec_aliases[game_name])
                    game_from_db = self.db.getGameByWosID(game_zxdb_id)
                else:
                    game_from_db = self.db.getGameByFile(game_file)
                    # print("got game_from_db by file", game_file)
                # print("game_from_db=", game_from_db, "current_game=", current_game)
                if game_from_db and current_game!=game_from_db:
                    if game_from_db.name != current_game.name:
                        print("WARNING! Possible error: changing game name from ", game_file.game.name, " to ", game_from_db)
                        print("md5=", game_file.getMD5())
                    current_release = game_from_db.findReleaseByFile(game_file)
                    current_release.importInfoFromGameFile(game_file)
                    current_release.addFiles([file for file in current_game.files])
                    current_release.addFile(copy(game_file))
                    current_game.files = []
                    current_game = game_from_db
                    self.addGameToLocalDB(current_game) #fixes weird bugs
                else:
                    current_game.files.append(game_file)
            else:
                file_release = current_game.findReleaseByFile(game_file, strict=True)
                if file_release and file_release!=current_release:
                    equivalent_file = current_game.findFileByMD5(file_path['md5'])
                    if equivalent_file:
                        equivalent_file.getParamsFromTOSECPath(file_path['path'])
                        file_tosec_name = equivalent_file.getTOSECName()
                    else:
                        file_release.addFile(game_file)
                        file_tosec_name = game_file.getTOSECName()
                    self.wrong_releases.append(
                        (file_path['path'],
                         equivalent_file.wos_path if equivalent_file else '',
                         current_game.getWosID(),
                         file_tosec_name))
                else:
                    current_release.addFile(game_file)
                # print('game_File.game=',game_file.game)
                self.addGameToLocalDB(current_game)
        self.addGameToLocalDB(current_game)
        self.db.commit()

    def addGameToLocalDB(self, game):
        game.setContentDescForFiles(lookup_table=self.manually_corrected_content_descriptions)
        game.setNotesForFiles(lookup_table=self.manually_corrected_notes)
        game.setTypeFromFiles()
        game.setCountryFromFiles()
        self.db.addGame(game)

    def showUnscraped(self):
        print('Will show unscraped TOSEC files')
        sql = 'SELECT tosec_path AS path, size, md5, crc32, sha1 FROM game_file WHERE tosec_path!="" AND format!=""'
        unscraped_paths = []
        db_paths = [x['path'] for x in self.db.execute(sql)]
        game_names = []
        for path in self.paths:
            expected_path = path['path']
            if expected_path not in db_paths:
                if 'ZxZvm ' in expected_path:
                    continue
                elif 'ZZZ-UNK' in expected_path:
                    continue
                elif '(CSSCGC)' in expected_path:
                    continue
                elif 'Compilations' in expected_path:
                    continue
                elif 'Games' not in expected_path:
                    continue
                print('Unscraped: ', expected_path, path['md5'])
                unscraped_paths.append(path)
                game_file = self.getGameFileFromFilePathDict(path)
                game_name = game_file.game.getTOSECName()
                game_names.append(game_name)
        game_names = sorted(set(game_names))
        for game_name in game_names:
            print(f'game_name={game_name}')
        print('Total:', len(self.paths), 'Unscraped files:', len(unscraped_paths),
              'Games with unscraped files:', len(game_names))
        return unscraped_paths

    def getGameFileFromFilePath(self, file_path):
        file_path = file_path.replace('Lerm ', '')
        game_file = GameFile(file_path, source='tosec')
        if file_path.endswith('.zip'):
            game_file.format = os.path.split(file_path)[0][-4:-1].lower()
        else:
            game_file.format = file_path[-3:]
        game_file.format = game_file.format.split('.')[-1]
        game_file.tosec_path = file_path
        game_file.getMD5()
        game_file.getCRC32()
        game_file.getSHA1()
        game_file.setSize(os.path.getsize(file_path))
        return game_file

    def getGameFileFromFilePathDict(self, file_path_dict):
        file_path = file_path_dict['path']
        file_path = file_path.replace('Lerm ', '')
        game_file = GameFile(file_path, source='tosec')
        filename = file_path_dict['name']
        if filename.endswith('.zip'):
            game_file.format = game_file.getFormat()
        else:
            game_file.format = file_path[-3:].lower()
        game_file.format = game_file.format.split('.')[-1]
        game_file.tosec_path = file_path
        game_file.md5 = file_path_dict['md5']
        game_file.crc32 = file_path_dict['crc32'].zfill(8)
        game_file.sha1 = file_path_dict['sha1']
        game_file.setSize(file_path_dict['size'])
        return game_file

    def setCovertapeNote(self, game_file):
        file_publisher = game_file.game.publisher
        for covertape_publisher in COVERTAPE_PUBLISHERS:
            if covertape_publisher in file_publisher and len(file_publisher)>len(covertape_publisher):
                game_file.notes += '[{} Covertape]'.format(covertape_publisher)
                break

    def updateTOSECAliasesCSV(self):
        self.getManuallyEnteredTOSECAliases()
        written_game_names = []
        with open('tosec_aliases.csv', 'w', encoding='utf-8') as f:
            for key, value in self.manually_entered_tosec_aliases.items():
                f.write(';'.join((key, value))+'\n')
            for file_path in self.unscraped_file_paths:
                if type(file_path) == str:
                    game_file = self.getGameFileFromFilePath(file_path)
                elif type(file_path) == dict:
                    game_file = self.getGameFileFromFilePathDict(file_path)
                game_name = game_file.game.getTOSECName()
                if '[CSSCGC]' in game_file.notes:
                    continue
                if game_name not in written_game_names:
                    f.write(';'.join((game_name, '', game_file.getGenre()))+'\n')
                    written_game_names.append(game_name)

    def getUnscraped(self):
        have = []
        miss = []
        md5s = [row['md5'] for row in self.db.execute('SELECT md5 FROM game_file')]
        for path in self.paths:
            if path['path'] in self.file_exclusion_list:
                continue
            if path['md5'] in md5s:
                have.append(path)
            else:
                miss.append(path)
        print('Have:', len(have))
        print('Miss:', len(miss))
        return miss

    def addUnscraped(self):
        self.unscraped_file_paths = sorted(self.getUnscraped(), key=lambda file: file['name'])
        self.updateTOSECAliasesCSV()
        for file_path in self.unscraped_file_paths:
            game_file = self.getGameFileFromFilePathDict(file_path)
            game = self.db.getGameByFileMD5(game_file.getMD5())
            if not game:
                game = self.db.getGameByFilePath(file_path['path'])
            if not game:
                game = game_file.game
            game.releases[0].addFile(game_file)
            self.addGameToLocalDB(game)
        self.db.commit()
        self.unscraped_file_paths = []

    def getManuallyEnteredTOSECAliases(self):
        if not self.manually_entered_tosec_aliases:
            with open('tosec_aliases.csv', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip().split(';')
                    if len(line)<2 or not line[1]:
                        continue
                    self.manually_entered_tosec_aliases[line[0]]=line[1]

    def updateContentDescAndNotesLookupTable(self):
        self.getManuallyCorrectedContentDescriptionsAndNotes()
        content_desc_aliases_update = self.db.execute('SELECT * FROM content_desc_aliases')
        with open('content_desc_aliases.csv', 'w', encoding='utf-8') as f:
            for row in content_desc_aliases_update:
                f.write(';'.join([str(x) if x else '' for x in row])+'\n')

    def getManuallyCorrectedContentDescriptionsAndNotes(self):
        if not self.manually_corrected_content_descriptions:
            with open('content_desc_aliases.csv', 'r', encoding='utf-8', errors='replace') as f:
                for line in f.readlines():
                    line = line.strip().replace('\t', ';').split(';')
                    if line[2].startswith('NONE') or line[2].startswith('ALT'):
                        md5 = line[7]
                        self.manually_corrected_content_descriptions[md5] = line[2]
                    notes = line[6]
                    if notes.startswith('NONE') or notes.startswith('ALT'):
                        md5 = line[7]
                        self.manually_corrected_notes[md5] = notes

    def getSameMD5ExclusionList(self):
        if not self.file_exclusion_list:
            with open('same_md5.csv', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.split(';')
                    decision = line[7]
                    if not decision.startswith('KEEP') and line[11]:
                        self.file_exclusion_list.append(line[11])
