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
                    paths.append(os.path.join('tosec_games', folder, filename))
    return paths

def scrapeTOSEC(paths):
    db = Database()
    games_found = 0
    current_game = None
    current_tosec_name = ''
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
        if not current_game:
            current_game = game_file.game
            current_tosec_name = current_game.getTOSECName()
        if not current_game.wos_id:
            game_from_db = db.getGameByFile(game_file)
            if game_from_db and current_game!=game_from_db:
                game_from_db.addFiles(current_game.files)
                current_game = game_from_db
        current_game.addFile(game_file)
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
    for path in tosec_paths:
        if path not in db_paths:
            print(path)
            unscraped += 1
    print('Total:', len(tosec_paths), 'Unscraped:', unscraped)

if __name__=='__main__':
    paths = generateTOSECPathsArray()
    # paths = [
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game).zip',
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game)[a].zip',
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game)[t IQ Soft].zip',
    # ]
    scrapeTOSEC(paths[:100])
    # showUnscraped(paths)