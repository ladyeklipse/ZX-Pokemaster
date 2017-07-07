from classes.database import *
from settings import *
import os
import shutil
import zipfile

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
        self.formats_preference = kwargs.get('formats_preference', GAME_EXTENSIONS)
        self.output_folder_structure = kwargs.get('output_folder_structure', '{Genre}/{Year}/{Letter}')
        self.delete_original_files = kwargs.get('delete_original_files', False)
        self.files_per_folder = kwargs.get('files_per_folder')
        self.ignore_hacks = kwargs.get('ignore_hacks', False)
        self.ignore_alternate = kwargs.get('ignore_alternate', True)
        self.ignore_rereleases = kwargs.get('ignore_rereleases', False)
        self.place_pok_files_in_pokes_subfolders = kwargs.get('place_pok_files_in_pokes_subfolders', True)
        if kwargs.get('cache', True):
            self.db.loadCache()

    def sortFiles(self, input_files=[]):
        if not input_files:
            input_files = self.getInputFiles()
        print('Got', len(input_files), 'files')
        src_dest_dict = {}
        collected_files = self.collectFiles(input_files)
        if self.ignore_hacks or \
            self.ignore_alternate or \
            self.ignore_rereleases:
            collected_files = self.filterCollectedFiles(collected_files)
        self.redistributeFiles(collected_files)

    def collectFiles(self, input_files):
        collected_files = {}
        for file_path in input_files:
            game_file = self.getGameFileFromInputPath(file_path)
            wos_id = game_file.game.wos_id
            if wos_id not in collected_files.keys():
                collected_files[game_file.game.wos_id] = []
            else:
                copies_count = game_file.countAlternateDumpsIn(collected_files[wos_id])
                game_file.addAlternateModFlag(copies_count)
            collected_files[game_file.game.wos_id].append(game_file)
        return collected_files

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
        game = self.db.getGameByFile(game_file)
        if game:
            game_file.game = game
            game_file.release = game.findReleaseByFile(game_file)
        game_file.src = file_path
        game_file.dest = self.getDestination(game_file)
        return game_file

    def getDestination(self, game_file):
        subfolders_dict = game_file.getOutputPathFormatKwargs()
        dest = self.output_folder_structure.format(**subfolders_dict)
        dest = os.path.join(self.output_location, dest, game_file.getFullTOSECName())
        return dest

    def filterCollectedFiles(self, collected_files):
        for game_wos_id, files in collected_files.items():
            for i, file in enumerate(files):
                if self.ignore_rereleases and file.getReleaseSeq():
                    collected_files[game_wos_id][i] = None
                if self.ignore_alternate and file.isAlternate():
                    collected_files[game_wos_id][i] = None
                if self.ignore_hacks and file.mod_flags:
                    collected_files[game_wos_id][i] = None
        return collected_files

    def redistributeFiles(self, collected_files):
        for files in collected_files.values():
            for file in files:
                if not file:
                    continue
                os.makedirs(os.path.dirname(file.dest), exist_ok=True)
                if file.src.lower().endswith('zip'):
                    self.unpackFile(file)
                else:
                    if self.delete_original_files:
                        shutil.move(file.src, file.dest)
                    else:
                        shutil.copy(file.src, file.dest)
                if file.game.cheats:
                    pok_file_path = os.path.dirname(file.dest)
                    pok_file_name = os.path.splitext(os.path.basename(file.dest))[0]+'.pok'
                    if self.place_pok_files_in_pokes_subfolders:
                        pok_file_path = os.path.join(pok_file_path, 'POKES')
                        os.makedirs(pok_file_path, exist_ok=True)
                    pok_file_path = os.path.join(pok_file_path, pok_file_name)
                    file.game.exportPokFile(pok_file_path)

    def unpackFile(self, game_file):
        with zipfile.ZipFile(game_file.src) as zf:
            for zfname in zf.namelist():
                crc32 = hex(zf.getinfo(zfname).CRC)[2:]
                if crc32 == game_file.crc32:
                    data = zf.read(zfname)
                    with open(game_file.dest, 'wb') as output:
                        output.write(data)
                    break
