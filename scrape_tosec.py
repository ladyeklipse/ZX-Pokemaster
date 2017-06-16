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
    # tosec_folders = ['[TAP]', '[TRD]', '[TZX]', '[Z80]', '[SCL]', '[DSK]']
    games_found = 0
    # games_not_found = 0
    current_game = None
    current_tosec_name = ''
    # for folder in tosec_folders:
    #     for root, dirs, files in os.walk(os.path.join('tosec_games', folder)):
    #         for filename in files:
    #             if not filename.endswith('.zip'):
    #                 continue
                # file_path = os.path.join('tosec_games', folder, filename)
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
        game_from_db = db.getGameByFile(game_file)
        if game_from_db and current_game!=game_from_db:
            game_from_db.addFiles(current_game.files)
            current_game = game_from_db
        current_game.addFile(game_file)
    db.addGame(current_game)
    db.commit()

if __name__=='__main__':
    paths = generateTOSECPathsArray()
    # paths = [
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game).zip',
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game)[a].zip',
    #     'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game)[t IQ Soft].zip',
    # ]
    scrapeTOSEC(paths)