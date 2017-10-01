from classes.game import Game
from functions.game_name_functions import *
from classes.game_release import GameRelease
import requests
import os
import zipfile
import zlib
import hashlib
from settings import *
import re

TOSEC_REGEX = re.compile('[\(\[](.*?)[\)\]]|\.zip|'+'|'.join(['\.'+x for x in GAME_EXTENSIONS]))
ROUND_BRACKETS_REGEX = re.compile('[\(](.*?)[\)]')
SQUARE_BRACKETS_REGEX = re.compile('[\[](.*?)[\]]')


class GameFile(object):

    path = ''
    game = None
    release = None
    release_seq = 0
    wos_name = ''
    wos_zipped_name = ''
    zfname = ''
    wos_path = ''
    tosec_path = ''
    content_desc = ''
    game_name_differentiator = ''
    is_demo = 0
    release_date = ''
    machine_type = ''
    language = ''
    part = 0
    side = 0
    mod_flags = ''
    alt_mod_flag = ''
    notes = ''
    format = ''
    size = 0
    size_zipped = 0
    md5 = ''
    crc32 = ''
    sha1 = ''
    src=''
    dest=''
    alt_dest=''
    is_tosec_compliant = False
    is_alternate = False

    def __init__(self, path='', size=0, game=None, release=None,
                 source=None):
        self.bundled_times = 0
        self.dest = ''
        self.alt_dest = ''
        self.alt_mod_flag = ''
        self.game_name_differentiator = ''
        self.is_alternate = False
        if not path:
            return
        filename = os.path.basename(path)
        self.setSize(size)
        self.format = self.getFormat(path)
        self.game = game
        self.release = release
        if game:
            if filename.endswith('.zip'):
                self.wos_zipped_name = filename
                self.wos_path = path
            else:
                self.wos_name = filename
        else:
            self.getGameFromFileName(path)
        if source == 'wos':
            self.wos_path = path
        elif source == 'tosec':
            # self.getGameFromFileName(path)
            self.getParamsFromTOSECPath(path)
        else:
            self.path = path
        if type(size)==str:
            size = int(size.replace(',',''))

    def __repr__(self):
        return '<GameFile: '+self.getPath()+' md5:'+self.md5+'>'

    def __eq__(self, other):
        if self.wos_name and \
            self.wos_name == other.wos_name and \
            self.size == other.size and \
            self.format == other.format:
            return True
        if self.md5 and self.md5==other.md5:
            return True
        return False

    def getPath(self):
        for path in [self.alt_dest, self.dest, self.path, self.wos_path, self.tosec_path]:
            if path:
                return path

    def importCredentialsFromGame(self, game, overwrite=False):
        self.game = game
        other_file = game.findFileByMD5(self.md5)
        if other_file:
            self.importCredentialsFromFile(other_file, overwrite=overwrite)
            self.release = game.findReleaseByFile(self)

    def importCredentialsFromFile(self, other_file, overwrite=False):
        if other_file.format:
            self.format = other_file.format
        if overwrite or other_file.tosec_path:
            self.tosec_path = other_file.tosec_path
        if overwrite or other_file.content_desc:
            self.content_desc = other_file.content_desc
        if overwrite or other_file.is_demo:
            self.is_demo = other_file.is_demo
        if overwrite or other_file.size:
            self.size = other_file.size
        if overwrite or other_file.language:
            self.language = other_file.language
        if overwrite or other_file.machine_type:
            self.machine_type = other_file.machine_type
        if overwrite or other_file.part:
            self.part = other_file.part
        if overwrite or other_file.side:
            self.side = other_file.side
        if overwrite or other_file.mod_flags:
            self.mod_flags = other_file.mod_flags
        if overwrite or other_file.notes:
            self.notes = other_file.notes

    def countFilesWithSameDestIn(self, collection=[]):
        count = 0
        for other_file in collection:
            if self.dest:
                if self.dest == other_file.dest:
                    count += 1
                continue
        return count

    def countAlternateDumpsIn(self, collection=[]):
        count = 0
        for other_file in collection:
            # if self.game.wos_id==other_file.game.wos_id and \
            #     self.game.name==other_file.game.name and \
            #     self.getYear()==other_file.getYear() and \
            #     self.getPublisher()==other_file.getPublisher() and \
            #     self.getReleaseSeq() == other_file.getReleaseSeq() and \
            #     self.getMachineType() == other_file.getMachineType() and \
            #     self.getMedia() == other_file.getMedia() and \
            #     self.getLanguage() == other_file.getLanguage() and \
            #     self.mod_flags == other_file.mod_flags and \
            #     self.is_demo == other_file.is_demo and \
            #     self.getContentDesc() == other_file.getContentDesc() and \
            #     self.format == other_file.format and \
            #     self.getNotes() == other_file.getNotes():
            #     count += 1

            # if self.game.wos_id != other_file.game.wos_id:
            #     continue
            # if self.getGameName().lower()!=other_file.getGameName().lower():
            #     continue
            if self.game.name != other_file.game.name:
                continue
            if self.getYear() != other_file.getYear():
                continue
            if self.getPublisher() != other_file.getPublisher():
                continue
            if self.getReleaseSeq() != other_file.getReleaseSeq():
                continue
            if self.getMachineType() != other_file.getMachineType():
                continue
            if self.getMedia() != other_file.getMedia():
                continue
            if self.getLanguage() != other_file.getLanguage():
                continue
            if self.mod_flags.lower() != other_file.mod_flags.lower():
                continue
            if self.is_demo != other_file.is_demo:
                continue
            if self.getContentDesc().lower() != other_file.getContentDesc().lower():
                continue
            if self.format.lower() != other_file.format.lower():
                continue
            if self.getNotes().lower() != other_file.getNotes().lower():
                continue
            count += 1
        if count:
            self.is_alternate = True
        return count

    def getEquals(self, collection):
        equals = []
        for other_file in collection:
            if self.game.wos_id == other_file.game.wos_id and \
                self.getYear() == other_file.getYear() and \
                self.getPublisher() == other_file.getPublisher() and \
                self.getReleaseSeq() == other_file.getReleaseSeq() and \
                self.content_desc == other_file.content_desc and \
                self.machine_type == other_file.machine_type and \
                self.side == other_file.side and \
                self.part == other_file.part and \
                self.getLanguage() == other_file.getLanguage() and \
                self.mod_flags == other_file.mod_flags and \
                self.notes == other_file.notes:
                equals.append(other_file)
        return equals

    def addAlternateModFlag(self, copies_count, tosec_compliant, short_filenames):
        if not copies_count:
            return
        dest = os.path.splitext(self.dest if self.dest else self.getTOSECName())
        if short_filenames:
            alt_mod_flag = '_'+str(copies_count+1)
            dir_path = os.path.split(dest[0])
            self.alt_dest = os.path.join(dir_path[0],
                                         dir_path[1][:(8-len(alt_mod_flag))]+alt_mod_flag+dest[1])
        elif tosec_compliant:
            if copies_count == 1:
                self.alt_mod_flag = '[a]'
            else:
                self.alt_mod_flag = '[a' + str(copies_count) + ']'
            dest_dir = os.path.dirname(dest[0])
            dest_filename = os.path.basename(dest[0])
            everything_except_notes = dest_filename.replace(self.getNotes(), '')
            self.alt_dest = os.path.join(dest_dir,
                         everything_except_notes+self.alt_mod_flag+self.getNotes()+'.'+self.format)
        else:
            alt_mod_flag = '_'+str(copies_count+1)
            self.alt_dest = dest[0]+alt_mod_flag+dest[1]

    def isAlternate(self):
        if self.is_alternate:
            return True
        else:
            return False

    def isHack(self):
        if '[c' in self.mod_flags or \
            '[h' in self.mod_flags or \
            '[m' in self.mod_flags or \
            '[f' in self.mod_flags or \
            '[t' in self.mod_flags:
            return True
        else:
            return False

    def isBadDump(self):
        if '[b' in self.mod_flags:
            return True
        else:
            return False

    def isXRated(self):
        if self.game.x_rated:
            return True
        else:
            return False

    def copy(self):
        new = GameFile(self.wos_path, self.size, self.game)
        return new

    def getFileName(self):
        return self.tosec_path if self.tosec_path else os.path.basename(self.wos_path)

    def getGameFromFileName(self, path):
        if '(demo' in path:
            self.is_demo = True
        filename = os.path.splitext(os.path.basename(path).replace('(demo)', ''))[0]
        matches = re.findall(ROUND_BRACKETS_REGEX, filename)
        game_name = re.sub(TOSEC_REGEX, '', filename).strip()
        version = re.findall('v[0-9].*', game_name)
        if version:
            game_name = game_name.replace(version[0], '').strip()
            self.content_desc = ' '+version[0].strip()
        if not self.game:
            self.game = Game(game_name)
        else:
            self.game.name = game_name
        self.release = GameRelease(game=self.game)
        self.game.addRelease(self.release)
        self.game.addFile(self)
        if len(matches)>0:
            self.setReleaseDate(matches[0])
        if len(matches)>1:
            self.game.setPublisher(matches[1])
        self.game.setGenreFromFilePath(path)
        self.getParamsFromTOSECPath(path)

    def getParamsFromTOSECPath(self, tosec_path):
        self.tosec_path = tosec_path
        filename = os.path.splitext(os.path.basename(tosec_path).replace('(demo)', ''))[0]
        self.setMachineType(filename)
        round_brackets_matches = re.findall(ROUND_BRACKETS_REGEX, filename)
        for each in round_brackets_matches[2:]:
            if len(re.findall('^M[0-9]$', each)):
                self.setLanguage(each)
            elif len(re.findall('^[a-z][a-z]-[a-z][a-z]$', each)):
                self.setLanguage(each)
            elif len(each)==2 and each.isalpha():
                if each.islower():
                    self.setLanguage(each)
                elif each.isupper():
                    self.setCountry(each)
            elif 'Side' in each:
                self.setSide(each)
            elif 'Part' in each or 'Disk' in each or 'Tape' in each:
                self.setPart(each)
        square_brackets_matches = re.findall(SQUARE_BRACKETS_REGEX, filename)
        for each in square_brackets_matches:
            if len(re.findall('^a[0-9]?[0-9]?$', each)):
                continue
            elif len(re.findall('^[0-9\-]+K?$', each)):
                self.setMachineType(each)
            elif self.isModFlag(each):
                mod_flag = '[{}]'.format(each)
                if mod_flag not in self.mod_flags:
                    self.mod_flags += mod_flag
            elif each.startswith('aka '):
                aka = getSearchStringFromGameName(each[4:])
                if aka == getSearchStringFromGameName(self.game.name):
                    continue
            elif each in self.notes:
                continue
            elif 're-release' in each:
                continue
            elif 'ZXDB=' in each:
                continue
            elif each.startswith('48'):
                continue
            elif each.startswith('Pentagon'):
                continue
            elif self.machine_type and self.machine_type in each:
                continue
            elif each=='adult':
                self.game.x_rated = 1
            else:
                note = '[{}]'.format(each)
                if note not in self.notes:
                    self.notes += note
        self.sortModFlags()
        if '(demo' in tosec_path.lower():
            self.is_demo = 1

    def isModFlag(self, match):
        for each in MOD_FLAGS_ORDER:
            if match==each:
                return True
            elif match.startswith(each) and \
                match[len(each)] in (' 0123456789'):
                return True
        return False

    def sortModFlags(self):
        mod_flags_array = re.findall(SQUARE_BRACKETS_REGEX, self.mod_flags)
        mod_flags_array = sorted(set(mod_flags_array))
        if 'b' in mod_flags_array:
            mod_flags_array.append(mod_flags_array.pop(mod_flags_array.index('b')))
        self.mod_flags = ''.join('[{}]'.format(x) for x in mod_flags_array)

    def setContentDesc(self, filename):
        if self.game and self.game.wos_id:
            game_name = filename.split('(')[0].strip()
            # aliases = sorted(self.game.getAliases(), key=len, reverse=True)
            aliases = self.game.getAliases()
            alias_found = False
            for alias in aliases:
                alias = alias.lower()
                if alias in game_name.lower():
                    self.content_desc = game_name[game_name.lower().find(alias)+len(alias):].rstrip()
                    alias_found = True
                    break
            if not self.content_desc and not alias_found:
                if ' - ' in game_name:
                    self.content_desc = ' - '+' - '.join(game_name.split(' - ')[1:])
                elif ' + ' in game_name:
                    self.content_desc = ' + '+' + '.join(game_name.split(' + ')[1:])
            if not self.content_desc.startswith(' '):
                self.content_desc = ''
            ss_content_desc = getSearchStringFromGameName(self.content_desc)
            if ss_content_desc in getSearchStringFromGameName(self.getGameName()):
                self.content_desc = ''
            elif ss_content_desc in getSearchStringFromGameName(self.notes):
                self.content_desc = ''
            elif ' - Issue' in self.content_desc:
                self.content_desc = ''
            elif ' - Part ' in self.content_desc:
                split_content_desc = self.content_desc.split(' - Part ')
                part = split_content_desc[1][0]
                if part.isdigit():
                    self.part = int(part)
                    split_content_desc[1] = split_content_desc[1][1:]
                    self.content_desc = ''.join(split_content_desc).strip()


    def setReleaseDate(self, release_date):
        release_date = re.findall('([12][90][x0-9][x0-9](-[x01][x0-9](-[x0-3][x0-9])?)?)', release_date)
        if not release_date:
            return
        else:
            release_date = release_date[0][0]
        if len(release_date)>4:
            self.release_date = release_date
        year = release_date[:4]
        self.game.setYear(year)
        self.release.setYear(year)

    def setMachineType(self, filename):
        if not filename:
            return
        filename = filename.lower()
        if 'pentagon 128' in filename or '(pentagon' in filename or '[pentagon' in filename:
            self.machine_type = 'Pentagon 128K'
        elif 'timex' in filename or 'tc2048' in filename or 'ts2068' in filename:
            self.machine_type = 'TC2048-TS2068'
        elif '+2a-+3' in filename:
            self.machine_type = '+2A-+3'
        elif '[+2a' in filename or '(+2a' in filename:
            self.machine_type = '+2A'
        elif '[+2' in filename or '(+2' in filename:
            self.machine_type = '+2'
        elif '[+3' in filename or '(+3' in filename:
            self.machine_type = '+3'
        elif '128k' in filename and '48' in filename:
            self.machine_type = '48K-128K'
        elif '128k' in filename:
            self.machine_type = '128K'
        elif '48k' in filename:
            self.machine_type = '48K'
        elif '16k' in filename:
            self.machine_type = '16K'
        elif 'zx-uno' in filename or 'zxuno' in filename:
            self.machine_type = 'ZX-UNO'
        elif '(vega)' in filename:
            self.machine_type = 'Vega'
        elif '(next)' in filename:
            self.machine_type = 'Next'
        elif '(atm' in filename:
            self.machine_type = 'ATM'

    def setProtectionScheme(self, protection_scheme):
        if protection_scheme and protection_scheme not in self.notes and \
            protection_scheme not in ('None', 'Undetermined', 'Unknown', 'Unspecified custom loader'):
            protection_scheme = protection_scheme.replace('Firebird ', '')
            protection_scheme = remove_brackets_regex.sub('', protection_scheme).strip()
            self.notes += '['+protection_scheme+']'

    def getMachineType(self):
        if self.machine_type:
            return self.machine_type
        else:
            return self.game.machine_type

    def setLanguage(self, language):
        # language = language.lower() if language.isalpha() else language.upper()
        if len(language)==2 or len(language)==5:
            self.language = language

    def setCountry(self, country):
        country = country.upper()
        if len(country)==2:
            if not self.release:
                print(self, 'has no self.release')
            self.release.country = country
            self.language = COUNTRY_LANGUAGE_DICT.get(country, country.lower())

    def getCountry(self):
        if self.release and self.release.country:
            return self.release.country
        return ''

    def setPart(self, part):
        part = part.replace(' ', '').lower()
        for word in ('part', 'disk', 'tape'):
            if word in part:
                index = part.index(word)+len(word)-1
                if part[index] in ['-']:
                    index+=1
                if len(part)>index+1 and part[index+1].isdigit():
                    index += 1
                    part_num = part[index]
                    while True:
                        index += 1
                        if index>=len(part) or not part[index].isdigit():
                            break
                        else:
                            part_num += part[index]
                    self.part = int(part_num)

    def setLanguageFromWosName(self):
        name = self.wos_name.lower()
        for each in INCLUDED_LANGUAGES_LIST:
            if '('+each[0]+')' in name or '('+each[1].lower()+')' in name:
                self.language = each[0]
                break

    def setContentDescFromWosName(self):
        content_desc = os.path.splitext(self.wos_name)[0].replace(' - ', '')
        for alias in self.release.getAllAliases():
            content_desc = content_desc.replace(alias, '')
        self.content_desc = ' - '+content_desc

    def getMedia(self):
        return ' '.join((self.getPart(), self.getSide())).strip()

    def getPart(self):
        if not self.part:
            return ''
        if self.game.parts<2:
            return ''
        if self.format in DISK_FORMATS:
            label = 'Disk'
        elif self.format in TAPE_FORMATS:
            label = 'Tape'
        else:
            label = 'Part'
        if self.game.parts>1:
            return  '%s %d of %d' % (label, self.part, self.game.parts)

    def getLanguage(self):
        if self.language:
            return self.language
        elif '[tr ' in self.mod_flags:
            return self.mod_flags.split('[tr ')[1][:2]
        else:
            return self.game.getLanguage()

    def getTOSECName(self, game_name_length=MAX_GAME_NAME_LENGTH):
        output_name = self.getOutputName(game_name_length=game_name_length)
        return output_name

    def getOutputName(self, structure=TOSEC_COMPLIANT_FILENAME_STRUCTURE,
                      game_name_length=MAX_GAME_NAME_LENGTH):
        if not structure:
            structure = TOSEC_COMPLIANT_FILENAME_STRUCTURE
        structure = structure.replace('{TOSECName}', TOSEC_COMPLIANT_FILENAME_STRUCTURE)
        if not structure.endswith('.{Format}'):
            structure += '.{Format}'
        kwargs = self.getOutputPathFormatKwargs(game_name_length=game_name_length,
                                                for_filename=True)
        output_name = structure.format(**kwargs)
        if structure==TOSEC_COMPLIANT_FILENAME_STRUCTURE+'.{Format}':
            country = self.getCountry().lower()
            if country==self.getLanguage() or \
                COUNTRY_LANGUAGE_DICT.get(country.upper())==self.getLanguage() or \
                '[tr ' in self.mod_flags:
                output_name = output_name.replace('(%s)' % self.getLanguage(), '')
                if self.getLanguage() == 'en' or \
                        (self.getCountry()=='GB' and '[tr ' in self.mod_flags):
                    output_name = output_name.replace('(%s)' % self.getCountry(), '')
            output_name = output_name.replace('(%s)' % DEFAULT_MACHINE_TYPE, '')
        output_name = output_name.replace('()', '').replace('[]', '')
        output_name = ' '.join([x for x in output_name.split(' ') if x])
        output_name = filepath_regex.sub('', output_name.replace('/', '-').replace(':', ' -'))
        filename, ext = os.path.splitext(output_name)
        output_name = filename.strip()+ext
        return output_name

    def setSide(self, side):
        side = side.lower().replace(' ', '')
        if 'sidea' in side or 'side1' in side:
            self.side = SIDE_A
        elif 'sideb' in side or 'side2' in side:
            self.side = SIDE_B
        elif 'side3' in side:
            self.side = SIDE_A
            self.part = 2
        elif 'side4' in side:
            self.side = SIDE_B
            self.part = 2
        elif 'side5' in side:
            self.side = SIDE_A
            self.part = 3
        elif 'side6' in side:
            self.side = SIDE_B
            self.part = 3


    def getSide(self):
        if self.side == SIDE_A:
            return 'Side A'
        elif self.side == SIDE_B:
            return 'Side B'
        else:
            return ''

    def setSize(self, size=0):
        if type(size)==str:
            size = int(size.replace(',',''))
        self.size = size

    def getSize(self):
        return '{:,}'.format(self.size)

    def getFormat(self, path=None):
        if not path:
            path = self.getPath()
        filename = os.path.basename(path)
        format = filename.replace('.zip','').split('.')[-1].lower()
        if format in GAME_EXTENSIONS:
            return format
        format = os.path.split(os.path.dirname(path))[-1].replace('[', '').replace(']', '').lower()
        if format in GAME_EXTENSIONS:
            return format
        if path.endswith('.zip'):
            with zipfile.ZipFile(path, 'r') as zf:
                for zfname in zf.namelist():
                    zfname_ext = zfname.split('.')[-1].lower()
                    if zfname_ext in GAME_EXTENSIONS:
                        return zfname_ext
        return None

    def getMD5(self):
        if self.md5:
            return self.md5
        local_path = self.getLocalPath()
        if os.path.exists(local_path):
            file_handle = self.getFileHandle(local_path)
            if not file_handle:
                print(self, 'has no valid file handle!')
                return ''
            md5 = hashlib.md5(file_handle).hexdigest()
            self.md5 = md5
            return md5

    def getCRC32(self):
        if self.crc32:
            return self.crc32
        local_path = self.getLocalPath()
        if os.path.exists(local_path):
            file_handle = self.getFileHandle(local_path)
            if not file_handle:
                print(self, 'has no valid file handle!')
                return ''
            crc32 = hex(zlib.crc32(file_handle))[2:].zfill(8)
            self.crc32 = crc32
            return crc32

    def getSHA1(self):
        if self.sha1:
            return self.sha1
        local_path = self.getLocalPath()
        if os.path.exists(local_path):
            file_handle = self.getFileHandle(local_path)
            if not file_handle:
                print(self, 'has no valid file handle!')
                return ''
            self.sha1 = hashlib.sha1(file_handle).hexdigest()
            return self.sha1

    def getFileHandle(self, local_path, zipped=False):
        if local_path.endswith('.zip') and not zipped:
            with zipfile.ZipFile(local_path, 'r') as zf:
                for zfname in zf.namelist():
                    zfname_ext = zfname.split('.')[-1].lower()
                    if zfname_ext != self.format and zfname_ext in GAME_EXTENSIONS:
                        if self.format:
                            print('FORMAT MISMATCH:', self, zfname)
                        self.format = zfname_ext
                    if zfname_ext == self.format:
                        if not self.size:
                            self.setSize(zf.getinfo(zfname).file_size)
                        if not self.crc32:
                            self.crc32 = hex(zf.getinfo(zfname).CRC)[2:].zfill(8)
                        return zf.read(zfname)
        else:
            with open(local_path, 'rb')as f:
                return f.read()

    def getOutputPathFormatKwargs(self, game_name_length=MAX_GAME_NAME_LENGTH,
                                  for_filename=False):
        game_name = self.getGameName(game_name_length=game_name_length, for_filename=for_filename)
        publisher = self.getPublisher(restrict_length=game_name_length<MAX_GAME_NAME_LENGTH)
        if publisher == '-' and not for_filename:
            publisher = 'Unknown Publisher'
        return {
            'Type':self.getType(),
            'Genre':self.getGenre(),
            'Year':self.getYear(for_filename=for_filename),
            'Letter':getWosSubfolder(game_name),
            'MachineType':self.getMachineType(),
            'Publisher':publisher,
            'MaxPlayers':self.getMaxPlayers(),
            'GameName':game_name,
            'Country':self.getCountry(),
            'Language':self.getLanguage(),
            'Format':self.format,
            'Media':self.getMedia(),
            'Part':self.getPart(),
            'Side':self.getSide(),
            'ModFlags':self.mod_flags+self.alt_mod_flag,
            'ZXDB_ID':self.game.getWosID(),
            'Notes':self.getNotes(),
            'OriginalName':self.getOriginalName(),
        }

    def getOriginalName(self):
        if self.src:
            return os.path.splitext(os.path.basename(self.src))[0]

    def getNotes(self):
        if self.notes == 'NONE':
            return ''
        if self.notes.startswith('ALT '):
            notes = self.notes[4:]
        else:
            notes = self.notes
        if self.game.x_rated:
            return notes + X_RATED_FLAG
        else:
            return notes

    def getTOSECDatName(self):
        parts = ['Sinclair ZX Spectrum'] #Hardcoded until ZX81 and other machines' support is about to be added
        parts += self.getType().split('\\')
        parts.append('[{}]'.format(self.format.upper()))
        return ' - '.join(parts)

    def getGenre(self):
        if self.game.genre:
            return self.game.getGenre()
        else:
            return 'Unknown'
        return 'Unknown'

    def getType(self):
        if self.game.name.startswith('ZZZ-UNK'):
            self.type = 'Unknown'
            return self.type
        genre = self.getGenre()
        self.type = ''
        if 'Compilation' in genre:
            self.type += 'Compilations'
            if 'Utilities' in genre:
                self.type += os.sep+'Applications'
            elif 'Educational' in genre:
                self.type += os.sep+'Educational'
            elif 'Demo' in genre:
                self.type += os.sep+'Demos'
            elif 'Magazine' in genre:
                self.type += os.sep+'Magazines'
            elif 'Mixed' in genre:
                self.type += os.sep+'Mixed'
            else:
                self.type += os.sep+'Games'
        elif 'Education' in genre:
            self.type += 'Educational'
        elif genre.startswith('Utility') or \
            'Programming' in genre or \
            'General' in genre or \
            'Emulator' in genre:
            self.type += 'Applications'
        elif 'Magazine' in genre:
            self.type += 'Magazines'
        elif 'Covertape' in genre:
            self.type += 'Covertapes'
        elif 'Demo' in genre:
            self.type += 'Demos'
        elif 'Music' in genre:
            self.type += 'Music'
        elif 'e-Book' in genre:
            self.type += 'eBooks'
        elif 'Documentation' in genre:
            self.type += 'Documentation'
        elif 'Game' in genre:
            self.type += 'Games'
        else:
            self.type = 'Unknown'
        return self.type

    def setReRelease(self):
        if '[re-release]' not in self.notes and \
                self.release.release_seq>0:
            for release in self.game.releases:
                if self.release.release_seq != release.release_seq and \
                    self.release.getYear()==release.getYear():
                    self.notes += '[re-release]'
                    break

    def setAka(self):
        if '[aka' not in self.notes:
            aliases_search_strings = []
            game_name_search_string = getSearchStringFromGameName(self.getGameName())
            aliases_search_strings.append(game_name_search_string)
            for alias in self.release.getAllAliases():
                alias_search_string = getSearchStringFromGameName(alias)
                if not [x for x in aliases_search_strings if x in alias_search_string or alias_search_string in x]:
                    alias = putPrefixToEnd(alias)
                    self.notes += '[aka '+alias+']'
                    aliases_search_strings.append(alias_search_string)

    def getGameName(self, game_name_length=MAX_GAME_NAME_LENGTH,
                    for_filename=False,
                    short=False):
        if for_filename and game_name_length<=70:
            self.removeAka()
        release_aliases = self.release.getAllAliases()
        game_name = release_aliases[0] if release_aliases else self.game.name
        if not game_name:
            print('No game_name for file:', self)
            return ''
        game_name = filepath_regex.sub('', game_name.replace('/', '-').replace(':', ' -')).strip()
        while game_name.endswith('.'):
            game_name = game_name[:-1]
        if short:
            return getMeaningfulEightLetterName(game_name)
        if for_filename and self.content_desc:
            game_name += self.getContentDesc()
        if self.game_name_differentiator:
            game_name += '('+self.game_name_differentiator+')'
        while len(game_name)>game_name_length:
            game_name = [x for x in game_name.split(' ') if x][:-1]
            game_name = ' '.join(game_name)
        game_name = [x for x in game_name.split(' ') if x]
        while len(game_name[-1])<2 and \
                not game_name[-1][-1].isalnum():
            game_name = ' '.join(game_name[:-1])
            game_name = [x for x in game_name.split(' ') if x]
        game_name = ' '.join(game_name).strip()
        if for_filename and self.is_demo:
            game_name += ' (demo)'
        return game_name

    def removeAka(self):
        if '[aka' in self.notes:
            self.notes = re.sub('(\[aka.+?\])', '', self.notes, count=1)

    def getContentDesc(self):
        if self.content_desc=='NONE':
            return ''
        elif self.content_desc.startswith('ALT'):
            return self.content_desc[3:]
        elif self.content_desc:
            return self.content_desc
        else:
            return ''

    def getYear(self, for_filename=True):
        if for_filename and self.release_date:
            return self.release_date
        if self.release:
            year = self.release.getYear()
        else:
            year = self.game.getYear()
        if not for_filename:
            year = year[:4]
        return year

    def getPublisher(self, restrict_length=False):
        if self.release:
            publisher =  self.release.getPublisher()
        else:
            publisher = self.game.getPublisher()
        if restrict_length:
            publisher = [x for x in publisher.split(' ') if x][:3]
            if len(publisher)==3 and len(publisher[-1])<3:
                publisher = publisher[:-1]
            publisher = ' '.join(publisher).strip()
        return publisher

    def getMaxPlayers(self):
        result = str(self.game.number_of_players) + 'P'
        return result
        #FUTURE:
        # if self.game.multiplayer_type:
            # result += ' (%s)' % self.game.getMultiplayerType()
        # return result

    def getReleaseSeq(self):
        return self.release.release_seq if self.release else 0

    def getSortIndex(self, preferred_formats_list=GAME_EXTENSIONS):
        try:
            return preferred_formats_list.index(self.format)
        except IndexError:
            return 99

    def getWosPath(self, wos_mirror_root = WOS_SITE_ROOT):
        return wos_mirror_root+self.wos_path

    def getLocalPath(self):
        if self.wos_path:
            local_path = os.path.abspath(self.getWosPath(wos_mirror_root=LOCAL_FTP_ROOT))
            return local_path
        elif self.path:
            return self.path
        elif self.tosec_path:
            return self.tosec_path

    def getDestPath(self):
        dest = self.alt_dest if self.alt_dest else self.dest
        return dest

    def getSrcPathForLog(self):
        src = self.src
        if self.zfname and src.lower().endswith('.zip'):
            src = self.zfname + ' from ' + src
        return src

    def getBundleName(self, depth_level):
        root_dir, bundled_part = self.getSplitDest(depth_level)
        bundle_name = bundled_part.split('\\')[0]
        bundle_name =  ''.join([x for x in bundle_name if x.isalnum()])[:3].lower()
        return bundle_name

    def setBundle(self, bundle_name, depth_level):
        root_dir, bundled_part = self.getSplitDest(depth_level)
        dest = os.path.join(root_dir, bundle_name, bundled_part)
        self.bundled_times += 1
        self.alt_dest = dest

    def getSplitDest(self, depth_level):
        if not depth_level:
            depth_level += 1
        dest = self.getDestPath()
        dest = dest.replace('/', '\\').split('\\')
        root_dir = os.sep.join(dest[:-depth_level])
        depth_level -= self.getBundledTimes(dest)
        bundled_part = os.sep.join(dest[-depth_level:])
        # dest = [re.sub('^[0-9a-z]{,3}\-[0-9a-z]{,3}[0-9]?$', '', x) for x in dest]
        # dest = [x for x in dest if x]
        # bundled_part = os.sep.join(dest)
        return root_dir, bundled_part

    def getBundledTimes(self, dest):
        # return self.bundled_times
        bundled_times = 0
        for folder in dest:
            if re.match('^[0-9a-z]{,3}\-[0-9a-z]{,3}[0-9]?$', folder):
                bundled_times += 1
        return bundled_times

    def getAbsoluteDestPath(self):
        return os.path.abspath(self.getDestPath())