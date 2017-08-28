import os
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
try:
    f = open('zxdb_tosec_incosistencies.csv', 'w', encoding='utf-8')
except IOError as e:
    print('File is opened in excel')
    raise e
from classes.database import *
db = Database()
games = db.getAllGames()
inconsistencies_header = [
    'TOSEC path',
    'WoS FTP path',
    'WoS FTP name',
    'Original TOSEC game name',
    'ZXDB-based TOSEC game name',
    'TOSEC DAT file',
    'ZXDB ID',
    'ZXDB release ID',
    'Problems',
    'ZXDB Frontend URL'
]
inconsistencies = []
undetermined_problems = 0
for game in games:
    for file in game.getFiles():
        problems = []
        if file.tosec_path and file.wos_path:
            file_from_path = GameFile(file.tosec_path)
            game_file_from_path = file_from_path
            game_from_path = game_file_from_path.game
            original_tosec_game_name = file_from_path.getTOSECName()
            current_tosec_game_name = file.getTOSECName()
            if original_tosec_game_name!=current_tosec_game_name:
                if game_from_path.publisher!=file.release.publisher:
                    problems.append('Wrong Publisher')
                if game_from_path.year!=file.release.year:
                    problems.append('Wrong Year')
                if '[re-release]' in original_tosec_game_name:
                    problems.append('Removed [re-release]')
                if '[re-release]' in current_tosec_game_name:
                    problems.append('Added [re-release]')
                if '[aka' in original_tosec_game_name:
                    problems.append('Removed [aka ...] alias')
                if '[aka' in current_tosec_game_name:
                    problems.append('Added [aka ...] alias')
                if file.getLanguage()!=file_from_path.getLanguage():
                    problems.append('Wrong Language')
                if file.getMachineType()!=file_from_path.getMachineType():
                    problems.append('Wrong Machine Type')
                if file.getPart()!=file_from_path.getPart():
                    problems.append('Wrong Part')
                if file.getSide()!=file_from_path.getSide():
                    problems.append('Wrong Side')
                if file.is_demo != file_from_path.is_demo:
                    if file.is_demo:
                        problems.append('Marked as (demo)')
                    else:
                        problems.append('Unmarked as (demo)')
                if file_from_path.getGameName()!=file.getGameName():
                    if game_from_path.name not in file.release.aliases:
                        problems.append('Game Title not in ZXDB')
                    else:
                        problems.append('Picked default Game Title')
                if not problems:
                    problems.append('Undetermined')
                    undetermined_problems += 1
            else:
                continue
        elif not file.tosec_path:
            problems.append('File not in TOSEC')
            original_tosec_game_name = ''
            current_tosec_game_name = file.getTOSECName()
        elif not file.wos_path:
            problems.append('File not in ZXDB')
            file_from_path = GameFile(file.tosec_path)
            original_tosec_game_name = file_from_path.getTOSECName()
            current_tosec_game_name = file.getTOSECName()
        else:
            continue
        if not problems:
            problems = ['Undetermined']
            undetermined_problems += 1
        inconsistencies.append([
            file.tosec_path,
            file.wos_path,
            file.wos_name,
            original_tosec_game_name,
            current_tosec_game_name,
            file.getTOSECDatName(),
            game.getWosID(),
            str(file.release_seq),
            ', '.join(sorted(set(problems))),
            'http://spectrumcomputing.co.uk/index.php?cat=96&id='+game.getWosID(),
        ])
print('Undetermined problems:', undetermined_problems)
inconsistencies = sorted(inconsistencies, key=lambda x: x[-2])
with f:
    f.write(';'.join(inconsistencies_header)+'\n')
    for each in inconsistencies:
        f.write(';'.join([x if x else 'N/A' for x in each])+'\n')
os.startfile('zxdb_tosec_incosistencies.csv')