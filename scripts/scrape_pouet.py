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
month_dict = {
    'january':'01',
    'february':'02',
    'march':'03',
    'april':'04',
    'may':'05',
    'june':'06',
    'july':'07',
    'august':'08',
    'september':'09',
    'october':'10',
    'november':'11',
    'december':'12'
}

def scrape_pouet():
    s = Scraper()
    success = 0
    exceptions = []
    pattern = 'http://www.pouet.net/prodlist.php?platform%5B%5D=ZX+Spectrum&page={}'
    for i in range(1,20): #only the latest ones.
        print('page ', i)
        url = pattern.format(i)
        print(url)
        selector = s.loadUrl(url)
        rows = selector.xpath('//table[@id="pouetbox_prodlist"]//tr').extract_all()
        for row in rows[1:-1]:
            row_selector = Selector(row)
            game_name = row_selector.xpath('//td[1]//span[@class="prod"]//text()').extract_first()
            release_group = row_selector.xpath('//td[2]//a/text()').extract_first()
            release_party = row_selector.xpath('//td[3]//a/text()').extract_first()
            release_date = row_selector.xpath('//td[4]//text()').extract_first()
            if release_date:
                release_date = release_date.split(' ')
                if len(release_date)==2:
                    release_month, release_year = release_date
                    release_date = '{}-{}'.format(release_year, month_dict[release_month])
                else:
                    release_date = release_date[0]
            else:
                release_date = '19xx'
            if not release_group:
                release_group = '-'
            if release_party:
                release_party = '[{}]'.format(release_party)
            else:
                release_party = ''
            # print(game_name, release_group, release_party, release_date)
            tosec_name = getFileSystemFriendlyName(
                '{} ({})({}){}'.format(
                    game_name, release_date, release_group, release_party))
            game_page_url = row_selector.xpath('//td[1]//a/@href').extract_first()
            game_page_url = 'http://www.pouet.net/'+game_page_url
            game_page_selector = s.loadUrl(game_page_url)
            download_link = game_page_selector.xpath('//a[@id="mainDownloadLink"]/@href').extract_first()
            download_link = download_link.replace(
                '/view/',
                '/get/')
            download_link = download_link.replace(
                'https://files.scene.org/get/',
                'https://files.scene.org/get:jp-http/')
            print(tosec_name)
            print(download_link)
            ext = os.path.splitext(download_link)[1]
            if ext[1:].lower() not in GAME_EXTENSIONS+['zip', 'rar', 'gz']:
                print('wrong download link:', download_link)
            else:
                dest = 'tosec/unsorted files/pouet.net/dest/'+tosec_name+ext
                print(dest)
                if not (os.path.exists(dest) and os.path.getsize(dest)):
                    try:
                        response = s.downloadFile(download_link, dest)
                        if int(response)==200:
                            success += 1
                        else:
                            exceptions.append([game_page_url, download_link, tosec_name])
                    except Exception as e:
                        print(traceback.format_exc())
                        exceptions.append([game_page_url, download_link, tosec_name])
                else:
                    success += 1
    print('Success:', success)
    print('Fails:', len(exceptions))
    print(exceptions)



def rename():
    files_extracted = []
    for root, dirs, files in os.walk('tosec\\unsorted files\\pouet.net\\sortedbytype'):
        for src_file in files:
            src = os.path.join(root,  src_file)
            print(src)
            game_file = GameFile(src)
            tosec_name = game_file.getTOSECName()
            dest = os.path.join(
                'tosec\\unsorted files\\pouet.net\\unpacked', game_file.getType(), tosec_name)
            ext = os.path.splitext(src)[-1]
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if ext == '.bak':
                continue
            if ext == '.zip':
                with zipfile.ZipFile(src, 'r') as zf:
                    files_to_extract = []
                    conflict = False
                    for zfname in zf.namelist():
                        zfname_ext = zfname.split('.')[-1].lower()
                        if zfname_ext in GAME_EXTENSIONS:
                            files_to_extract.append(zfname)
                    for each in GAME_EXTENSIONS:
                        if len([x for x in files_to_extract if x.endswith(each)]) > 1:
                            print('Conflict:', tosec_name, src, files_to_extract)
                            conflict = True
                            break
                    if not conflict and files_to_extract:
                        for file in files_to_extract:
                            data = zf.read(files_to_extract[0])
                            ext = os.path.splitext(files_to_extract[0])[-1].lower()
                            dest = dest.replace('.zip', ext)
                            with open(dest, 'wb+') as output:
                                output.write(data)
                        files_extracted.append(src)
                    if conflict:
                        dest = src.replace('sortedbytype', 'conflicts')
                        os.makedirs(os.path.dirname(dest), exist_ok=True)
                        shutil.copy(src, dest)
            else:
                shutil.copy(src, dest)

if __name__=='__main__':
    scrape_pouet()
    rename()
    #After renaming should automate copying to