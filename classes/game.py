from functions.game_name_functions import *
from classes.cheat import *
from classes.poke import *
from settings import *
import os
import glob
import re

class Game(object):

    zxdb_id = 0
    name = ''
    publisher = ''
    author = ''
    year = None
    genre = ''
    type = 'Unknown'
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

    def __init__(self, name='', zxdb_id=0, db=None):
        self.setName(name)
        if type(zxdb_id)!=int:
            raise ValueError('zxdb_id is not integer')
        self.zxdb_id = zxdb_id
        self.files, self.cheats, self.releases = [], [], []
        if db:
            self = db.getGameByWosID(zxdb_id)

    def __repr__(self):
        return '<Game '+self.getWosID()+':'+self.getTOSECName()+'>'

    def __eq__(self, other):
        if self.zxdb_id and self.zxdb_id==other.zxdb_id:
            return True
        if self.name.replace(' ', '')==other.name.replace(' ', '') and \
            self.year==other.year and \
            self.publisher==other.publisher and \
            not (not self.zxdb_id and self.zxdb_id!=other.zxdb_id):
            return True
        return False

    def getTOSECName(self, game_name_length=MAX_GAME_NAME_LENGTH):
        name = self.name[:game_name_length].replace(': ', ' - ')
        filepath = name + ' (' + self.getYear() + ')(' + self.getPublisher() + ')'
        filepath = filepath_regex.sub('', filepath.replace('/', '-')).strip()
        return filepath

    def getAliases(self):
        aliases = []
        for release in self.releases:
            aliases += release.aliases
        aliases = sorted(aliases, key=lambda alias: (len(alias), alias), reverse=True)
        return [getFileSystemFriendlyName(alias) for alias in aliases]

    def getWosID(self):
        return str(self.zxdb_id).zfill(7)

    def getWosUrl(self):
        return WOS_SITE_ROOT + '/infoseekid.cgi?id=' + self.getWosID()

    def setContentDescForZXDBFiles(self, lookup_table={}):
        files = self.getFiles()
        for file in files:
            key = file.wos_path+'|'+file.wos_name
            if key in lookup_table:
                file.content_desc = lookup_table[key]

    def setContentDescForFiles(self, lookup_table={}):
        files = self.getFiles()
        for file in files:
            if file.md5 in lookup_table:
                file.content_desc = lookup_table[file.md5]
                continue
            if file.tosec_path and not file.content_desc:
                filename = os.path.basename(file.tosec_path)
                file.setContentDesc(filename)

    def setNotesForFiles(self, lookup_table={}):
        files = self.getFiles()
        for file in files:
            md5 = file.getMD5()
            if md5 in lookup_table:
                file.notes = lookup_table[md5]
            else:
                file.setAka()
                file.setReRelease()
                if 'Covertape' in file.notes:
                    covertape_comment = '[{} Covertape]'.format(file.release.getPublisher())
                    if covertape_comment in file.notes:
                        file.notes = file.notes.replace(covertape_comment, '')

    def setTypeFromFiles(self):
        if self.genre and self.genre!='Compilation':
            return
        files = self.getFiles()
        for file in files:
            if 'Compilation' in file.tosec_path:
                self.setGenreFromFilePath(file.tosec_path)
                if self.genre:
                    break
        if not self.genre:
            for file in files:
                self.setGenreFromFilePath(file.tosec_path)
                if self.genre:
                    break

    def setCountryFromFiles(self):
        for file in self.getFiles():
            if file.getLanguage() in ['pl', 'ru', 'cs', 'sl', 'bs']:
                if file.getCountry() in ['GB', 'ES']:
                    mod_flag = '[tr {}]'.format(file.getLanguage())
                    file.addModFlag(mod_flag)
                    # if mod_flag not in file.mod_flags:
                    #     file.mod_flags += mod_flag
                    file.language = ''
                elif not file.getCountry():
                    if file.getLanguage()=='cs':
                        file.release.country = 'CZ'
                    elif file.getLanguage()=='sl':
                        file.release.country = 'SI'
                    else:
                        file.release.country = file.getLanguage().upper()
                    if not file.game.language:
                        file.game.language = file.getLanguage()
                    file.language = ''


    def setGenreFromFilePath(self, path):
        path = ''.join(os.path.split(path)[-3:]).lower()
        if self.publisher == 'Vaxalon':
            self.genre = 'Scene Demo'
            return
        if 'compilation' in path:
            self.genre = 'Compilation'
            if 'demo' in path:
                self.genre += ' - Demos'
            elif 'education' in path:
                self.genre += ' - Educational'
            elif 'magazine' in path:
                self.genre += ' - Magazines'
            elif 'application' in path:
                self.genre += ' - Utilities'
            elif 'book' in path:
                self.genre += 'Books'
            elif 'music' in path:
                self.genre += 'Music'
            elif 'mixed' in path:
                self.genre += ' - Mixed'
            else:
                self.genre += ' - Games'
        elif 'firmware' in path:
            self.genre = 'Firmware'
        elif 'magazines' in path:
            self.genre = 'Electronic Magazine'
        elif 'application' in path:
            self.genre = 'Utility'
        elif 'covertapes' in path:
            self.genre = 'Covertape'
        elif 'demos' in path:
            self.genre = 'Scene Demo'
        elif 'education' in path:
            self.genre = 'General - Education'
        elif 'documentation' in path:
            self.genre = 'Documentation'
        elif 'games' in path:
            self.genre = 'Various Games'
        elif 'music' in path:
            self.genre = 'Music'
        elif 'book' in path:
            self.genre = 'Books'

    def getGenre(self):
        return self.genre if self.genre else 'Unknown'

    def getTipshopUrl(self):
        if self.tipshop_page:
            return self.tipshop_page
        else:
            return None

    def getYear(self):
        return str(self.year) if self.year else '19xx'

    def getPublisher(self):
        if self.publisher:
            return self.publisher
        elif self.author:
            return self.author
        else:
            return '-'

    def getAuthor(self):
        if self.author:
            return self.author
        else:
            return '-'

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
            name = getFileSystemFriendlyName(name)
            self.name = name

    def setPublisher(self, publisher):
        if publisher=='unknown' or not publisher:
            publisher = ''
        publisher = remove_brackets_regex.sub('', publisher).strip()
        publisher = publisher.replace('/', '-').strip()
        publisher = publisher_regex.sub('', publisher)
        self.publisher = publisher.strip()

    def setAuthor(self, author):
        if author:
            self.author = author

    def setYear(self, year):
        self.year = year

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
            if 'TC20' in machine_type or 'TS20' in machine_type:
                machine_type = 'TC2048-TS2068'
            else:
                machine_type = machine_type.replace('ZX-Spectrum', '').replace('/', '-').strip()
                if '+2' in machine_type or '+3' in machine_type:
                    machine_type = machine_type.replace('128 ', '')
        else:
            machine_type = '48K'
        self.machine_type = machine_type

    def setLanguage(self, language):
        if not language:
            language='en'
        self.language = language.lower()[:2]

    def getLanguage(self):
        if self.language.startswith('?') or self.language.endswith('-'):
            return 'en'
        return self.language if self.language else 'en'

    def setGenre(self, genre):
        if not genre:
            self.genre = ''
            self.type = ''
        else:
            self.genre = genre.replace(':', ' -').replace('I/O', 'IO').replace('/', '-')
            self.setType(genre)

    def setType(self, genre):
        if 'Compilation' in genre:
            self.type = genre.replace(' - ', '/')
        # if 'Box Set' in genre:
        #     self.type = 'Compilation'
        if 'Domestic' in genre:
            self.type = 'Applications'
        elif 'Business' in genre:
            self.type = 'Applications'
        elif 'Industrial' in genre:
            self.type = 'Applications'
        elif 'Emulator' in genre:
            self.type = 'Applications'
        elif 'Programming' in genre:
            self.type = 'Applications'
        elif 'Simulation' in genre:
            self.type = 'Applications'
        elif 'Utilit' in genre:
            self.type = 'Applications'
        elif 'Education' in genre:
            self.type = 'Educational'
        elif 'Covertape' in genre:
            self.type = 'Covertapes'
        elif 'Magazine' in genre:
            self.type = 'Magazines'
        elif 'Game' in genre:
            self.type = 'Games'
        elif 'Music' in genre:
            self.type = 'Music'
        elif 'Demo' in genre:
            self.type = 'Demos'
        elif 'Book' in genre:
            self.type = 'Books'
        elif 'Hardware' in genre:
            self.type = 'Firmware'

    def setmanualUrl(self, url):
        self.manual_url = url

    def addRelease(self, release=None):
        if release:
            self.releases.append(release)

    def addFile(self, new_file, release_seq=0):
        if not new_file:
            return
        # try:
        self.releases[release_seq].addFile(new_file)
        # except Exception as e:
        #     print(self)
        #     raise e

    def getFiles(self):
        files = []
        for release in self.releases:
            files.extend(release.files)
        return files

    def addCheat(self, cheat, cheat_source=CHEAT_SOURCE_SCRAPE, modify_description_on_collision=False):
        if type(cheat)!=Cheat:
            raise TypeError()
        if cheat not in self.cheats:
            self.cheats.append(cheat)
        elif modify_description_on_collision:
            for existing_cheat in self.cheats:
                if existing_cheat == cheat:
                    existing_cheat.description = cheat.description

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
                except Exception as e:
                    print('Cannot add poke:', line, e)
                    print(self.zxdb_id)
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
                if str(self.getYear()) in pok_file and \
                   self.getPublisher() in pok_file:
                    return pok_file

    def exportPokFile(self, file_path):
        with open(file_path, 'w+', encoding='utf-8') as f:
            pok_file_contents = self.getPokFileContents()
            f.write(pok_file_contents)

    def getPokFileContents(self, for_xlsx=False):
        if not self.cheats:
            return ''
        pok_file_contents = ''
        for cheat in self.cheats:
            if not cheat.description.startswith('--'):
                pok_file_contents += cheat.asFileRecord(for_xlsx=for_xlsx)
                pok_file_contents += '\n'
        pok_file_contents += 'Y'
        return pok_file_contents

    def getSpectrumComputingURL(self):
        if self.zxdb_id>9000000:
            return "This file is not in ZXDB"
        return "https://spectrumcomputing.co.uk/index.php?cat=96&id={}".format(self.zxdb_id)

    def findFileByCRC32(self, crc32):
        for file in self.getFiles():
            if file.crc32 == crc32:
                return file #assuming there are NO CRC collisions within a single game entry.

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
                    release.importInfoFromGameFile(game_file)
                    return release
        game_file_publisher = game_file.game.publisher.lower().replace('.','')
        for release in self.releases:
            release_publisher = release.publisher.lower().replace('.', '')
            if game_file_publisher==release_publisher:
                return release
        # print(self, 'Not found proper release for:', game_file)
        if not strict:
            return self.releases[0]
        else:
            return None