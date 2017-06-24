from classes.game import Game, getWosSubfolder
import requests
import os
import zipfile
import hashlib
from settings import *
import re
TOSEC_REGEX = re.compile('[\(\[](.*?)[\)\]]|.zip|'+'|'.join(['.'+x for x in GAME_EXTENSIONS]))

class GameFile(object):

    game = None
    wos_name = ''
    wos_zipped_name = ''
    tosec_name = ''
    machine_type = ''
    language = ''
    part = 0
    side = 0
    # zipped = False
    format = ''
    size = 0
    size_zipped = 0
    md5 = ''
    md5_zipped = ''
    wos_path = ''

    def __init__(self, path='', size=0, game=Game()):
        filename = os.path.basename(path)
        # if filename.endswith('.zip'):
        #     filename = filename[:-4]
        self.path = path
        self.setSize(size)
        self.format = self.getFormat(path)
        self.game = game
        self.setMachineType(filename)
        if game.wos_id:
            if filename.endswith('.zip'):
                self.wos_zipped_name = filename
                self.wos_path = path
            else:
                self.wos_name = filename
        else:
            self.getGameFromFileName()
        if type(size)==str:
            size = int(size.replace(',',''))

    def __repr__(self):
        return '<GameFile: '+self.path+' md5:'+self.md5+'>'

    def __eq__(self, other):
        if self.wos_name and \
            self.wos_name == other.wos_name and \
            self.size == other.size and \
            self.format == other.format:
            return True
        if self.md5 and self.md5==other.md5:
            return True
        return False

    def copy(self):
        new = GameFile(self.path, self.size, self.game)
        return new

    def getFileName(self):
        return self.tosec_name if self.tosec_name else os.path.basename(self.path)

    def getGameFromFileName(self):
        filename = os.path.basename(self.path)
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
        for each in matches[2:]:
            if len(each)==2:
                self.setLanguage(each)
            elif 'Side' in each:
                self.setSide(each)
            elif 'Part' in each or 'Disk' in each:
                self.setPart(each)

    def setMachineType(self, filename):
        if not filename:
            return
        if '128' in filename and '48' in filename:
            self.machine_type = '48/128K'
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
        self.language = language

    def setPart(self, part):
        part = part.split(' ')
        for i, word in enumerate(part):
            if (word in ['Part', 'Disk']) and \
                len(part)>i and \
                part[i+1][0].isdigit():
                self.part = int(part[i+1][0])

    def getOutputPathFormatKwargs(self):
        return {
            'Genre':self.game.genre.replace(':', ''),
            'Publisher':self.game.getPublisher(),
            'Machine type':self.getMachineType(),
            'Language':self.getLanguage(),
            'Letter':getWosSubfolder(self.wos_name)
        }

    def getLanguage(self):
        return self.language if self.language else self.game.language

    def getFullTOSECName(self, zipped=False):
        if self.tosec_name:
            return self.tosec_name
        game = self.game
        basename =  game.name
        params = []
        params.append('('+game.getYear()+')')
        params.append('('+game.getPublisher()+')')
        if self.language:
            params.append('('+self.language+')')
        if self.side:
            params.append('(Side '+self.getSide()+')')
        elif self.part:
            params.append('(Part '+str(self.part)+' of '+str(game.parts)+')')
        # if self.tosec_info:
        #     params.append(self.tosec_info)
        ext = 'zip' if zipped else self.format
        return basename+' '+''.join(params)+'.'+ext

    def setSide(self, side):
        if 'Side A' in side or 'Side 1' in side:
            self.side = SIDE_A
        elif 'Side B' in side or 'Side 2' in side:
            self.side = SIDE_B

    def getSide(self):
        if self.side == SIDE_A:
            return 'A'
        elif self.side == SIDE_B:
            return 'B'

    def setSize(self, size, zipped=False):
        if type(size)==str:
            size = int(size.replace(',',''))
        if zipped:
            self.size_zipped = size
        else:
            self.size = size

    def getSize(self):
        return '{:,}'.format(self.size)

    def getFormat(self, path):
        filename = os.path.basename(path)
        format = filename.replace('.zip','').split('.')[-1].lower()
        if format in GAME_EXTENSIONS:
            return format
        else:
            format = os.path.dirname(path).split('/')[-1].replace('[', '').replace(']', '').lower()
            if format in GAME_EXTENSIONS:
                return format

    def getMD5(self, zipped=False):
        if zipped and self.md5_zipped:
            return self.md5_zipped
        elif not zipped and self.md5:
            return self.md5

        local_path = self.getLocalPath(zipped=zipped)
        if os.path.exists(local_path):
            file_handle = self.getFileHandle(local_path, zipped=zipped)
            md5 = hashlib.md5(file_handle).hexdigest()
            if zipped:
                self.md5_zipped = md5
            else:
                self.md5 = md5
            return md5

    def getFileHandle(self, local_path, zipped):
        if local_path.endswith('.zip') and not zipped:
            with zipfile.ZipFile(local_path, 'r') as zf:
                for zfname in zf.namelist():
                    zfname_ext = zfname.split('.')[-1].lower()
                    if zfname_ext == self.format:
                        if not self.size:
                            self.setSize(zf.getinfo(zfname).file_size)
                        return zf.read(zfname)
        else:
            return open(local_path, 'rb').read()

    def getWosPath(self, wos_mirror_root = WOS_SITE_ROOT):
        return wos_mirror_root+self.path
        # return self.wos_path
        # wos_folder = WOS_TRDOS_GAME_FILES_DIRECTORY if self.format=='trd' \
        #     else WOS_GAME_FILES_DIRECTORY
        # return '/'.join((wos_mirror_root,
        #                  wos_folder,
        #         getWosSubfolder(self.wos_name),
        #         self.wos_name+'.zip'))
        # subfolder = getWosSubfolder(self.wos_name[0])
        # wos_path = os.path.join(WOS_GAME_FILES_DIRECTORY, subfolder, self.wos_name+'.zip')
        # return wos_path

    def getLocalPath(self, zipped=False):
        return self.getWosPath(LOCAL_FTP_ROOT)
        # if zipped and self.wos_zipped_name:
        #     subfolder = getWosSubfolder(self.wos_zipped_name)
        #     local_path = os.path.join(LOCAL_GAME_FILES_DIRECTORY, subfolder, self.wos_zipped_name)
        #     return local_path
        # elif not zipped and self.wos_name:
        #     subfolder = getWosSubfolder(self.wos_name)
        #     local_path = os.path.join(LOCAL_GAME_FILES_DIRECTORY, subfolder, self.wos_name)
        #     return local_path
        # else:
        #     return self.path

    def getLocalFile(self):
        return open(self.getLocalPath())

    # def getRemoteFile(self):
    #     wos_path = self.getWosPath()
    #     return wos_path

    # def unzip(self):
    #     try:
    #         zf = self.getLocalFile()
    #     except FileNotFoundError:
    #         zf = self.getRemoteFile()

    def savePokesLocally(self):
        path = self.getLocalPath()
