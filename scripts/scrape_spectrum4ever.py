import os
import glob
import zipfile
import shutil
from transliterate import translit
from functions.game_name_functions import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

from classes.scraper import *
from classes.database import *

mod_flags_dict = {
    # 'DISTRIBUTED BY':'h',
    # 'DISKED BY':'h',
    # 'BROKEN BY':'h',
    'бессмертие':'[t]',
    'неубиваемость':'[t]',
    'poke':'[t]',
    'infinity':'[t]',
    'translate':'[tr ru]',
    'russian':'[tr ru]',
    'украинский':'[tr ua]',
}

def scrape_spectrum4ever():
    s = Scraper()
    pattern = 'http://spectrum4ever.org/fulltape.php?go=releases&scr=1&letter='
    letters = ['0-9']+list('ABCDEFGHIJKLMNOPQRSTUVWXYZ')
    mod_flags = []
    db = Database()
    db.loadCache()
    noted_games = 0
    unsorted_games = 0
    total_games = 0
    for letter in letters:
        url = pattern+letter
        print(url)
        selector = s.loadUrl(url)
        games = selector.xpath('//table[2]//tr').extract_all()[2:-1]
        for game in games:
            src = 'tosec/spectrum4ever.org/src/'
            dest = 'tosec/spectrum4ever.org/dest/'
            data = Selector(game)
            game_name = data.xpath('//a[@class="yel"]/text()').extract_first()
            if not game_name:
                continue
            src += getFileSystemFriendlyName(game_name).upper()
            game_name = translit(getFileSystemFriendlyName(game_name.title()), 'ru', reversed=True)
            format = data.xpath('//td[@class="cian"]/text()').extract_first()
            game_file = GameFile(game_name+'.'+format)
            game = db.getGameByName(game_name)
            if game:
                print('Game found:', game)
                game_file.game = game
                game_file.release = game.releases[0]
            else:
                print('Game not found.')
                dest += 'unsorted/'
                unsorted_games += 1
            hacker_name = data.xpath('//a[@class="grey"]/text()').extract_first()
            if hacker_name:
                hacker_name = translit(hacker_name.title().replace("'", ''), 'ru', reversed=True)
                hacker_name = getFileSystemFriendlyName(hacker_name)
                src += ' ('+hacker_name.upper()+')'
                game_file.mod_flags += '[h '+hacker_name+']'
            else:
                src += ' (-)'
            src += '.'+format
            notes = data.xpath('//td[@class="red"]/text()').extract_first()
            if notes:
                notes = translit(notes.title(), 'ru', reversed=True).split(' + ')
                for note in notes:
                    note  = note.strip()
                    if not note:
                        continue
                    mod_flags.append(note)
                    for key in mod_flags_dict:
                        if note.startswith(key):
                            game_file.mod_flags += mod_flags_dict[key]
                            continue
                    if '128K' in note:
                        game_file.setMachineType('128K')
                        continue
                    if 'part' in note.lower():
                        game_file.setPart(note)
                        continue
                    if not hacker_name:
                        note = getFileSystemFriendlyName(translit(note, 'ru', reversed=True))
                        game_file.notes += '[h '+note+']'
                        dest += 'noted/'
                        noted_games += 1
            is_rus = data.xpath('//td[@class="magn"]/text()').extract_first() == 'RUS'
            if is_rus:
                if '[tr ru' not in game_file.mod_flags:
                    game_file.mod_flags += '[tr ru]'
            print(game_name, hacker_name, notes, is_rus)
            print('src=',src)
            dest += game_file.getTOSECName()
            print('dest=', dest)
            total_games += 1
            if not os.path.exists(src):
                download_link = data.xpath('//td[@class="yel"]/a/@href').extract_first()
                download_link = 'http://spectrum4ever.org/'+download_link
                s.downloadFile(download_link, src)
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copy(src, dest)
    print(sorted(list(set(mod_flags))))
    print(len(mod_flags))
    print('Noted:', noted_games)
    print('Unsorted:', unsorted_games)
    print('Total games:', total_games)


if __name__=='__main__':
    scrape_spectrum4ever()