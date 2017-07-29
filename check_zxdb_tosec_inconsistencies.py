from classes.database import *
import os
problem = ''
db = Database()
games = db.getAllGames()
inconsistencies = [[
    'TOSEC path',
    'WoS FTP path',
    'Original TOSEC game name',
    'ZXDB-based TOSEC game name',
    'ZXDB ID',
    'ZXDB release ID',
    'Problem',
    'WoS URL'
]]
for game in games:
    for file in game.getFiles():
        if file.tosec_path and file.wos_path:
            file_from_path = GameFile(file.tosec_path)
            game_file_from_path = file_from_path
            game_from_path = game_file_from_path.game
            original_tosec_game_name = file_from_path.getTOSECName()
            # current_tosec_game_name = file.getOutputName('{GameName} ({Year})({Publisher})')
            current_tosec_game_name = file.getTOSECName()
            current_tosec_game_name_for_comparison = os.path.splitext(current_tosec_game_name)[0].replace('(demo) ', '')
            if original_tosec_game_name!=current_tosec_game_name:
                # print(original_tosec_game_name, current_tosec_game_name)
                if game_from_path.publisher!=file.release.publisher:
                    problem = 'Wrong Publisher'
                elif game_from_path.year!=file.release.year:
                    problem = 'Wrong Year'
                elif game_from_path.name not in file.release.aliases:
                    problem = 'Wrong Title'
                elif '[re-release]' in original_tosec_game_name:
                    problem = 'Removed [re-release]'
                elif file.getLanguage()!=file_from_path.getLanguage():
                    problem = 'Wrong Language'
                elif file.getMachineType()!=file_from_path.getMachineType():
                    problem = 'Wrong Machine Type'
                else:
                    problem = 'Undetermined'
            else:
                continue
        elif not file.tosec_path:
            problem = 'File not in TOSEC'
            original_tosec_game_name = ''
            # current_tosec_game_name = file.getOutputName('{GameName} ({Year})({Publisher})')
            current_tosec_game_name = file.getTOSECName()
            # current_tosec_game_name = os.path.splitext(current_tosec_game_name)[0].replace('(demo) ', '')
        # elif not file.wos_path:
        #     problem = 'File not in ZXDB'
        #     game_file_from_path = GameFile(file.tosec_path)
        #     game_from_path = game_file_from_path.game
        #     original_tosec_game_name = game_from_path.getTOSECName()
        #     current_tosec_game_name = ''
        else:
            continue
        inconsistencies.append([
            file.tosec_path,
            file.wos_path,
            original_tosec_game_name, current_tosec_game_name,
            game.getWosID(), str(file.release_seq),
            problem,
            WOS_SITE_ROOT+'/infoseekid.cgi?id='+game.getWosID(),
        ])
with open('zxdb_tosec_incosistencies.csv', 'w', encoding='utf-8') as f:
    for each in inconsistencies:
        f.write(';'.join(each)+'\n')