from classes.game_file import *
from classes.game import *
from classes.database import *
import traceback

def generateTOSECPathsArray():
    tosec_folders = ['[TAP]', '[TRD]', '[TZX]', '[Z80]', '[SCL]', '[DSK]']
    paths = []
    for folder in tosec_folders:
        for root, dirs, files in os.walk(os.path.join('tosec_games', folder)):
            for filename in files:
                if filename.endswith('.zip'):
                    paths.append((filename, os.path.join('tosec_games', folder, filename)))
    paths = sorted(paths, key=lambda path: path[0])
    return [path[1] for path in paths]

def scrapeTOSEC(paths):
    db = Database()
    db.loadCache()
    games_found = 0
    current_game = None
    current_tosec_name = ''
    current_release_seq = -1
    for file_path in paths:
        game_file = GameFile(file_path)
        print(file_path)
        new_tosec_name = game_file.game.getTOSECName()
        if current_tosec_name and current_tosec_name != new_tosec_name:
            if current_game.wos_id:
                db.addGame(current_game)
                games_found += 1
            current_game.files = []
            current_game = None
            if games_found % 100 == 0:
                db.commit()
        game_file.format = os.path.split(file_path)[0][-4:-1].lower()
        game_file.tosec_name = os.path.basename(file_path)
        game_file.getMD5(zipped=False)
        game_file.setSize(os.path.getsize(file_path), zipped=True)
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

def showUnscraped(tosec_paths):
    db = Database()
    sql = 'SELECT tosec_name, format FROM game_file WHERE tosec_name!="" AND format!=""'
    db_tosec_files = db.execute(sql, [])
    db_paths = []
    unscraped = 0
    for file in db_tosec_files:
        path = os.path.join('tosec_games', '['+file['format'].upper()+']', file['tosec_name'])
        db_paths.append(path)
    game_names = []
    for path in tosec_paths:
        if path not in db_paths:
            print(path)
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
    # paths = [
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game).zip',
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game)[a].zip',
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game)[t IQ Soft].zip',
    # ]
    # paths = paths[:100]
    scrapeTOSEC(paths)
    showUnscraped(paths)