import os
import glob
import zipfile
import shutil
import re
from html.parser import HTMLParser
from transliterate import translit
from functions.game_name_functions import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')

from classes.scraper import *
from classes.database import *
h = HTMLParser()

def get_magazines_countries():
    pattern = 'http://zxpress.ru/ezines.php'
    s = Scraper()
    selector = s.loadUrl(pattern)
    rows = selector.xpath('//tr').extract_all()
    mag_countries = {}
    mag_cities = {}
    for row in rows:
        row_selector = Selector(row)
        mag_name = row_selector.xpath('//td/a/b/text()').extract_first()
        mag_country_image = row_selector.xpath('//td/img/@src').extract_first()
        mag_city = row_selector.xpath('//td[3]/text()').extract_first()
        if not mag_name or not mag_country_image:
            continue
        if mag_name in ['city']:
            continue
        if '1.png' in mag_country_image:
            mag_country = 'RU'
        if '2.png' in mag_country_image:
            mag_country = 'BY'
        if '3.png' in mag_country_image:
            mag_country = 'UA'
        mag_name = translit(mag_name, 'ru', reversed=True).lower()
        if mag_city:
            mag_cities[mag_name] = translit(mag_city.strip(), 'ru', reversed=True)
        print(mag_name, mag_country, mag_city)
        mag_countries[mag_name] = mag_country
    for root, dirs, files in os.walk('tosec/unsorted files/vtrdos.ru/press/dest_reviewed'):
        for file in files:
            for key in mag_countries:
                if file.lower().startswith(key):
                    dest_file = file.replace('(RU)', '({})[{}]'.format(mag_countries[key], mag_cities[key]))
                    src = os.path.join(root, file)
                    dest = os.path.join(root, 'renamed', dest_file)
                    print(src, dest)
                    if os.path.exists(src):
                        shutil.move(src, dest)
        break

def get_magazines_dates():
    pattern = 'http://zxpress.ru/chronology.php'
    s = Scraper()
    selector = s.loadUrl(pattern)
    rows = selector.xpath('//tr').extract_all()
    year = 2018
    ru_months = {
        'января':'1',
        'февраля':'2',
        'марта':'3',
        'апреля':'4',
        'мая':'5',
        'июня':'6',
        'июля':'7',
        'августа':'8',
        'сентября':'9',
        'октября':'10',
        'ноября':'11',
        'декабря':'12'
    }
    mag_dates = {}
    for row in rows:
        # print(date)
        date_selector = Selector(row)
        cells = date_selector.xpath('//text()').extract_all()[1:]
        cells = [cell.strip() for cell in cells if cell.strip()]
        if len(cells)==1:
            year = cells[0][:4]
            print(year)
        elif len(cells)==2:
            day, ru_month = cells[0].replace('  ', ' ').split(' ')
            month = ru_months[ru_month].zfill(2)
            day = day.zfill(2)
            date = '{}-{}-{}'.format(year, month, day)
            mag_name = cells[1].replace('#', '')
            mag_dates[mag_name] = date
            # print(date, mag_name)
    for root, dirs, files in os.walk('tosec/unsorted files/vtrdos.ru/press/dest_reviewed'):
        for file in files:
            for key in mag_dates:
                if file.replace('#', '').startswith(key):
                    dest_file = file.replace('19xx', mag_dates[key])
                    src = os.path.join(root, file)
                    dest = os.path.join(root, 'renamed', dest_file)
                    print(src, dest)
                    if os.path.exists(src):
                        shutil.move(src, dest)
        break


def scrape_demos():
    pattern = 'http://vtrd.in/'
    vars = ['russian.php', 'other.php']
    scrape_vtrdos(pattern, vars, 'demos')


def scrape_demos_comps():
    s = Scraper()
    pattern = 'http://vtrd.in/demo.php?party='
    vars = range(1, 200)
    src = 'tosec/unsorted files/vtrdos.ru/demos_comps/src/'
    dest = 'tosec/unsorted files/vtrdos.ru/demos_comps/dest/'
    for var in vars:
        selector = s.loadUrl(pattern+str(var))
        all_works_link = selector.xpath('//tr/td/div/b/a').extract_first()
        if not all_works_link:
            continue
        aw_selector = Selector(all_works_link)
        download_link = aw_selector.xpath('//@href').extract_first().replace('../','')
        filename = aw_selector.xpath('//text()').extract_first()
        if not filename:
            continue
        dest_name = filename.replace('. All Works', '').replace('. All ZX Works', '').strip()
        date = selector.xpath('//td/div/font/text()').extract_first().split('//')[-1].split('.')
        date = '-'.join([x.strip() for x in reversed(date)])
        dest_name += ' ({})(vtrdos.ru)(RU)'.format(date)
        print(download_link, dest_name)
        download_and_unpack(s, download_link, src, dest, dest_name)

def scrape_press():
    s = Scraper()
    pattern = 'http://vtrd.in/press.php?l='
    vars = ['1', '2']
    src = 'tosec/unsorted files/vtrdos.ru/press/src/'
    dest = 'tosec/unsorted files/vtrdos.ru/press/dest/'
    for var in vars:
        selector = s.loadUrl(pattern+var)
        magazines = selector.xpath('//tr').extract_all()
        for magazine in magazines:
            m_selector = Selector(magazine)
            magazine_name = m_selector.xpath('//td//b/text()').extract_first()
            issues = m_selector.xpath('//a').extract_all()
            for issue in issues:
                i_selector = Selector(issue)
                issue_num = i_selector.xpath('//text()').extract_first()
                download_link = i_selector.xpath('//@href').extract_first()
                dest_name = "{} - Issue {} (19xx)(vtrdos.ru)(RU)".format(magazine_name, issue_num)
                print(download_link, dest_name)
                download_and_unpack(s, download_link, src, dest, dest_name)

def scrape_gs():
    s = Scraper()
    pattern = 'http://vtrd.in/gs.php'
    selector = s.loadUrl(pattern)
    src = 'tosec/unsorted files/vtrdos.ru/gs/src/'
    dest = 'tosec/unsorted files/vtrdos.ru/gs/dest_players/'
    players = selector.xpath('//table[2]//tr//a').extract_all()
    # print(players)
    for link in players:
        link = h.unescape(link.decode('utf-8'))
        link = link.encode('ISO-8859-1').decode('utf-8')
        link_sel = Selector(link)
        download_link = link_sel.xpath('//a/@href').extract_first()
        if not download_link:
            continue
        # print(link)
        desc = ' '.join(link_sel.xpath('//text()').extract_all())
        dest_name = translit(desc, 'ru', reversed=True)
        # print('!', download_link, desc)
        # download_and_unpack(s, download_link, src, dest, dest_name)
    dest = 'tosec/unsorted files/vtrdos.ru/gs/dest_games/'
    games = selector.xpath('//tr[@bgcolor="#787878" or @bgcolor="#999999"]').extract_all()
    print(games)
    for row in games:
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
        publisher_and_year = Selector(cells[1]).xpath('//text()').extract_first().split("'")
        if len(publisher_and_year) != 2:
            year = None
            publisher = "'".join(publisher_and_year)
        else:
            publisher, year = publisher_and_year
        if year and year.isnumeric():
            year = int(year)
            if year > 80:
                year = 1900 + year
            elif year < 20:
                year = 2000 + year
            else:
                print('Wrong year:', year)
        else:
            year = '19xx'
        publisher = publisher.encode('ISO-8859-1').decode('utf-8').strip()
        publisher = translit(publisher, 'ru', reversed=True)
        publisher = publisher.split(', ')[-1]
        publisher = publisher_regex.sub('', publisher)
        publisher = publisher.replace(',', ' - ')
        hacker = Selector(cells[2]).xpath('//text()').extract_first()
        if hacker in ['author', 'n/a', 'unknown']:
            hacker = ''
        hacker = hacker.encode('ISO-8859-1').decode('utf-8').strip()
        hacker = hacker.replace(',', ', ').replace("'", " '").replace('  ', ' ')
        dest_name = '{} ({})({})'.format(game_name, year, publisher)
        if hacker:
            dest_name += '[h ' + translit(hacker, 'ru', reversed=True) + ']'
        if game_aka:
            dest_name += '[aka ' + game_aka + ']'
        dest_name += '[GS]'
        print(download_link, 'dest_name=', dest_name)
        download_and_unpack(s, download_link, src, dest, dest_name)


def scrape_sbor():
    s = Scraper()
    pattern = 'http://vtrd.in/sbor.php'
    selector = s.loadUrl(pattern)
    uls = selector.xpath('//ul').extract_all()
    cats = selector.xpath('//p/b/font/text()').extract_all()[1:]
    cats = [translit(cat.encode('ISO-8859-1').decode('utf-8'), 'ru', reversed=True)[:-1] for cat in cats]
    print(cats)
    for i, ul in enumerate(uls):
        ul_selector = Selector(ul)
        links = ul_selector.xpath('//li').extract_all()
        for link in links:
            src = 'tosec/unsorted files/vtrdos.ru/sbor/src/'
            cat = cats[i]
            cat = getFileSystemFriendlyName(cat)[:20]
            dest = 'tosec/unsorted files/vtrdos.ru/sbor/dest/'+cats[i].zfill(2)+'/'
            link = h.unescape(link.decode('utf-8'))
            link = link.encode('ISO-8859-1').decode('utf-8')
            link_sel = Selector(link)
            download_link = link_sel.xpath('//a/@href').extract_first()
            if not download_link:
                continue
            print(link)
            desc = ' '.join(link_sel.xpath('//text()').extract_all())
            dest_name = translit(desc, 'ru', reversed=True)
            print(download_link, dest_name)
            download_and_unpack(s, download_link, src, dest, dest_name)

def scrape_system():
    s = Scraper()
    pattern = 'http://vtrd.in/system.php'
    selector = s.loadUrl(pattern)
    links = selector.xpath('//font[@size="2"]//a').extract_all()
    for link in links:
        src = 'tosec/unsorted files/vtrdos.ru/system/src/'
        dest = 'tosec/unsorted files/vtrdos.ru/system/dest/'
        link = h.unescape(link.decode('utf-8'))
        link = link.encode('ISO-8859-1').decode('utf-8')
        link_sel = Selector('<p>'+link+'</p>')
        download_link = link_sel.xpath('//a/@href').extract_first()
        if not download_link:
            continue
        print(link)
        desc = link_sel.xpath('//text()').extract_all()
        prog_name = desc[0]
        prog_publisher = desc[1] if len(desc)>1 else '-'
        prog_publisher = prog_publisher.replace('by ', '').strip().split(',')
        first_prog_publisher = prog_publisher[0].split("'")
        if len(prog_publisher)>1:
            hacker = prog_publisher[1].strip()
            hacker = publisher_regex.sub('', hacker)
        else:
            hacker = ''
        publisher = first_prog_publisher[0].strip()
        publisher = publisher_regex.sub('', publisher).strip()
        if len(first_prog_publisher)>1 and first_prog_publisher[-1].isdigit():
            year = first_prog_publisher[-1].strip()
            year = '19'+year if int(year)>60 else '20'+year
        else:
            year = '19xx'
        dest_name = '{} ({})({})'.format(prog_name, year, publisher)
        if hacker:
            dest_name += '[h {}]'.format(hacker)
        dest_name = translit(dest_name, 'ru', reversed=True)
        print(download_link, dest_name)
        download_and_unpack(s, download_link, src, dest, dest_name)

def scrape_games():
    pattern = 'http://vtrd.in/games.php?t='
    vars = ['full_ver', 'demo_ver', 'translat', 'remix', 'en']
    scrape_vtrdos(pattern, vars)

def scrape_vtrdos(pattern, vars, name=""):
    s = Scraper()
    db = Database()
    # db.loadCache()
    dest_paths = []
    for var in vars:
        url = pattern+var
        selector = s.loadUrl(url)
        games_table = selector.xpath('//table[1]//tr').extract_all()[1:-1]
        for row in games_table[1:-1]:
            src = 'tosec/unsorted files/vtrdos.ru/{}/src/'.format(name)
            dest= 'tosec/unsorted files/vtrdos.ru/{}/dest/'.format(name)
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
            if len(cells)>2:
                hacker = Selector(cells[2]).xpath('//text()').extract_first()
                if hacker in ['author', 'n/a', 'unknown']:
                    hacker = ''
                hacker = hacker.encode('ISO-8859-1').decode('utf-8').strip()
                hacker = hacker.replace(',', ', ').replace("'", " '").replace('  ', ' ')
            else:
                hacker = ''
            dest_name = '{} ({})({})'.format(game_name, year, publisher)
            if var=='full_ver' or 'rus' in var:
                dest_name += '(RU)'
            if hacker:
                dest_name += '[h '+translit(hacker, 'ru', reversed=True)+']'
            if var=='translat':
                dest_name += '[tr ru]'
            if game_aka:
                dest_name += '[aka '+game_aka+']'
            print('dest_name=', dest_name)
            dest_paths.append(dest)
            download_and_unpack(s, download_link, src, dest, dest_name)
    with open('tosec/unsorted files/vtrdos.ru/destnames.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(dest_paths))

def download_and_unpack(s, download_link, src, dest, dest_name):
    src += download_link
    if not os.path.exists(src):
        s.downloadFile('http://vtrd.in/'+download_link, src)
    dest += getFileSystemFriendlyName(dest_name)
    if not os.path.exists(src):
        print("Couldn't  copy ", src)
        return
    try:
        with zipfile.ZipFile(src, 'r') as zf:
            if len(zf.namelist())>1:
                count = 0
                for zfname in zf.namelist():
                    zfname_ext = zfname.split('.')[-1].lower()
                    if zfname_ext in GAME_EXTENSIONS:
                        count += 1
                if count>1:
                    # dest += '.zip'
                    os.makedirs(dest, exist_ok=True)
                    zf.extractall(dest)
                    # shutil.copy(src, dest)
                    return
            for zfname in zf.namelist():
                zfname_ext = zfname.split('.')[-1].lower()
                if zfname_ext not in GAME_EXTENSIONS:
                    return
                dest += '.'+zfname_ext
                if os.path.exists(dest):
                    return
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



if __name__=='__main__':
    # get_magazines_dates()
    get_magazines_countries()
    # scrape_demos()
    # scrape_demos_comps()
    # scrape_press()
    # scrape_gs()
    # scrape_sbor()
    # scrape_vtrdos()
    # scrape_system()