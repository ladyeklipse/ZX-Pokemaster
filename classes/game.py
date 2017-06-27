# from classes.game_release import GameRelease
# from classes.game_file import GameFile
from classes.cheat import *
from classes.poke import *
from settings import *
import os
import glob
import re

publisher_regex = re.compile('inc[ .]|ltd|plc', re.IGNORECASE)
filepath_regex = re.compile('\*|\?|\:|\||\\|/|\"|<|>|')

def getWosSubfolder(filepath):
    return '123' if filepath[0].isdigit() else filepath[0].lower()

class Game(object):

    wos_id = 0
    name = None
    publisher = ''
    year = None
    genre = ''
    x_rated = False
    number_of_players = 1
    machine_type = ''
    language = 'en'
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
    availability = AVAILABILITY_AVAILABLE
    tipshop_page = False
    has_new_pokes = False
    tipshop_multiface_pokes_section = ''
    pok_file_contents = ''

    def __init__(self, name='', wos_id=0, db=None):
        self.name=name
        if type(wos_id)!=int:
            raise ValueError('wos_id is not integer')
        self.wos_id = wos_id
        self.files, self.cheats = [], []
        if db:
            self.getInfoFromDB(db)
        self.releases = []

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
        filepath = self.name + ' (' + self.getYear() + ')(' + self.getPublisher() + ')'
        filepath = filepath_regex.sub('', filepath.replace('/', '-')).strip()
        return filepath

    def getInfoFromDB(self, db):
        game_from_db = db.getGameByWosID(self.wos_id)
        if game_from_db:
            self.name = game_from_db.name
            self.publisher = game_from_db.publisher
            self.year = game_from_db.year
            self.genre = game_from_db.genre
            self.number_of_players = game_from_db.number_of_players
            self.machine_type = game_from_db.machine_type
            self.language = game_from_db.language
            self.ingame_screen_filepath = game_from_db.ingame_screen_filepath
            self.loading_screen_filepath = game_from_db.ingame_screen_filepath
            self.manual_filepath = game_from_db.manual_filepath
            self.files = game_from_db.files
            self.cheats = game_from_db.cheats
            self.pok_file_contents = game_from_db.pok_file_contents

    def getWosID(self):
        return str(self.wos_id).zfill(7)

    def getWosUrl(self):
        return WOS_SITE_ROOT + '/infoseekid.cgi?id=' + self.getWosID()

    def getTipshopUrl(self):
        return self.tipshop_page

    def getManualUrl(self):
        return self.manual_url

    def getYear(self):
        return str(self.year) if self.year else '19--'

    def getPublisher(self):
        return self.publisher if self.publisher else '-'

    def setAvailability(self, value):
        if value == 'D':
            self.availability = AVAILABILITY_DISTRIBUTION_DENIED
        elif value == 'd':
            self.availability = AVAILABILITY_DISTRIBUTION_DENIED_STILL_FOR_SALE
        elif value == '?':
            self.availability = AVAILABILITY_MISSING_IN_ACTION
        elif value == 'N':
            self.availability = AVAILABILITY_NEVER_RELEASED
        elif value == 'R':
            self.availability = AVAILABILITY_RECOVERED
        else:
            self.availability = AVAILABILITY_AVAILABLE

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

    def addAlternateName(self, name, publisher=None):
        if not publisher:
            publisher = self.publisher
        if name!=self.name and \
            name not in [x[0] for x in self.alternate_names]:
                self.alternate_names.append((name, publisher))

    def setTitle(self, title):
        self.name = title

    def setPublisher(self, publisher):
        if publisher=='unknown' or not publisher:
            publisher = ''
        publisher = publisher_regex.sub('', publisher).strip()
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

    def setMachineType(self, machine_type):
        if machine_type:
            self.machine_type = machine_type.replace('ZX-Spectrum', '').strip()

    def setLanguage(self, language):
        if not language:
            language='en'
        self.language = language.lower()[:2]

    def setGenre(self, genre):
        self.genre = genre #.replace(':', '')

    def setmanualUrl(self, url):
        self.manual_url = url

    def addRelease(self, release=None):
        if release:
            self.releases.append(release)

    def addFile(self, new_file, release_seq=0):
        if not new_file:
            return
        self.releases[release_seq].addFile(new_file)

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

    def getRemoteIngameScreenUrl(self, format='gif',
                                 wos_mirror_root = WOS_SITE_ROOT,
                                 release_seq=0):
        ingame_screen_filepath = self.releases[release_seq].getIngameScreenFilePath(format)
        if not ingame_screen_filepath and release_seq>0:
            ingame_screen_filepath = self.releases[0].getIngameScreenFilePath(format)
        return '/'.join(wos_mirror_root, ingame_screen_filepath)

    def getRemoteLoadingScreenUrl(self, format='gif',
                                    wos_mirror_root = WOS_SITE_ROOT,
                                    release_seq = 0):
        loading_screen_filepath = self.releases[release_seq].getLoadingScreenFilePath(format)
        if not loading_screen_filepath and release_seq>0:
            loading_screen_filepath = self.releases[0].getLoadingScreenFilePath(format)
        return '/'.join(wos_mirror_root, loading_screen_filepath)

    def getRemoteManualUrl(self,
                            wos_mirror_root = WOS_SITE_ROOT,
                            release_seq = 0):
        manual_filepath = self.releases[release_seq].getManualFilePath(format)
        if not manual_filepath and release_seq>0:
            manual_filepath = self.releases[0].getManualFilePath(format)
        return '/'.join(wos_mirror_root, manual_filepath)

    def getLocalManualPath(self, release_seq=0):
        return self.getRemoteManualUrl(wos_mirror_root=LOCAL_FTP_ROOT, release_seq=release_seq)

    def getLocalLoadingScreenPath(self, format='scr', release_seq=0):
        return self.getRemoteLoadingScreenUrl(format, wos_mirror_root=LOCAL_FTP_ROOT, release_seq=release_seq)

    def getLocalIngameScreenPath(self, format='scr', release_seq=0):
        return self.getRemoteIngameScreenUrl(format, wos_mirror_root=LOCAL_FTP_ROOT, release_seq=release_seq)

    def findReleaseByFile(self, game_file):
        if len(self.releases)==1:
            return self.releases[0]
        for release in self.releases:
            if game_file.game.name in release.getAllAliases() and \
                game_file.game.year==release.year:
                return release.release_seq
        return None