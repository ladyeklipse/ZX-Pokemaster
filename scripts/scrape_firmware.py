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
        rom_publisher = line[-1]
        if rom_publisher.startswith('"'):
            rom_publisher = rom_publisher[1:]
        if rom_publisher.endswith('"'):
            rom_publisher = rom_publisher[:-1]
        rom_publisher = rom_publisher.replace (')', ' -')
        if rom_publisher.endswith('-'):
            rom_publisher = rom_publisher[:-1]
        rom_publisher = rom_publisher.strip()
        rom_publisher = rom_publisher.replace('SAM Coup?', 'SAM Coupe').replace('"', "'")
        rom_publisher = rom_publisher.replace('\xa0', '')
        if not rom_publisher:
            rom_publisher = line[0]
        rom_publisher += ' (19xx)(Sinclair Research)'
        if line[0] not in rom_publisher:
            rom_publisher += '['+line[0]+']'
        rom_publisher += '.rom'
        game_file = GameFile(rom_publisher)
        game_file.sha1 = line[2].split('\xa0')[1]
        game_file.md5 = line2[3].split('\xa0')[1]
        game_file.crc32 = line2[2].split('\xa0')[1]
        game_file.size = int(line[1])*1024
        dat.addFile(game_file)
    dat.export()

def scrapeOmegaHG():
    s = Scraper()
    url_root= 'http://zxspectrum.it.omegahg.com/'
    homepage_selector = s.loadUrl(url_root)
    links_table = homepage_selector.xpath('//table//table//tr//a').extract_all()
    csv = open('tosec\\unsorted files\\roms\\omegahg.csv', 'w+')
    for link in links_table[2:-2]:
        # print(link)
        link_sel = Selector(link)
        publisher = link_sel.xpath('//text()').extract_first()
        publisher = ' '.join([x.strip() for x in publisher.split(' ') if x.strip()])
        country = 'GB'
        if 'Sinclair' in publisher:
            publisher = 'Sinclair'
        if 'Timex' in publisher:
            country = 'US'
        if 'Russian' in publisher or 'Pentagon' in publisher or 'Scorpion' in publisher:
            country = 'RU'
        if 'Sintez' in publisher:
            country = 'MD'
        if 'Brest' in publisher:
            country = 'BY'
        if 'Didaktik' in publisher:
            country = 'CZ'
        publisher = publisher.replace('/', ' - ')
        url = link_sel.xpath('//@href').extract_first()
        print(publisher, url)
        url = url_root+url
        roms_page_selector = s.loadUrl(url)
        csv.write(url+'\n')
        roms_links = roms_page_selector.xpath('//table//tr').extract_all()
        for link in roms_links:
            rom_publisher = publisher
            link = Selector(link)
            rom_name = link.xpath('//h3//text()').extract_first()
            if not rom_name:
                print('no rom name')
                continue
            rom_name = rom_name.replace('\t', ' ').replace('\n', ' ') \
                .replace('v.', 'v').replace('V.', 'v').replace('V ', 'v') \
                .replace('V4', 'v4').replace('V1', 'v1').replace('V2', 'v2') \
                .replace('V3', 'v3').replace('V5', 'v5')
            rom_country = country
            if 'French' in rom_name:
                rom_country = 'FR'
                rom_name = rom_name.replace('French', '')
            if 'Spanish' in rom_name:
                rom_country = 'ES'
                rom_name = rom_name.replace('Spanish', '')
            if 'Arabic' in rom_name:
                rom_country = 'ar'
                rom_name = rom_name.replace('Arabic', '')
            if 'Andrew Owen' in rom_name:
                rom_publisher = 'Owen, Andrew'
                rom_name = rom_name.replace('Andrew Owen', '')
            rom_name = ' '.join([x.strip() for x in rom_name.split(' ') if x.strip()])
            rom_urls = link.xpath('//a').extract_all()
            if 'Custom-made Russian' in publisher:
                rom_publisher = '-'
                rom_name = '{} (19xx)({})(RU)[Custom-made]'.format(rom_name, rom_publisher)
            elif 'Custom-made' in publisher:
                rom_publisher = '-'
                rom_name = '{} (19xx)({})[Custom-made]'.format(rom_name, rom_publisher)
            elif 'Cartridge' in publisher:
                rom_publisher = '-'
                rom_name = 'Cartridges\\{} (19xx)({})[Cartridge]'.format(rom_name, rom_publisher)
            else:
                rom_name = '{} (19xx)({})'.format(rom_name, rom_publisher)
            rom_name = getFileSystemFriendlyName(rom_name)
            if rom_country != 'GB':
                if rom_country not in rom_name:
                    rom_name += '(' + rom_country + ')'
            for rom_url in rom_urls:
                rom_url = Selector(rom_url)
                url = rom_url.xpath('//@href').extract_first()
                if not url or not url.lower().endswith('rom'):
                    continue
                img = rom_url.xpath('//img//@src').extract_first()
                img = '' if not img else img.replace('images/1/', '').replace('_', '-').split('.')[0]
                print(url, img)
                src = url_root+url
                dest_dir = os.path.join('tosec', 'unsorted files', 'roms', 'omegahg')
                os.makedirs(dest_dir, exist_ok=True)
                dest_rom_name = rom_name
                if img:
                    img = img.split('-')
                    # if img[1]!=img[2] and img[2]!='17':
                    if int(img[2])-int(img[1])+int(img[0])!=0 and img[2]!='17':
                        dest_rom_name += '[{}K-{}K of {}K]'.format(img[0], img[1], img[2])
                dest_rom_name += '.rom'
                dest = os.path.join(dest_dir, dest_rom_name)
                print(dest)
                csv.write(os.path.basename(dest)+'\n')
                s.downloadFile(src, dest)
    csv.close()

if __name__=='__main__':
    scrapeOmegaHG()
    # createDATFromCSV()