from classes.game import Game
import requests
import os
import zipfile
import hashlib
from settings import *


class GameFile(object):

    game = None
    wos_name = ''
    md5 = ''
    format = ''
    size = 0

    def __init__(self, wos_name, size=0, game=Game()):
        file_name = os.path.basename(wos_name)
        if file_name.endswith('.zip'):
            file_name = file_name[:-4]
        self.wos_name = file_name
        self.size = size
        self.format = self.getFormat()
        self.game = game

    def __repr__(self):
        return '<GameFile: '+self.wos_name+' size:'+str(self.size)+'>'

    def getInstructionsUrl(self):
        return self.instructions_url

    def getFormat(self):
        return self.wos_name.replace('.zip','').split('.')[-1]

    def getMD5(self):
        local_path = self.getLocalPath()
        print(os.path.abspath(local_path))
        file_handle = self.getFileHandle(local_path)
        return hashlib.md5(file_handle).hexdigest()

    def getFileHandle(self, local_path):
        with zipfile.ZipFile(local_path, 'r') as zf:
            for zfname in zf.namelist():
                zfname_ext = zfname.split('.')[-1].lower()
                if zfname_ext == self.format:
                    return zf.read(zfname)

    def getLocalPath(self):
        first_letter = self.wos_name[0].upper()
        local_path = os.path.join(LOCAL_GAME_FILES_DIRECTORY, first_letter, self.wos_name)
        return local_path

    def getWosPath(self):
        first_letter = self.wos_name[0].lower()
        wos_path = os.path.join(WOS_GAME_FILES_DIRECTORY, first_letter, self.wos_name+'.zip')
        return wos_path

    def getLocalFile(self):
        pass

    def getRemoteFile(self):
        pass

    def unzip(self):
        zf = self.getLocalFile()
