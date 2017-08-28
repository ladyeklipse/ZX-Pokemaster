import os
import glob
import shutil
import zipfile
from functions.game_name_functions import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

from classes.scraper import *

def scrape_csscgc():
    # if os.path.exists('tosec\\CSSCGC Games'):
    #     shutil.rmtree('tosec\\CSSCGC Games')
    s = Scraper()
    template = 'https://www.yoursinclair.co.uk/csscgc/csscgc.cgi?year='
    for year in range(1996, 2017):
        files_extracted = []
        page = template + str(year)
        selector = s.loadUrl(page)
        games_tables = selector.xpath('//table[@border="1"]').extract_all()
        for game_table in games_tables:
            cells = Selector(game_table).xpath('//td//text()').extract_all()
            game_name = cells[0]
            author = cells[2]
            if not author.startswith('Mr'):
                author = putInitialsToEnd(author)
            filenames = list(set(cells[4].split(' ')+[cells[4]]))
            format = cells[10]
            game_represented = False
            for filename in filenames:
                if not filename:
                    continue
                filename = os.path.basename(filename)
                ext = os.path.splitext(filename)[-1].lower()
                tosec_name = '{} ({})({})({})[CSSCGC]{}'.format(game_name, str(year), author, format, ext)
                tosec_name = tosec_name.replace('(Spectrum)', '').replace('ZX Spectrum ', '').replace('(48K)', '')
                tosec_name = tosec_name.replace('(128K Spectrum)', '(128K)')
                tosec_name = tosec_name.replace('(128K-+2)', '(+2)')
                tosec_name =tosec_name.replace('(unknown)', '(-)')
                tosec_name = getFileSystemFriendlyName(tosec_name)
                src = os.path.join('tosec', 'csscgc scrape', 'CSSCGC' + str(year), filename)
                dest = os.path.join('tosec', 'CSSCGC Games', str(year), tosec_name)
                # print(src, dest)
                if not os.path.exists(src):
                    # print('File does not exist:', filename, 'Year:', year)
                    continue
                if os.path.exists(dest):
                    print('Conflict:', tosec_name, filename, 'Year:', year)
                    continue
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                if ext == '.zip':
                    with zipfile.ZipFile(src, 'r') as zf:
                        files_to_extract = []
                        conflict = False
                        for zfname in zf.namelist():
                            zfname_ext = zfname.split('.')[-1].lower()
                            if zfname_ext in GAME_EXTENSIONS:
                                files_to_extract.append(zfname)
                        for each in GAME_EXTENSIONS:
                            if len([x for x in files_to_extract if x.endswith(each)])>1:
                                print('Conflict:', tosec_name, src, files_to_extract, 'Year:', year)
                                conflict = True
                                break
                        if not conflict and files_to_extract:
                            for file in files_to_extract:
                                data = zf.read(files_to_extract[0])
                                ext = os.path.splitext(files_to_extract[0])[-1].lower()
                                dest = dest.replace('.zip', ext)
                                with open(dest, 'wb+') as output:
                                    output.write(data)
                                    game_represented = True
                            files_extracted.append(src)
                else:
                    shutil.copy(src, dest)
                    files_extracted.append(src)
                    game_represented = True
            if not game_represented:
                print('Game not represented:', tosec_name, cells[4], 'Year:', year)
        for src in glob.glob(os.path.join('tosec', 'csscgc scrape', 'CSSCGC'+str(year), '*')):
            filename, ext = os.path.splitext(os.path.basename(src))
            if ext[1:] not in GAME_EXTENSIONS+['zip']:
                continue
            if src in files_extracted:
                continue
            else:
                tosec_name = '{} ({})(-)[CSSCGC]{}'.format(filename.title() , str(year), ext)
                dest = os.path.join('tosec', 'CSSCGC Games', str(year), 'unsorted', tosec_name)
                os.makedirs(os.path.dirname(dest), exist_ok=True)
                shutil.copy(src, dest)
                print('Copied: ', src, 'to:', dest, 'Year:', year)

if __name__=='__main__':
    scrape_csscgc()