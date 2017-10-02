import os
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
from classes.tosec_dat import *
from classes.game import *
from classes.scraper import *

def createDATFromCSV():
    with open('tosec\\unsorted files\\ROMs\\roms.csv') as f:
        lines = f.readlines()
    dat = TOSECDat('Sinclair ZX Spectrum - Firmware - [ROM}')
    for i in range(0, len(lines), 2):
        line = lines[i].strip().split(';')
        line2 = lines[i+1].strip().split(';')
        print(line)
        print(line2)
        rom_name = line[-1]
        if rom_name.startswith('"'):
            rom_name = rom_name[1:]
        if rom_name.endswith('"'):
            rom_name = rom_name[:-1]
        rom_name = rom_name.replace (')', ' -')
        if rom_name.endswith('-'):
            rom_name = rom_name[:-1]
        rom_name = rom_name.strip()
        rom_name = rom_name.replace('SAM Coup?', 'SAM Coupe').replace('"', "'")
        rom_name = rom_name.replace('\xa0', '')
        if not rom_name:
            rom_name = line[0]
        rom_name += ' (19xx)(Sinclair Research)'
        if line[0] not in rom_name:
            rom_name += '['+line[0]+']'
        rom_name += '.rom'
        game_file = GameFile(rom_name)
        game_file.sha1 = line[2].split('\xa0')[1]
        game_file.md5 = line2[3].split('\xa0')[1]
        game_file.crc32 = line2[2].split('\xa0')[1]
        game_file.size = int(line[1])*1024
        dat.addFile(game_file)
    dat.export()

def scrapeOmegaHG():
    s = Scraper()
    url_template = 'http://zxspectrum.it.omegahg.com/'

if __name__=='__main__':
    createDATFromCSV()