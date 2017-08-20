import os
import glob
import zipfile
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

from classes.scraper import *

def scrape_chip():
    s = Scraper()
    pages = [
        'https://zxaaa.net/ZXCHIP.html',
        'https://zxaaa.net/ZXCHIP2.html'
    ]
    for page in pages:
        selector = s.loadUrl(page)
        files = selector.xpath('//a/@href').extract()
        for src in files:
            if not src.endswith('.zip'):
                continue
            dest = os.path.join('tosec', 'zxaaa', 'zxchip',src)
            src = 'https://zxaaa.net/'+src
            print(src, dest)
            if not os.path.exists(dest):
                s.downloadFile(src, dest)

def scrape_staryo():
    s = Scraper()
    pages = [
        'https://zxaaa.net/STARYO.html',
    ]
    for page in pages:
        selector = s.loadUrl(page)
        files = selector.xpath('//a/@href').extract()
        for src in files:
            if not src.endswith('.zip'):
                continue
            dest = os.path.join('tosec', 'ZXAAA Compilations', 'staryo',src)
            src = 'https://zxaaa.net/'+src
            print(src, dest)
            if not os.path.exists(dest):
                s.downloadFile(src, dest)

def scrape_system_disks():
    s = Scraper()
    pages = [
        'https://zxaaa.net/MAGICSOFTSYS.html',
    ]
    for page in pages:
        selector = s.loadUrl(page)
        files = selector.xpath('//a').extract()
        for file in files:
            src = Selector(file).xpath('//@href').extract_first()
            name = Selector(file).xpath('//img/@alt').extract_first()
            if not name:
                continue
            if not src.endswith('.zip'):
                continue
            dest = os.path.join('tosec', 'ZXAAA Compilations', 'system_disks', name+'.zip')
            src = 'https://zxaaa.net/'+src
            print(src, dest)
            if not os.path.exists(dest):
                s.downloadFile(src, dest)

def scrape_flash_games():
    s = Scraper()
    pages = [
        'https://zxaaa.net/FLASH.html',
    ]
    for page in pages:
        selector = s.loadUrl(page)
        files = selector.xpath('//a').extract()
        for file in files:
            src = Selector(file).xpath('//@href').extract_first()
            name = Selector(file).xpath('//img/@alt').extract_first()
            if not name:
                continue
            if not src.endswith('.zip'):
                continue
            dest = os.path.join('tosec', 'ZXAAA Compilations', 'flash_demos', name+'.zip')
            src = 'https://zxaaa.net/'+src
            print(src, dest)
            if not os.path.exists(dest):
                s.downloadFile(src, dest)

def scrape_disks_aaa():
    s = Scraper()
    pages = [
        'file:///C:\ZX Pokemaster\\tosec/zxaaa/DISKAAA.html',
        'file:///C:\ZX Pokemaster\\tosec/zxaaa/DISKAAA2.html',
        'file:///C:\ZX Pokemaster\\tosec/zxaaa/DISKAAA3.html',
        'file:///C:\ZX Pokemaster\\tosec/zxaaa/DISKAAA4.html',
    ]
    for page in pages:
        selector = s.loadUrl(page)
        files = selector.xpath('//a').extract()
        for file in files:
            src = Selector(file).xpath('//@href').extract_first()
            name = Selector(file).xpath('//img/@alt').extract_first()
            if not name:
                continue
            if not src.endswith('.zip'):
                continue
            dest = os.path.join('tosec','ZXAAA Compilations', 'disks_aaa', name+'.zip')
            src = 'https://zxaaa.net/'+src
            print(src, dest)
            if not os.path.exists(dest):
                s.downloadFile(src, dest)

def rename_files():
    skipped = []
    for src in glob.glob('tosec/ZXAAA Compilations/*/*.*')+glob.glob('tosec/ZXAAA Compilations/*/*/*.*'):
        if 'renamed' in src or 'skipped' in src:
            continue
        print(src)
        # continue
        filename = os.path.basename(src)
        dirname = os.path.dirname(src).split('\\')[-1]
        if 'fikus-pikus' in src:
            filenum = filename[-7:-4]
            if 'Demos' in src:
                dirname = 'Fikus Pikus Demos'
                filename = 'Fikus Pikus Demos (19xx)(Flash)(RU)(Disk {} of 140).trd'.format(str(int(filenum)))
            elif 'Games' in src:
                dirname = 'Fikus Pikus Games'
                if filename.startswith('GAME202'):
                    filename = 'Fikus Pikus Games (19xx)(Flash)(RU)(Disk 202 of 245)[{}].trd'.format(filename[7].upper())
                else:
                    filename = 'Fikus Pikus Games (19xx)(Flash)(RU)(Disk {} of 245).trd'.format(str(int(filenum)))
        elif 'disks_aaa' in src:
            dirname = 'ZX AAA Demos'
            if 'Диск новые демки сборник №' in src:
                filename = 'New Demo Disks Compilations'
                filenum = src.split('№')[-1].split('.')[0]
                filename += ' (19xx)(ZXAAA)(RU)(Disk {} of 157).trd'.format(filenum)
            elif 'Сборник демок с эффектом по бордюру' in src:
                filename = 'Collection of demos with border effect'
                filenum = src.split('№')[-1].split('.')[0]
                filename += ' (19xx)(ZXAAA)(RU)(Disk {} of 9).trd'.format(filenum)
            elif 'Сборники сборников музыки AY' in src:
                filename = 'AY Music Collections'
                filenum = src.split(' AY ')[-1].split('.')[0]
                filename += ' (19xx)(ZXAAA)(RU)(Disk {} of 8).trd'.format(filenum)
            else:
                filename = src.split('\\')[-1].split('.')[0]
                filename += ' (19xx)(ZXAAA)(RU)'
        elif 'staryo' in src:
            dirname = 'Old Demos'
            filename = 'Old Demo Disks'
            filenum = str(int(''.join([x for x in src.split('\\')[-1] if x.isdigit()])))
            filename += ' (19xx)(ZXAAA)(RU)(Disk {} of 14'.format(filenum)
        elif 'democolwa' in src:
            dirname = 'Wlodek Demos'
            if 'disk' in src:
                filenum = str(int(''.join([x for x in src.split('\\')[-1] if x.isdigit()])))
                filename = "Wlodek's Demo collection (19xx)(Wlodek)(RU)(Disk {} of 73)".format(filenum)
            else:
                filename = src.split('\\')[-1].split('.')[0]
                filename += ' (19xx)(Wlodek)(RU)'
        elif 'system_disks' in src:
            dirname = 'System Applications'
            filename = src.split('\\')[-1].split('.')[0]
            filename += ' (19xx)(Magic Soft)(RU)(en)'
        elif 'zxchip' in src:
            if 'DISKI' in src and 'musn' in src:
                dirname = 'ZX Chip Demos'
                filenum = str(int(''.join([x for x in src.split('\\')[-1] if x.isdigit()])))
                filename = 'ZX Chip Demos Collection (19xx)(Newart)(Disk {} of 228)'.format(filenum)
            elif 'GAMES' in src:
                dirname = 'ZX Chip Games'
                filenum = str(int(''.join([x for x in src.split('\\')[-1] if x.isdigit()]))+1)
                ext = os.path.splitext(src)[-1].lower()
                filename = 'ZX Chip Vologodonsk (19xx)(-)(Disk {} of 539){}'.format(filenum, ext)
            else:
                dirname = 'ZX Chip Demos'
                filename = src.split('\\')[-1].split('.')[0]
                filename += ' (19xx)(-)'
        elif 'flash_demos' in src:
            dirname = 'Flash Demos'
            filename = src.split('\\')[-1].split('.')[0]
            filename += ' (19xx)(Flash)'
        else:
            continue
        dest = os.path.join('tosec', 'ZXAAA Compilations', 'renamed', dirname, filename)
        print('dest=', dest)
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        if src.endswith('.zip'):
            with zipfile.ZipFile(src) as zf:
                if len(zf.namelist())>1:
                    print('More than 1 file in zip! Skipping.')
                    skipped.append(src)
                    continue
                for zfname in zf.namelist():
                    data = zf.read(zfname)
                    if dest[-4]!='.':
                        dest+= '.'+zfname.split('.')[-1].lower()
                    with open(dest, 'wb+') as output:
                        output.write(data)
                    break
        else:
            shutil.copy(src, dest)
    for src in skipped:
        dest = src.replace('/ZXAAA Compilations', '/ZXAAA Compilations/skipped')
        os.makedirs(os.path.dirname(dest), exist_ok=True)
        shutil.copy(src, dest)

if __name__=='__main__':
#     scrape_disks_aaa()
#     scrape_flash_demos()
#     scrape_system_disks()
#     scrape_chip()
#     scrape_staryo()
    rename_files()

