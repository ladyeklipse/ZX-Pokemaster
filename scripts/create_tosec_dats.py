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
            if '[POK]' in file:
                continue
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
    games = db.getAllGames()
    # games = db.getAllGames('game.wos_id=30508')
    for game in games:
        for file in game.getFiles():
            dat_name = file.getTOSECDatName()
            if not dats_files.get(dat_name):
                dats_files[dat_name] = []
            dats_files[dat_name].append(file)
    for dat_name, files in dats_files.items():
        dat = TOSECDat(dat_name)
        dat.files = []
        print('adding files to DAT')
        dat.addFiles(files)
        print('exporting a DAT')
        dat.export()

createTOSECDATs()
createPOKTOSECDat()
updateROMVaultDATs()