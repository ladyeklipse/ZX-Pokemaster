from classes.database import *

db = Database()
games = db.getAllGames()
inconsistencies = [[
    'TOSEC path',
    'WoS FTP path',
    'Original TOSEC game name',
    'ZXDB-based TOSEC game name',
    'ZXDB ID',
    'ZXDB release ID',
    'WoS URL'
]]
for game in games:
    for file in game.getFiles():
        if file.tosec_path and file.wos_path:
            original_tosec_game_name = GameFile(file.tosec_path).game.getTOSECName()
            current_tosec_game_name = file.release.getTOSECName()
            if original_tosec_game_name!=current_tosec_game_name:
                inconsistencies.append([
                    file.tosec_path,
                    file.wos_path,
                    original_tosec_game_name, current_tosec_game_name,
                    game.getWosID(), str(file.release_seq),
                    WOS_SITE_ROOT+'/infoseekid.cgi?id='+game.getWosID()
                ])
with open('zxdb_tosec_incosistencies.csv', 'w', encoding='utf-8') as f:
    for each in inconsistencies:
        f.write(';'.join(each)+'\n')