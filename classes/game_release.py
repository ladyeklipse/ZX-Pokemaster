from classes.game import Game
from functions.game_name_functions import *
import re
import zipfile
import hashlib
import os
from settings import *

class GameRelease(object):

    game = None
    release_seq = 0
    year = None
    publisher=None
    country='UK'
    aliases = []
    loading_screen_gif_filepath = None
    loading_screen_scr_filepath = None
    ingame_screen_gif_filepath = None
    ingame_screen_scr_filepath = None
    manual_filepath = None
    loading_screen_gif_filesize = 0
    loading_screen_scr_filesize = 0
    ingame_screen_gif_filesize = 0
    ingame_screen_scr_filesize = 0
    manual_filesize = 0
    files = []


    def __init__(self, release_seq=0, year=None, publisher=None, country=None, game=None, aliases=[]):
        self.release_seq = release_seq
        self.game = game if game else Game()
        self.year = year if year else self.game.year
        self.setPublisher(publisher if publisher else self.game.publisher)
        self.country = country if country else 'UK'
        self.files = []
        self.aliases = []
        self.addAliases(aliases)
        if release_seq==0 and self.game.name not in self.aliases:
            self.aliases = [self.game.name]+self.aliases

    def __repr__(self):
        return '<Release {}: {}, ({})({}), {} files>'.format(
            self.release_seq,
            self.getName(),
            self.year,
            self.publisher,
            len(self.files)
        )

    def getTOSECName(self):
        name = self.game.name[:100].replace(': ', ' - ')
        filepath = name + ' (' + self.getYear() + ')(' + self.getPublisher() + ')'
        filepath = filepath_regex.sub('', filepath.replace('/', '-')).strip()
        return filepath

    def getName(self, language=None):
        return '/'.join(self.aliases) if self.aliases else self.game.name

    def getPublisher(self):
        if self.publisher:
            return self.publisher.replace('/', '-').replace('"', '')
        else:
            return self.game.getPublisher()

    def getLanguage(self):
        if self.country in ['US', 'UK', 'GB', 'AU', 'NZ']:
            return 'en'
        else:
            return self.country.lower()

    def getYear(self):
        if not self.year:
            return self.game.getYear()
        else:
            return str(self.year)

    def getAllAliases(self):
        return sorted(set(self.aliases), key=len, reverse=True)

    def getIngameScreenFilePath(self, format='scr'):
        if format=='scr':
            return self.ingame_screen_scr_filepath
        elif format=='gif':
            return self.ingame_screen_gif_filepath

    def getLoadingScreenFilePath(self, format='scr'):
        if format=='scr':
            return self.loading_screen_scr_filepath
        elif format=='gif':
            return self.loading_screen_gif_filepath

    def getManualFilePath(self):
        return self.manual_filepath

    def setPublisher(self, publisher):
        if publisher=='unknown' or not publisher:
            publisher = ''
        publisher = publisher.replace('/', '-')
        publisher = publisher_regex.sub('', publisher)
        publisher = remove_square_brackets_regex.sub('', publisher).strip()
        self.publisher = publisher

    def addAliases(self, aliases=[]):
        for alias in aliases:
            self.addAlias(alias)

    def addAlias(self, alias):
        alias = getFileSystemFriendlyName(alias)
        if alias and alias not in self.aliases:
            self.aliases.append(alias)

    def addFiles(self, files):
        for file in files:
            self.addFile(file)

    def addFile(self, new_file):
        for file in self.files:
            if file == new_file:
                file.importCredentialsFromFile(new_file)
                return
        new_file.game = self.game
        new_file.release_seq = self.release_seq
        new_file.release = self
        self.files.append(new_file)

    def getInfoFromLocalFiles(self):
        extra_files = []
        for file in self.files:
            file_path = file.getLocalPath()
            if not os.path.exists(file_path):
                print(file_path, 'does not exist. Cannot get MD5 hashes.')
                continue
            file.md5_zipped = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            with zipfile.ZipFile(file_path) as z:
                for zfname in z.namelist():
                    zfext = os.path.splitext(zfname)[1].lower()[1:]
                    if zfext in GAME_EXTENSIONS:
                        unzipped_file = z.read(zfname)
                        new_file_md5 = hashlib.md5(unzipped_file).hexdigest()
                        new_file_sha1 = hashlib.sha1(unzipped_file).hexdigest()
                        new_file_crc32 = hex(z.getinfo(zfname).CRC)[2:]
                        if file.format != zfext:
                            print('FORMAT MISMATCH:', file.wos_path, zfname)
                        if not file.md5:
                            file.md5 = new_file_md5
                            file.sha1 = new_file_sha1
                            file.crc32 = new_file_crc32
                            file.wos_name = os.path.basename(zfname)
                            file.format = zfext
                            file.is_demo = '(demo' in file_path.lower()
                            file.setSize(z.getinfo(zfname).file_size)
                            file.setMachineType(zfname)
                            file.setPart(zfname)
                            file.setSide(zfname)
                        else:
                            second_file = file.copy()
                            second_file.crc32 = new_file_crc32
                            second_file.md5 = new_file_md5
                            second_file.sha1 = new_file_sha1
                            second_file.format = zfext
                            second_file.md5_zipped = file.md5_zipped
                            second_file.is_demo = '(demo' in file_path.lower()
                            second_file.setSize(z.getinfo(zfname).file_size)
                            second_file.wos_name = os.path.basename(zfname)
                            second_file.wos_zipped_name = file.wos_zipped_name
                            second_file.setMachineType(zfname)
                            second_file.setPart(zfname)
                            second_file.setSide(zfname)
                            extra_files.append(second_file)
        self.addFiles(extra_files)
        self.files = [file for file in self.files if file.md5]