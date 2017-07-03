from classes.game import Game, publisher_regex
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
    country=None
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


    def __init__(self, release_seq=0, year=None, publisher=None, country=None, game=Game(), aliases=[]):
        self.release_seq = release_seq
        self.year = year
        self.setPublisher(publisher)
        self.country = country
        self.game = game
        self.files = []
        self.aliases = aliases if aliases else []
        # self.loading_screen_gif_filepath = game.loading_screen_gif_filepath
        # self.loading_screen_scr_filepath = game.loading_screen_scr_filepath
        # self.ingame_screen_gif_filepath = game.ingame_screen_gif_filepath
        # self.ingame_screen_scr_filepath = game.ingame_screen_scr_filepath
        # self.manual_filepath = game.manual_filepath

    def __repr__(self):
        return '<Release {}: {}, ({})({}), {} files>'.format(
            self.release_seq,
            self.getName(),
            self.year,
            self.publisher,
            len(self.files)
        )

    def getName(self, language=None):
        return '/'.join(self.aliases) if self.aliases else self.game.name
        # aliases = [x.name for x in self.aliases if x.language==language] if language else \
        #     [x.name for x in self.aliases]
        # if aliases:
        #     return '/'.join(aliases)
        # return self.game.name

    # def `rchString(self):
    #     names = self.getName().split('/')
    #     for i, name in names:
    #         for prefix in GAME_PREFIXES:
    #             if release_name.startswith(prefix + ' '):
    #                 return ''.join(filter(str.isalnum, self.getName().lower()))

    def getAllAliases(self):
        return self.aliases
        # return [x.name for x in self.aliases]+[self.game.name]

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
        publisher = publisher_regex.sub('', publisher).strip()
        self.publisher = publisher

    def addAlias(self, alias):
        if alias not in self.aliases:
            self.aliases.append(alias)
        # alias = GameAlias(alias, language)
        # if alias.name != self.name and \
        #    alias not in self.aliases:
        #     self.aliases.append(alias)

    def addFiles(self, files):
        for file in files:
            self.addFile(file)

    def addFile(self, new_file):
        for file in self.files:
            if file == new_file:
                file.tosec_path = new_file.tosec_path
                if new_file.size:
                    file.size = new_file.size
                if new_file.language:
                    file.language = new_file.language
                if new_file.machine_type:
                    file.machine_type = new_file.machine_type
                if new_file.part:
                    file.part = new_file.part
                if new_file.side:
                    file.side = new_file.side
                return
        new_file.game = self.game
        new_file.release_seq = self.release_seq
        self.files.append(new_file)

    def getInfoFromLocalFiles(self):
        extra_files = []
        for file in self.files:
            # if not file.zipped:
            #     continue
            file_path = file.getLocalPath(zipped=True)
            if not os.path.exists(file_path):
                print(file_path, 'does not exist. Cannot get MD5 hashes.')
            file.md5_zipped = hashlib.md5(open(file_path, 'rb').read()).hexdigest()
            with zipfile.ZipFile(file_path) as z:
                for zfname in z.namelist():
                    zfext = os.path.splitext(zfname)[1].lower()[1:]
                    # DEPRECATED
                    # if zfext == 'pok':
                    #     with z.open(zfname) as pok_file:
                    #         pok_file_contents = pok_file.read().decode('utf-8')
                    #         self.importPokFile(text=pok_file_contents)
                    if zfext in GAME_EXTENSIONS:
                        unzipped_file = z.read(zfname)
                        new_file_md5 = hashlib.md5(unzipped_file).hexdigest()
                        if not file.md5:
                            file.md5 = new_file_md5
                            file.wos_name = os.path.basename(zfname)
                            file.setSize(z.getinfo(zfname).file_size)
                            file.setMachineType(zfname)
                            file.setPart(zfname)
                            file.setSide(zfname)
                        else:
                            second_file = file.copy()
                            second_file.md5 = new_file_md5
                            second_file.md5_zipped = file.md5_zipped
                            second_file.setSize(z.getinfo(zfname).file_size)
                            second_file.size_zipped = file.size_zipped
                            second_file.wos_name = os.path.basename(zfname)
                            second_file.wos_zipped_name = file.wos_zipped_name
                            second_file.setMachineType(zfname)
                            second_file.setPart(zfname)
                            second_file.setSide(zfname)
                            extra_files.append(second_file)
        self.addFiles(extra_files)
        self.files = [file for file in self.files if file.md5]