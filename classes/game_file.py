from classes.game import Game, getWosSubfolder, filepath_regex
from classes.game_release import GameRelease
import requests
import os
import zipfile
import hashlib
from settings import *
import re

TOSEC_REGEX = re.compile('[\(\[](.*?)[\)\]]|\.zip|'+'|'.join(['\.'+x for x in GAME_EXTENSIONS]))

def putPrefixToEnd(game_name):
    if game_name.startswith('Die Hard'):
        return game_name
    if game_name.endswith(', 3D'):
        game_name = '3D '+game_name[:-4]
    for prefix in GAME_PREFIXES:
        if game_name.startswith(prefix + ' '):
            game_name = ' '.join(game_name.split(' ')[1:]) + ', ' + prefix
            return game_name
    return game_name

class GameFile(object):

    path = ''
    game = None
    release = None
    release_seq = 0
    wos_name = ''
    wos_zipped_name = ''
    wos_path = ''
    tosec_path = ''
    content_desc = ''
    is_demo = 0
    machine_type = '48K'
    language = ''
    part = 0
    side = 0
    mod_flags = ''
    notes = ''
    format = ''
    size = 0
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
        if not path:
            return
        filename = os.path.basename(path)
        self.setSize(size)
        self.format = self.getFormat(path)
        if source == 'wos':
            self.wos_path = path
        elif source == 'tosec':
            self.getParamsFromTOSECPath(path)
        else:
            self.path = path
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

    def importCredentials(self, game):
        self.game = game
        other_file = game.findFileByMD5(self.md5)
        if other_file:
            self.content_desc = other_file.content_desc
            self.part = other_file.part
            self.language = other_file.language
            self.mod_flags = other_file.mod_flags
            self.notes = other_file.notes
            self.side = other_file.side
            self.machine_type = other_file.machine_type
            self.format = other_file.format
            self.release = game.findReleaseByFile(self)

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
            if self.game.wos_id==other_file.game.wos_id and \
                self.getYear()==other_file.getYear() and \
                self.getPublisher()==other_file.getPublisher() and \
                self.getReleaseSeq() == other_file.getReleaseSeq() and \
                self.getMachineType() == other_file.getMachineType() and \
                self.side == other_file.side and \
                self.part == other_file.part and \
                self.getLanguage() == other_file.getLanguage() and \
                self.mod_flags == other_file.mod_flags and \
                self.is_demo == other_file.is_demo and \
                self.content_desc == other_file.content_desc and \
                self.format == other_file.format:
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
                self.mod_flags == other_file.mod_flags:
                equals.append(other_file)
        return equals

    def addAlternateModFlag(self, copies_count, tosec_compliant, short_filenames):
        if not copies_count:
            return
        dest = os.path.splitext(self.dest)
        if short_filenames:
            alt_mod_flag = '_'+str(copies_count+1)
            dir_path = os.path.split(dest[0])
            self.alt_dest = os.path.join(dir_path[0],
                                         dir_path[1][:(8-len(alt_mod_flag))]+alt_mod_flag+dest[1])
        elif tosec_compliant:
            if copies_count == 1:
                alt_mod_flag = '[a]'
            else:
                alt_mod_flag = '[a' + str(copies_count) + ']'
            self.alt_dest = dest[0] + alt_mod_flag + dest[1]
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
        if '[b]' in self.mod_flags:
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
        filename = os.path.splitext(os.path.basename(path).replace('(demo)', ''))[0]
        matches = re.findall(TOSEC_REGEX, filename)
        game_name = re.sub(TOSEC_REGEX, '', filename).strip()
        if not self.game:
            self.game = Game(game_name)
        else:
            self.game.name = game_name
        if len(matches)==0:
            return
        self.game.setYear(matches[0])
        if len(matches)==1:
            return
        self.game.setPublisher(matches[1])
        self.game.setGenreFromFilePath(path)
        self.release = GameRelease(game=self.game)
        self.game.addRelease(self.release)
        self.game.addFile(self)
        self.getParamsFromTOSECPath(path)

    def getParamsFromTOSECPath(self, tosec_path):
        self.tosec_path = tosec_path
        filename = os.path.splitext(os.path.basename(tosec_path).replace('(demo)', ''))[0]
        # self.setContentDesc(filename)
        self.setMachineType(filename)
        matches = re.findall(TOSEC_REGEX, filename)
        for each in matches[2:]:
            if len(re.findall('^a[0-9]?[0-9]?$', each)):
                continue
            elif len(re.findall('^M[0-9]$', each)):
                self.setLanguage(each)
            elif len(re.findall('^[0-9\-]+K?$', each)):
                self.setMachineType(each)
            elif len(each)==2 and each.isalpha() and each!='cr':
                self.setLanguage(each)
            elif 'Side' in each:
                self.setSide(each)
            elif 'Part' in each or 'Disk' in each or 'Tape' in each:
                self.setPart(each)
            elif each and each[0].lower() in ['m', 'h', 'c', 'f', 'b', 'o', 't']:
                self.mod_flags += '[%s]' % each
            elif each not in self.notes and \
                self.machine_type not in each:
                self.notes += '[%s]' % each
        if '(demo' in tosec_path.lower():
            self.is_demo = 1

    def setContentDesc(self, filename):
        if self.game and self.game.wos_id:
            game_name = filename.split('(')[0].strip()
            aliases = sorted(self.game.getAliases(), key=len, reverse=True)
            for alias in aliases:
                if len(game_name)<=len(alias):
                    break
                elif alias in game_name:
                    self.content_desc = game_name.split(alias)[-1]
                    break

    def setMachineType(self, filename):
        if not filename:
            return
        if '128' in filename and '48' in filename:
            self.machine_type = '48-128K'
        elif '128' in filename:
            self.machine_type = '128K'
        elif '48' in filename:
            self.machine_type = '48K'
        elif '16' in filename:
            self.machine_type = '16K'


    def getMachineType(self):
        if self.machine_type:
            return self.machine_type
        else:
            return self.game.machine_type

    def setLanguage(self, language):
        self.language = language.lower() if language.isalpha() else language.upper()

    def setPart(self, part):
        part = part.split(' ')
        for i, word in enumerate(part):
            if (word in ['Part', 'Disk', 'Tape']) and \
                len(part)>i+1 and \
                part[i+1][0].isdigit():
                self.part = int(part[i+1][0])

    def getPart(self):
        if not self.part:
            return ''
        label = 'Disk' if self.format in ('dsk', 'trd') else 'Part'
        if self.game.parts>1:
            return  '%s %d of %d' % (label, self.part, self.game.parts)
        else:
            return '%s %d' % (label, self.part)
        # if self.format in ['trd', 'dsk']:
        #     return 'Disk %d' % self.part
        # else:
        #     return 'Part %d' % self.part

    def getLanguage(self):
        if self.language:
            return self.language
        # elif self.release:
        #     return self.release.getLanguage()
        else:
            return self.game.getLanguage()

    def getTOSECName(self, game_name_length=MAX_GAME_NAME_LENGTH):
        output_name = self.getOutputName(game_name_length=game_name_length)
        return output_name

        # basename = self.getGameName(game_name_length=game_name_length)
        # params = []
        # params.append('('+self.getYear()+')')
        # params.append('('+self.getPublisher(restrict_length=game_name_length<MAX_GAME_NAME_LENGTH)+')')
        # language = self.getLanguage()
        # if language!='en':
        #     params.append('('+language+')')
        # if self.part:
        #     label = 'Disk' if self.format in ('dsk', 'trd') else 'Part'
        #     if self.game.parts>1:
        #         params.append('(%s %d of %d)' % (label, self.part, self.game.parts))
        #     else:
        #         params.append('(%s %d)' % (label, self.part))
        # if self.side:
        #     params.append('(%s)' % self.getSide())
        # if self.machine_type and self.machine_type!='48K':
        #     params.append('[%s]' % self.machine_type)
        # if self.mod_flags:
        #     params.append(self.mod_flags)
        # tosec_name = basename+' '+''.join(params)+'.'+self.format
        # tosec_name = filepath_regex.sub('', tosec_name.replace('/', '-').replace(':', ' -')).strip()
        # return tosec_name

    def getOutputName(self, structure=TOSEC_COMPLIANT_FILENAME_STRUCTURE,
                      game_name_length=MAX_GAME_NAME_LENGTH):
        if not structure.endswith('.{Format}'):
            structure += '.{Format}'
        kwargs = self.getOutputPathFormatKwargs(game_name_length=game_name_length,
                                                for_filename=True)
        output_name = structure.format(**kwargs)
        if structure==TOSEC_COMPLIANT_FILENAME_STRUCTURE:
            output_name = output_name.replace('(%s)' % DEFAULT_GAME_LANGUAGE, '')
            output_name = output_name.replace('[%s]' % DEFAULT_MACHINE_TYPE, '')
        output_name = output_name.replace('()', '').replace('[]', '')
        output_name = filepath_regex.sub('', output_name.replace('/', '-').replace(':', ' -')).strip()
        return output_name

    def setSide(self, side):
        if 'Side A' in side or 'Side 1' in side:
            self.side = SIDE_A
        elif 'Side B' in side or 'Side 2' in side:
            self.side = SIDE_B

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

    def getFormat(self, path):
        filename = os.path.basename(path)
        format = filename.replace('.zip','').split('.')[-1].lower()
        if format in GAME_EXTENSIONS:
            return format
        else:
            format = os.path.split(os.path.dirname(path))[-1].replace('[', '').replace(']', '').lower()
            if format in GAME_EXTENSIONS:
                return format

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
        return self.crc32

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
                            self.crc32 = hex(zf.getinfo(zfname).CRC)[2:]
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
            'Genre':self.getGenre(),
            'Year':self.getYear(),
            'Letter':getWosSubfolder(game_name),
            'MachineType':self.getMachineType(),
            'Publisher':publisher,
            'MaxPlayers':self.getMaxPlayers(),
            'GameName':game_name,
            'Language':self.getLanguage(),
            'Format':self.format,
            'Side':self.getSide(),
            'Part':self.getPart(),
            'ModFlags':self.mod_flags,
            'ZXDB_ID':self.game.getWosID(),
            'Notes':self.notes
        }


    def getGenre(self):
        if self.game.genre:
            return self.game.getGenre()
        else:
            return 'Unknown'
        return 'Unknown'


    def getGameName(self, game_name_length=MAX_GAME_NAME_LENGTH,
                    for_filename=False):
        game_name = self.release.aliases[0] if self.release else self.game.name
        # game_name = putPrefixToEnd(game_name)
        game_name = filepath_regex.sub('', game_name.replace('/', '-').replace(':', ' -')).strip()
        # game_name = game_name[:MAX_GAME_NAME_LENGTH]
        while game_name.endswith('.'):
            game_name = game_name[:-1]
        while len(game_name)>game_name_length:
            game_name = [x for x in game_name.split(' ') if x][:-1]
            game_name = ' '.join(game_name)
        game_name = [x for x in game_name.split(' ') if x]
        while len(game_name[-1])<2 and \
                not game_name[-1][-1].isalnum():
            game_name = ' '.join(game_name[:-1])
            game_name = [x for x in game_name.split(' ') if x]
        game_name = ' '.join(game_name).strip()
        if for_filename:
            if self.content_desc:
                game_name += ' '+self.content_desc
            if self.is_demo:
                game_name += ' (demo)'
        return game_name.strip()

    def getYear(self):
        if self.release:
            return self.release.getYear()
        else:
            return self.game.getYear()

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
        if self.game.multiplayer_type:
            result += ' (%s)' % self.game.getMultiplayerType()
        return result

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

    def getDestPath(self, camel_case=False):
        dest = self.alt_dest if self.alt_dest else self.dest
        if camel_case:
            dest = ''.join([x[0].upper() + x[1:] for x in dest.split(' ') if x])
        return dest

    def getBundleName(self):
        bundle_name = ''.join([x for x in self.getGameName() if x.isalnum()])[:3].lower()
        return bundle_name

    def setBundle(self, bundle_name):
        dest = self.getDestPath()
        dest_dir, dest_filename = os.path.split(dest)
        dest = os.path.join(dest_dir, bundle_name, dest_filename)
        self.alt_dest = dest

    def getAbsoluteDestPath(self, camel_case=False):
        return os.path.abspath(self.getDestPath(camel_case=False))

    # def getLocalFile(self):
    #     with open(self.getLocalPath()) as file:
    #         return file

    def savePokesLocally(self):
        path = self.getLocalPath()