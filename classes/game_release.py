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
    year = ''
    publisher = ''
    country = ''
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
    modded_by = ''

    def __init__(self, release_seq=0, year=None, publisher=None, country='', game=None, aliases=[]):
        self.release_seq = release_seq
        self.game = game if game else Game()
        self.year = year if year else self.game.year
        self.setPublisher(publisher if publisher else self.game.publisher)
        if country == 'UK':
            country = 'GB'
        self.country = country
        if publisher == 'Timex Portugal':
            self.country = 'PT'
        self.files = []
        self.aliases = []
        self.addAliases(aliases)
        if release_seq==0:
            self.addAlias(self.game.name)

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
        return '/'.join(self.getAllAliases()) if self.aliases else self.game.name

    def getPublisher(self):
        if self.publisher:
            return self.publisher.replace('/', '-').replace('"', '')
        else:
            return self.game.getPublisher()

    def setYear(self, year):
        self.year = year

    def getYear(self):
        if not self.year:
            return self.game.getYear()
        else:
            return str(self.year)

    def getAllAliases(self):
        aliases = sorted(set(self.aliases), key=lambda x: (len(x), -self.aliases.index(x)), reverse=True)
        for i, alias in enumerate(aliases):
            if self.game.name in alias:
                return [aliases.pop(i)]+aliases
        return aliases

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
        if alias:
            alias = getFileSystemFriendlyName(alias)
            if alias not in self.aliases:
                self.aliases.append(alias)

    def addFiles(self, files):
        for file in files:
            self.addFile(file)

    def addFile(self, new_file):
        for file in self.files:
            if file == new_file:
                file.importCredentialsFromFile(new_file)
                return
        if new_file.game and 'Your Sinclair - Issue' not in new_file.game.name:
            add_aka = True
            for alias in self.getAllAliases():
                ss_newfile = getSearchStringFromGameName(new_file.game.name)
                ss_self = getSearchStringFromGameName(alias)
                if ss_newfile==ss_self or ss_self in ss_newfile or ss_newfile in ss_self:
                    add_aka = False
                    break
                elif new_file.content_desc and \
                    new_file.content_desc.replace('ALT ','') in new_file.game.name:
                    add_aka = False
                    break
            if add_aka:
                aka = '[aka {}]'.format(new_file.game.name)
                if aka not in new_file.notes:
                    new_file.notes += aka
        new_file.game = self.game
        new_file.release_seq = self.release_seq
        new_file.release = self
        self.files.append(new_file)

    def removeFile(self, file_exclusion_key):
        self.files = [file for file in self.files if \
                file.wos_name+'|'+file.wos_path!=file_exclusion_key]


    def importInfoFromGameFile(self, game_file):
        game_file_year = game_file.getYear()
        if (not self.year and game_file_year!='19xx') or \
            (self.getYear()[:4] == game_file.getYear()[:4] and len(game_file_year)>4):
            self.year = game_file.getYear()
            self.modded_by = game_file.md5
        if self.getPublisher()=='-' and game_file.getPublisher()!='-':
            self.publisher = game_file.getPublisher()
            self.modded_by = game_file.md5
        if not self.country and game_file.getCountry():
            self.country = game_file.getCountry()
            self.modded_by = game_file.md5

    def getInfoFromLocalFiles(self):
        extra_files = []
        for file in self.files:
            file_path = file.getLocalPath()
            if not os.path.exists(file_path):
                print(file_path, 'does not exist. Cannot get MD5 hashes.')
                continue
            try:
                z = zipfile.ZipFile(file_path)
            except zipfile.BadZipFile:
                print('Bad zip file:', file_path)
                continue
            for zfname in z.namelist():
                zfext = os.path.splitext(zfname)[1].lower()[1:]
                if zfext in GAME_EXTENSIONS:
                    unzipped_file = z.read(zfname)
                    new_file_md5 = hashlib.md5(unzipped_file).hexdigest()
                    new_file_sha1 = hashlib.sha1(unzipped_file).hexdigest()
                    new_file_crc32 = hex(z.getinfo(zfname).CRC)[2:].zfill(8)
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
                        file.setLanguageFromWosName()
                    else:
                        second_file = file.copy()
                        second_file.crc32 = new_file_crc32
                        second_file.md5 = new_file_md5
                        second_file.sha1 = new_file_sha1
                        second_file.format = zfext
                        second_file.is_demo = '(demo' in file_path.lower()
                        second_file.setSize(z.getinfo(zfname).file_size)
                        second_file.wos_name = os.path.basename(zfname)
                        second_file.wos_zipped_name = file.wos_zipped_name
                        second_file.setMachineType(zfname)
                        second_file.setPart(zfname)
                        second_file.setSide(zfname)
                        second_file.setLanguageFromWosName()
                        second_file.release = file.release
                        extra_files.append(second_file)
            z.close()
        self.addFiles(extra_files)
        self.files = [file for file in self.files if file.md5]