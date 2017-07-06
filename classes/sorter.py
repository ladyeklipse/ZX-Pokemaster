from classes.database import *
from settings import *
import os
import shutil

OUTPUT_FOLDER_STRUCTURES = [
    '{Genre}/{Year}/{Letter}',
    '{Genre}/{Year}/{Letter}/{Name}',
    '{Publisher}/{Year}/{Name}',
    '{Genre}/{Publisher}/{Year}',
    '{Letter}/{Name}/{Publisher}',
    '{MachineType}/{NumberOfPlayers}/{Genre}'
]
class Sorter():

    db = Database()

    def __init__(self, *args, **kwargs):
        self.input_locations = kwargs.get('input_locations', [])
        self.output_location = kwargs.get('output_location', 'sorted')
        self.formats_preference = kwargs.get('formats_preference', ['tap', 'z80', 'dsk', 'trd', 'tzx'])
        self.output_folder_structure = kwargs.get('output_folder_structure', '{Genre}/{Year}/{Letter}')
        self.delete_original_files = kwargs.get('delete_original_files', False)
        self.files_per_folder = kwargs.get('files_per_folder')
        self.ignore_cracked = kwargs.get('ignore_cracked', False)
        self.ignore_alternate = kwargs.get('ignore_alternate', True)
        self.ignore_rereleases = kwargs.get('ignore_rereleases', False)
        if kwargs.get('cache', True):
            self.db.loadCache()

    def sortFiles(self, input_files=[]):
        if not input_files:
            input_files = self.getInputFiles()
        print('Got', len(input_files), 'files')
        src_dest_dict = {}
        files_collected = self.collectFiles(input_files)
        if self.ignore_cracked or \
            self.ignore_alternate or \
            self.ignore_rereleases:
            files_collected = self.filterCollectedFiles(files_collected)
        self.redistributeFiles(files_collected)

    def collectFiles(self, input_files):
        files_collected = {}
        for file_path in input_files:
            game_file = self.getGameFileFromInputPath(file_path)
            if game_file.game.wos_id not in files_collected.keys():
                files_collected[game_file.game.wos_id] = []
            files_collected[game_file.game.wos_id].append(game_file)
        return files_collected

    def getInputFiles(self, input_locations=None):
        if not input_locations:
            input_locations = self.input_locations
        input_files = []
        formats = ['zip']+GAME_EXTENSIONS
        for location in input_locations:
            for root, dirs, files in os.walk(location):
                for file in files:
                    if file[-3:] in formats:
                        input_files.append(os.path.join(root, file))
        return input_files

    def getGameFileFromInputPath(self, file_path):
        game_file = GameFile(file_path)
        game_file.src = file_path
        game_file.dest = self.getDestination(game_file)
        return game_file

    def getDestination(self, game_file):
        subfolders_dict = game_file.getSubfoldersDict()
        dest = self.output_folder_structure.format(**subfolders_dict)
        return dest

    def filterCollectedFiles(self, files_collected):
        return files_collected

    def redistributeFiles(self, files_collected):
        for files in files_collected.values():
            for file in files:
                os.makedirs(file.dest, exist_ok=True)
                if self.delete_original_files:
                    shutil.move(file.src, file.dest)
                else:
                    shutil.copy(file.src, file.dest)
