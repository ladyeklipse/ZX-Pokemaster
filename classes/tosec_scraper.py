from classes.game_file import *
from classes.game import *
from classes.database import *
from lxml import etree

def refresh_tosec_aliases():
    with open('tosec_aliases.bak', 'r', encoding='utf-8') as f:
        with open('tosec_aliases.txt', 'w', encoding='utf-8') as fn:
            for line in f.readlines():
                if '|' in line:
                    fn.write(line)
    os.rename('tosec_aliaes.bak', 'tosec_aliases.bak.bak')

class TOSECScraper():

    paths = []
    manually_entered_tosec_aliases = {}

    def __init__(self, cache=True, db=None):
        self.db = db if db else Database()
        if cache:
            self.db.loadCache()

    def generateTOSECPathsArray(self):
        categories = ['Applications',
                      'Compilations\Applications',
                      'Compilations\Demos',
                      'Compilations\Educational',
                      'Compilations\Games',
                      'Compilations\Magazines',
                      'Covertapes',
                      'Demos',
                      'Documentation',
                      'Educational',
                      'Magazines',
                      'Games']
        tosec_folders = ['[%s]' % x.upper() for x in GAME_EXTENSIONS]
        paths = []
        for category in categories:
            for folder in tosec_folders:
                for root, dirs, files in os.walk(os.path.join('tosec', category, folder)):
                    for filename in files:
                        if filename.endswith('.zip'):
                            paths.append((filename, os.path.join(root, filename)))
        paths = sorted(paths, key=lambda path: path[0])
        self.paths = [path[1] for path in paths]
        return self.paths

    def generateTOSECPathsArrayFromDatFiles(self, dat_files=[]):
        paths = []
        if not dat_files:
            root, dirs, files = next(os.walk('tosec'))
            dat_files = [file for file in files if file.endswith('.dat')]
        for dat_file in dat_files:
            dat_file = os.path.join(root, dat_file)
            for ext in GAME_EXTENSIONS:
                if '[%s]' % ext.upper() in dat_file:
                    paths += self.getPathsFromDatFile(dat_file)
        paths = sorted(paths, key=lambda path_dict: path_dict['name'])
        paths = sorted(paths, key=lambda path_dict: 'Compilation' in path_dict['path'])
        return paths

    def getPathsFromDatFile(self, dat_file):
        paths = []
        with open(dat_file, 'r', encoding='utf-8') as f:
            root = etree.fromstring(f.read())
            header = root[0]
            path = os.path.join(*header[0].text.split(' - ')[1:])
            games = [tag for tag in root[1:] if tag.tag=='game']
            for game in games:
                roms = [tag for tag in game if tag.tag=='rom']
                if len(roms)>1:
                    print(path, game.attrib['name'], len(roms))
                for rom in roms:
                    file_path_dict = {}
                    file_path_dict['name'] = rom.attrib['name']
                    file_path_dict['path'] = os.path.join('tosec', path, rom.attrib['name'])
                    file_path_dict['size'] = rom.attrib['size']
                    file_path_dict['md5'] = rom.attrib['md5']
                    file_path_dict['crc32'] = rom.attrib['crc']
                    file_path_dict['sha1'] = rom.attrib['sha1']
                    paths.append(file_path_dict)
        return paths


    def scrapeTOSEC(self):
        self.getTOSECAliases()
        if not self.paths:
            self.generateTOSECPathsArray()
        games_found = 0
        current_game = None
        current_tosec_name = ''
        for file_path in self.paths:
            print(file_path)
            if type(file_path)==str:
                game_file = self.getGameFileFromFilePath(file_path)
            elif type(file_path)==dict:
                game_file = self.getGameFileFromFilePathDict(file_path)
            new_tosec_name = game_file.game.getTOSECName()
            if current_tosec_name and current_tosec_name != new_tosec_name:
                if current_game.wos_id:
                    self.db.addGame(current_game)
                    games_found += 1
                current_game.files = []
                current_game = None
                if games_found % 1000 == 0:
                    self.db.commit()
            if not current_game:
                current_game = game_file.game
                current_tosec_name = current_game.getTOSECName()
            if not current_game.wos_id:
                game_name = game_file.game.getTOSECName()
                if game_name in self.manually_entered_tosec_aliases.keys():
                    game_wos_id = int(self.manually_entered_tosec_aliases[game_name])
                    game_from_db = self.db.getGameByWosID(game_wos_id)
                else:
                    game_from_db = self.db.getGameByFile(game_file)
                if game_from_db and current_game!=game_from_db:
                    current_release = game_from_db.findReleaseByFile(game_file)
                    current_release.addFiles([file for file in current_game.files])
                    current_release.addFile(game_file)
                    current_game.files = []
                    current_game = game_from_db
                else:
                    current_game.files.append(game_file)
            else:
                current_release.addFile(game_file)
        if current_game.wos_id:
            self.db.addGame(current_game)
        self.db.commit()


    def getGameFileFromFilePath(self, file_path):
        game_file = GameFile(file_path)
        game_file.format = os.path.split(file_path)[0][-4:-1].lower()
        game_file.tosec_path = file_path
        game_file.getMD5(zipped=False)
        game_file.setSize(os.path.getsize(file_path), zipped=True)
        return game_file

    def getGameFileFromFilePathDict(self, file_path):
        game_file = GameFile(file_path['path'])
        game_file.format = os.path.splitext(file_path['path'])[1][1:].lower()
        game_file.tosec_path = file_path['path']
        game_file.md5 = file_path['md5']
        game_file.crc32 = file_path['crc32']
        game_file.sha1 = file_path['sha1']
        game_file.setSize(file_path['size'])
        return game_file

    def getTOSECAliases(self):
        if not self.manually_entered_tosec_aliases:
            with open('tosec_aliases.txt', 'r', encoding='utf-8') as f:
                for line in f.readlines():
                    line = line.strip().split('|')
                    if len(line)<2:
                        continue
                    self.manually_entered_tosec_aliases[line[0]]=line[1]

    def showUnscraped(self):
        print('Will show unscraped TOSEC files')
        sql = 'SELECT tosec_path FROM game_file WHERE tosec_path!="" AND format!=""'
        unscraped_paths = []
        db_paths = [x['tosec_path'] for x in self.db.execute(sql)]
        game_names = []
        for path in self.paths:
            if path not in db_paths:
                if 'ZxZvm ' in path:
                    continue
                elif 'ZZZ-UNK' in path:
                    continue
                elif path.endswith('(CSSCGC).zip'):
                    continue
                # elif 'Compilations' in path:
                #     continue
                # elif 'Games' not in path:
                #     continue
                print('Unscraped:', 'file:\\\\\\'+os.path.abspath(path))
                unscraped_paths.append(path)
                game_file = GameFile(path)
                game_name = game_file.game.getTOSECName()
                game_names.append(game_name)
        game_names = sorted(set(game_names))
        for game_name in game_names:
            print(game_name)
        print('Total:', len(self.paths), 'Unscraped files:', len(unscraped_paths),
              'Games with unscraped files:', len(game_names))
        return unscraped_paths