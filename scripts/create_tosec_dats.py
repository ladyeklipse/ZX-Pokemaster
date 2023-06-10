import os
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

from classes.tosec_dat import *
from classes.database import *
from scripts.scrape_tipshop import createPOKTOSECDat
import shutil

def updateROMVaultDATs():
    for root, dirs, files in os.walk('tosec\\my dats\\'):
        latest_dats_dir = os.path.join(root, next(reversed(dirs)))
        break
    for root, dirs, files in os.walk(latest_dats_dir):
        for file in files:
            dat_path = os.path.join(root, file)
            dat_name = os.path.basename(dat_path)
            dir_path = '\\'.join(dat_name.split('(')[0].split(' - ')[1:]).strip()
            new_dat_path = os.path.join('tosec', 'ROMVault_V2.6.2', 'DATRoot', dir_path, dat_name)
            new_dat_dir = os.path.dirname(new_dat_path)
            if os.path.exists(new_dat_dir):
                shutil.rmtree(new_dat_dir)
            os.makedirs(new_dat_dir, exist_ok=True)
            shutil.copy(dat_path, new_dat_path)

def createTOSECDATs():
    dats_files = {}
    db = Database()
    # db.loadCache(force_reload=True)
    # games = db.getAllGames()
    kolbeck_dict = {}
    games = db.getAllGames()
    for game in games:
        if game.getYear()>'2020' and game.availability=='S':
            print("Skipping", game)
            continue
        kolbeck_dict[game.getWosID()] = []
        files = game.getFiles()
        files = sorted(files, key = lambda file:
        (not file.wos_name,
         file.tosec_path.startswith('Sinclair ZX Spectrum'),
         str(len(re.findall('\[a[0-9]{1,}\]', file.tosec_path))),
         '[a]' in file.tosec_path,
         file.wos_path,
         file.wos_name,
         file.tosec_path,
         file.getMD5()))
        for file in files:
            dat_name = file.getTOSECDatName()
            if not dats_files.get(dat_name):
                dats_files[dat_name] = []
            dats_files[dat_name].append(file)

    for dat_name, files in dats_files.items():
        dat = TOSECDat(dat_name)
        dat.files = []
        print('adding files to DAT')
        dat.addFiles(files)
        for file in files:
            if file.game.zxdb_id<9000000:
                kolbeck_dirname = dat.getBaseFileName().replace(' - ', '/')
                kolbeck_filepath = kolbeck_dirname+'/'+file.alt_dest
                kolbeck_dict[file.game.getWosID()].append(kolbeck_filepath)
        print('exporting a DAT')
        dat.export()

    with open('kolbeck.csv', 'w+', encoding='utf-8') as f:
        for game_zxdb_id in kolbeck_dict:
            for filepath in kolbeck_dict[game_zxdb_id]:
                f.write(';'.join((game_zxdb_id, filepath))+'\n')

# createTOSECDATs()
createPOKTOSECDat()
updateROMVaultDATs()