import os
import glob
import zipfile
import shutil
import re
from transliterate import translit
from functions.game_name_functions import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

from classes.scraper import *
from classes.database import *

def scrape_vtrdos():
    s = Scraper()
    pattern = 'http://vtrd.in/games.php?t='
    vars = ['full_ver', 'demo_ver', 'translat', 'remix', 'en']
    # db = Database()
    # db.loadCache()
    dest_paths = []
    for var in vars:
        url = pattern+var
        selector = s.loadUrl(url)
        games_table = selector.xpath('//table[1]//tr').extract_all()[1:-1]
        for row in games_table[1:-1]:
            src = 'tosec/unsorted files/vtrdos.ru/src/'
            dest= 'tosec/unsorted files/vtrdos.ru/dest/'
            cells = Selector(row).xpath('//td').extract_all()
            game_name = Selector(cells[0]).xpath('//a/text()').extract_first()
            game_name = game_name.encode('ISO-8859-1').decode('utf-8').strip()
            download_link = Selector(cells[0]).xpath('//a/@href').extract_first()
            game_aka = None
            game_aka = re.findall("\([^\)]*\)", game_name)
            if game_aka:
                game_name = game_name.replace(game_aka[0], '').strip()
                game_aka = translit(game_aka[0][1:-1], 'ru', reversed=True).strip()
            game_name = translit(game_name, 'ru', reversed=True)
            if var=='demo_ver':
                game_name += ' (demo)'
            publisher_and_year = Selector(cells[1]).xpath('//text()').extract_first().split("'")
            if len(publisher_and_year)!=2:
                year = None
                publisher = "'".join(publisher_and_year)
            else:
                publisher, year = publisher_and_year
            if year and year.isnumeric():
                year = int(year)
                if year>80:
                    year = 1900+year
                elif year<20:
                    year = 2000+year
                else:
                    print('Wrong year:', year)
            else:
                year = '19xx'
            publisher = publisher.encode('ISO-8859-1').decode('utf-8').strip()
            publisher = translit(publisher, 'ru', reversed=True)
            publisher = publisher.split(', ')[-1]
            publisher = publisher_regex.sub('', publisher)
            hacker = Selector(cells[2]).xpath('//text()').extract_first()
            if hacker in ['author', 'n/a', 'unknown']:
                hacker = ''
            hacker = hacker.encode('ISO-8859-1').decode('utf-8').strip()
            hacker = hacker.replace(',', ', ').replace("'", " '").replace('  ', ' ')
            dest_name = '{} ({})({})'.format(game_name, year, publisher)
            if var=='full_ver':
                dest_name += '(RU)'
            if hacker:
                dest_name += '[h '+translit(hacker, 'ru', reversed=True)+']'
            if var=='translat':
                dest_name += '[tr ru]'
            if game_aka:
                dest_name += '[aka '+game_aka+']'
            print('dest_name=', dest_name)
            src += download_link
            # if not os.path.exists(src):
            #     s.downloadFile('http://vtrd.in'+download_link, src)
            dest += getFileSystemFriendlyName(dest_name)
            dest_paths.append(dest)
            if not os.path.exists(src):
                print("Couldn't  copy ", src)
                continue
            try:
                with zipfile.ZipFile(src, 'r') as zf:
                    if len(zf.namelist())>1:
                        count = 0
                        for zfname in zf.namelist():
                            zfname_ext = zfname.split('.')[-1].lower()
                            if zfname_ext in GAME_EXTENSIONS:
                                count += 1
                        if count>1:
                            dest += '.zip'
                            shutil.copy(src, dest)
                            continue
                    for zfname in zf.namelist():
                        zfname_ext = zfname.split('.')[-1].lower()
                        if zfname_ext not in GAME_EXTENSIONS:
                            continue
                        dest += '.'+zfname_ext
                        if os.path.exists(dest):
                            continue
                        data = zf.read(zfname)
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        with open(dest, 'wb+') as output:
                            output.write(data)
            except Exception as e:
                print(src)
                print(e)
            # if os.path.exists(src) and not os.path.exists(dest):
            #     os.makedirs(os.path.dirname(dest), exist_ok=True)
            #     shutil.copy(src, dest)
            # elif not os.path.exists(src):
            #     print("Couldn't  copy ", src)
    with open('tosec/unsorted files/vtrdos.ru/destnames.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(dest_paths))

if __name__=='__main__':
    scrape_vtrdos()