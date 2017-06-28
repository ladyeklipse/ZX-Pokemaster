from classes.game_file import *
from classes.game import *
from classes.database import *
import traceback

def generateTOSECPathsArray():
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
    tosec_folders = ['[TAP]', '[TRD]', '[TZX]', '[Z80]', '[SCL]', '[DSK]']
    paths = []
    for category in categories:
        for folder in tosec_folders:
            for root, dirs, files in os.walk(os.path.join('tosec', category, folder)):
                for filename in files:
                    if filename.endswith('.zip'):
                        paths.append((filename, os.path.join(root, filename)))
    paths = sorted(paths, key=lambda path: path[0])
    return [path[1] for path in paths]

def scrapeTOSEC(paths, cache=True):
    db = Database()
    if cache:
        db.loadCache()
    games_found = 0
    current_game = None
    current_tosec_name = ''
    for file_path in paths:
        print(file_path)
        if type(file_path)==str:
            game_file = getGameFileFromFilePath(file_path)
        elif type(file_path)==dict:
            game_file = getGameFileFromFilePathDict(file_path)
        new_tosec_name = game_file.game.getTOSECName()
        if current_tosec_name and current_tosec_name != new_tosec_name:
            if current_game.wos_id:
                db.addGame(current_game)
                games_found += 1
            current_game.files = []
            current_game = None
            if games_found % 100 == 0:
                db.commit()
        if not current_game:
            current_game = game_file.game
            current_tosec_name = current_game.getTOSECName()
        if not current_game.wos_id:
            game_from_db = db.getGameByFile(game_file)
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
        db.addGame(current_game)
    db.commit()


def getGameFileFromFilePath(file_path):
    game_file = GameFile(file_path)
    game_file.format = os.path.split(file_path)[0][-4:-1].lower()
    game_file.tosec_name = os.path.basename(file_path)
    game_file.getMD5(zipped=False)
    game_file.setSize(os.path.getsize(file_path), zipped=True)
    return game_file

def getGameFileFromFilePathDict(file_path):
    game_file = GameFile(file_path['path'])
    game_file.format = os.path.splitext(file_path['path'])[1][1:].lower()
    game_file.tosec_name = os.path.basename(file_path['path'])
    game_file.md5 = file_path['md5']
    game_file.setSize()

def showUnscraped(tosec_paths):
    print('Will show unscraped TOSEC files')
    db = Database()
    sql = 'SELECT tosec_name, format FROM game_file WHERE tosec_name!="" AND format!=""'
    db_tosec_files = db.execute(sql, [])
    db_paths = []
    unscraped = 0
    for file in db_tosec_files:
        path = os.path.join('['+file['format'].upper()+']', file['tosec_name'])
        db_paths.append(path)
    game_names = []
    for path in tosec_paths:
        shortened_path = os.path.split(path)
        shortened_path = os.path.join(shortened_path[0][-5:], shortened_path[1])
        if shortened_path not in db_paths:
            if 'ZxZvm ' in shortened_path:
                continue
            elif 'ZZZ-UNK' in shortened_path:
                continue
            elif shortened_path.endswith('(CSSCGC).zip'):
                continue
            print('Unscraped:', path)
            game_file = GameFile(path)
            game_name = game_file.game.getTOSECName()
            game_names.append(game_name)
            unscraped += 1
    print('Total:', len(tosec_paths), 'Unscraped:', unscraped)
    game_names = sorted(set(game_names))
    for game_name in game_names:
        print(game_name)

if __name__=='__main__':
    paths = generateTOSECPathsArray()
    # for path in paths[:10]:
    #     print(path)
    paths = [
        # "tosec\Games\[TAP]\\3D Starfighter (1988)(Codemasters).zip",
# "tosec\Games\[TZX]\\3D Starfighter (1988)(Codemasters).zip",
# "tosec\Games\[Z80]\\3D Starfighter (1988)(Codemasters).zip",
# "tosec\Games\[SCL]\\3D Starfighter (1988)(Codemasters)[h Flash][t].zip",
#         "tosec\Games\[TZX]\Indoor Soccer (1986)(Alternative Software)[re-release].zip",
# "tosec\Games\[TAP]\Indoor Soccer (1986)(Magnificent 7 Software).zip",
"tosec\Games\[TZX]\Indoor Soccer (1986)(Magnificent 7 Software).zip", #Error in ZXDB!!!
"tosec\Games\[TZX]\Falcon - The Renegade Lord (1987)(Virgin Games)[h].zip", #":" symbol!d
# "tosec\Games\[Z80]\Indoor Soccer (1986)(Magnificent 7 Software).zip",
        # "tosec\Games\[Z80]\9-Hole Golf (1986)(Galileo).zip",
        # "tosec\Covertapes\[TZX]\Ajedrez (1985)(Load 'n' Run)(es)[aka Cyrus IS Chess].zip",
        # 'tosec\Games\[TAP]\Zzzz (1986)(Mastertronic).zip',
        # 'tosec\Games\[TZX]\Zzzz (1986)(Mastertronic).zip',
        # 'tosec\Games\[Z80]\Zzzz (1986)(Mastertronic).zip',
        # 'tosec\Games\[TZX]\Zzzz (1986)(Mastertronic)[a].zip',
        # 'tosec\Games\[Z80]\Zzzz (1986)(Mastertronic)[a].zip',
        # 'tosec\Games\[TZX]\Zzzz (1986)(Zenobi Software)[re-release].zip',
        # 'tosec\Games\[Z80]\Zzzz (1986)(Zenobi Software)[re-release].zip',
        # 'tosec\Games\[DSK]\Zzzz (1986)(Zenobi Software)[re-release].zip'
        ]
    scrapeTOSEC(paths, cache=False)
    showUnscraped(paths)
    # scrapeTOSEC(paths, cache=True)
    # showUnscraped(paths)