from classes.cheat import *
from classes.poke import *
from settings import *
import os
import glob
import re

publisher_regex = re.compile('inc[ .]|ltd|plc|S\.A\.', re.IGNORECASE)
filepath_regex = re.compile('\*|\?|\:|\||\\|/|\"|<|>|\"')
remove_square_brackets_regex = re.compile('\[[^\]]*\]')

def getWosSubfolder(filepath):
    return '123' if not filepath[0].isalpha() else filepath[0].lower()

class Game(object):

    wos_id = 0
    name = None
    publisher = ''
    year = None
    genre = ''
    x_rated = False
    number_of_players = 1
    multiplayer_type = ''
    machine_type = ''
    language = ''
    releases = []
    files = []
    cheats = []
    wos_has_files = False
    help_txt_url = None
    manual_url = None
    loading_screen_gif_filepath = None
    ingame_screen_gif_filepath = None
    loading_screen_scr_filepath = None
    ingame_screen_scr_filepath = None
    manual_filepath = None
    loading_screen_gif_size = 0
    loading_screen_scr_size = 0
    ingame_screen_gif_size = 0
    ingame_screen_scr_size = 0
    manual_size = 0
    parts = 1
    availability = 'A'
    tipshop_page = False
    has_new_pokes = False
    tipshop_multiface_pokes_section = ''
    pok_file_contents = ''

    def __init__(self, name='', wos_id=0, db=None):
        self.setName(name)
        if type(wos_id)!=int:
            raise ValueError('wos_id is not integer')
        self.wos_id = wos_id
        self.files, self.cheats, self.releases = [], [], []
        if db:
            self = db.getGameByWosID(wos_id)

    def __repr__(self):
        return '<Game '+self.getWosID()+':'+self.getTOSECName()+'>'

    def __eq__(self, other):
        if self.wos_id and self.wos_id==other.wos_id:
            return True
        if self.name.replace(' ', '')==other.name.replace(' ', '') and \
            self.year==other.year and \
            self.publisher==other.publisher and \
            not (not self.wos_id and self.wos_id!=other.wos_id):
            return True
        return False

    def getTOSECName(self):
        name = self.name[:100].replace(': ', ' - ')
        filepath = name + ' (' + self.getYear() + ')(' + self.getPublisher() + ')'
        filepath = filepath_regex.sub('', filepath.replace('/', '-')).strip()
        return filepath

    def getWosID(self):
        return str(self.wos_id).zfill(7)

    def getWosUrl(self):
        return WOS_SITE_ROOT + '/infoseekid.cgi?id=' + self.getWosID()

    def getGenre(self):
        return self.genre if self.genre else 'Unknown'

    def getTipshopUrl(self):
        if self.tipshop_page:
            return self.tipshop_page
        else:
            self.tipshop_page = TIPSHOP_SITE_ROOT+'/cgi-bin/info.pl?wosid='+self.getWosID()
            return self.tipshop_page

    def getYear(self):
        return str(self.year) if self.year else '19xx'

    def getPublisher(self):
        return self.publisher if self.publisher else '-'

    def setAvailability(self, value):
        self.availability = value

    def setParams(self, **kwargs):
        self.setPublisher(kwargs['publisher'])
        self.setYear(kwargs['year'])
        self.setGenre(kwargs['genre'])
        self.setNumberOfPlayers(kwargs['number_of_players'])
        self.setMachineType(kwargs['machine_type'])
        self.setLanguage(kwargs['language'])
        self.setAvailability(kwargs['availability'])
        self.pok_file_contents = kwargs['pok_file_contents']
        self.tipshop_multiface_pokes_section = kwargs['tipshop_multiface_pokes_section']

    def setName(self, name):
        if name:
            name = remove_square_brackets_regex.sub('', name).strip()
            self.name = name

    def setPublisher(self, publisher):
        if publisher=='unknown' or not publisher:
            publisher = ''
        publisher = publisher.replace('/', '-')
        publisher = publisher_regex.sub('', publisher)
        publisher = remove_square_brackets_regex.sub('', publisher).strip()
        self.publisher = publisher

    def setYear(self, year):
        if type(year)==int:
            self.year = year
        elif year and year.isdigit():
            self.year = int(year)

    def setNumberOfPlayers(self, n_players):
        if type(n_players)==int:
            self.number_of_players = n_players
        elif n_players:
            self.number_of_players = int(n_players.split(' ')[0])

    def setMultiplayerType(self, mp_type):
        self.multiplayer_type = mp_type

    def getMultiplayerType(self):
        return MULTIPLAYER_TYPES.get(self.multiplayer_type, '')

    def setMachineType(self, machine_type):
        if machine_type:
            self.machine_type = machine_type.replace('ZX-Spectrum', '').replace('/', '-').strip()

    def setLanguage(self, language):
        if not language:
            language='en'
        self.language = language.lower()[:2]

    def getLanguage(self):
        return self.language if self.language else 'en'

    def setGenre(self, genre):
        if not genre:
            self.genre = ''
        else:
            self.genre = genre.replace(':', ' -').replace('I/O', 'IO').replace('/', '-')

    def setmanualUrl(self, url):
        self.manual_url = url

    def addRelease(self, release=None):
        if release:
            self.releases.append(release)

    def addFile(self, new_file, release_seq=0):
        if not new_file:
            return
        try:
            self.releases[release_seq].addFile(new_file)
        except Exception as e:
            print(self)
            raise e

    def getFiles(self):
        files = []
        for release in self.releases:
            files.extend(release.files)
        return files

    def addCheat(self, cheat, cheat_source=CHEAT_SOURCE_SCRAPE):
        if type(cheat)!=Cheat:
            raise TypeError()
        if cheat_source == CHEAT_SOURCE_OLD_DB:
            if cheat in self.cheats:
                self.cheats[self.cheats.index(cheat)].description = cheat.description
        else:
            if cheat not in self.cheats:
                if cheat.description in [x.description for x in self.cheats]:
                    cheat.description += ' (alt)'
                self.cheats.append(cheat)

    def mergeDescriptionsWithOldDBFile(self):
        self.importPokFile()

    def importPokFile(self, file_path=None, text=None):
        if not self.tipshop_page:
            self.tipshop_page = TIPSHOP_SITE_ROOT + '/cgi-bin/info.pl?wosid='+self.getWosID()
        cheat_source = CHEAT_SOURCE_OLD_DB if not file_path and not text else CHEAT_SOURCE_WOS_FILE
        if text!=None:
            if type(text)!=str:
                text = text.decode('utf-8')
            lines = [x.strip() for x in text.split('\n') if x]
        elif file_path:
            with open(file_path) as f:
                lines = f.readlines()
        else:
            file_path = self.findPokFile()
            if not file_path:
                return
            with open(file_path) as f:
                lines = f.readlines()
        for line in lines:
            line = line.replace('\t', ' ')
            if line.startswith('N'):
                c = Cheat(description=line[1:].strip())
            elif line.startswith('M') or line.startswith('Z'):
                line = [x for x in line.split(' ') if x]
                try:
                    c.addPoke(address=line[2], value=line[3], memory_bank=line[1], original_value=line[4])
                except IndexError as e:
                    print('Cannot add poke:', line)
                    raise e
                if line[0]=='Z':
                    self.addCheat(c, cheat_source=cheat_source)

    def findPokFile(self):
        dirpath = os.path.join('AllTipshopPokes', self.name[0].upper())
        file_mask = self.name+'*.pok'
        pok_files = glob.glob(os.path.join(dirpath, file_mask))
        if len(pok_files)==1:
            return pok_files[0]
        else:
            for pok_file in pok_files:
                if str(self.year) in pok_file and \
                   self.publisher in pok_file:
                    return pok_file

    def exportPokFile(self, file_path):
        with open(file_path, 'w+', encoding='utf-8') as f:
            pok_file_contents = self.getPokFileContents()
            f.write(pok_file_contents)

    def getPokFileContents(self):
        if not self.cheats:
            return ''
        pok_file_contents = ''
        for cheat in self.cheats:
            if not cheat.description.startswith('--'):
                pok_file_contents += cheat.asFileRecord()
                pok_file_contents += '\n'
        pok_file_contents += 'Y'
        return pok_file_contents

    def findFileByMD5(self, md5):
        for file in self.getFiles():
            if file.md5 == md5:
                return file

    def findReleaseByFile(self, game_file, strict=False):
        if len(self.releases)==1:
            return self.releases[0]
        for release in self.releases:
            for file in release.files:
                if file.md5 == game_file.md5:
                    return release
        game_file_publisher = game_file.game.publisher.lower().replace('.','')
        for release in self.releases:
            release_publisher = release.publisher.lower().replace('.', '')
            if game_file_publisher==release_publisher:
                return release
        print(self, 'Not found proper release for:', game_file)
        if not strict:
            return self.releases[0]
        else:
            return None