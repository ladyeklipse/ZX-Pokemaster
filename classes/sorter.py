from classes.database import *
from settings import *
import os
import stat
import shutil
import zipfile
import hashlib
import time

class Sorter():

    db = Database()
    gui = None
    input_files = []
    collected_files = []
    should_cancel = False

    def __init__(self, *args, **kwargs):
        self.input_locations = kwargs.get('input_locations', [])
        self.output_location = kwargs.get('output_location', 'sorted')
        self.formats_preference = kwargs.get('formats_preference', [])
        if not self.formats_preference:
            self.formats_preference = GAME_EXTENSIONS
        self.output_folder_structure = kwargs.get('output_folder_structure', '{Letter}')
        self.delete_original_files = kwargs.get('delete_original_files', False)
        self.files_per_folder = kwargs.get('files_per_folder')
        self.ignore_alternate = kwargs.get('ignore_alternate', True)
        self.ignore_alternate_formats = kwargs.get('ignore_alternate_formats', False)
        self.ignore_rereleases = kwargs.get('ignore_rereleases', False)
        self.ignore_hacks = kwargs.get('ignore_hacks', False)
        self.ignore_bad_dumps = kwargs.get('ignore_bad_dumps', True)
        self.place_pok_files_in_pokes_subfolders = kwargs.get('place_pok_files_in_pokes_subfolders', True)
        self.gui = kwargs.get('gui', None)
        if kwargs.get('cache', True):
            if self.gui:
                self.gui.updateProgressBar(0, 0, 'Loading database cache...')
            self.db.loadCache()


    def sortFiles(self):
        if not self.input_files:
            self.input_files = self.getInputFiles()
        print('Got', len(self.input_files), 'raw input files')
        self.collected_files = self.collectFiles(self.input_files)
        print('Files collected')

        if self.ignore_hacks or \
            self.ignore_alternate or \
            self.ignore_rereleases:
            self.collected_files = self.filterCollectedFiles()
            print('Files filtered')
        print('Redistributing...')
        self.redistributeFiles()

    def collectFiles(self, input_files):
        if self.gui:
            self.gui.updateProgressBar(0, len(input_files), 'Examining files...')
        collected_files = {}
        for i, file_path in enumerate(input_files):
            if self.should_cancel:
                break
            if i % 100 == 0:
                print('Examined', i, 'files of', len(input_files))
                if self.gui:
                    self.gui.updateProgressBar(i)
            game_files = self.getGameFilesFromInputPath(file_path)
            if not game_files:
                print('Nothing found for', file_path)
                continue
            for game_file in game_files:
                wos_id = game_file.game.wos_id
                if wos_id not in collected_files.keys():
                    collected_files[game_file.game.wos_id] = []
                else:
                    if game_file in collected_files[game_file.game.wos_id]:
                        continue
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
            if self.should_cancel:
                break
            if self.gui:
                self.gui.updateProgressBar(0, 0, 'Traversing '+location)
            for root, dirs, files in os.walk(location):
                for file in files:
                    if file[-3:].lower() in formats:
                        input_files.append(os.path.join(root, file))
        return input_files

    def getGameFilesFromInputPath(self, file_path):
        ext = os.path.splitext(file_path)[1][1:].lower()
        if ext in self.formats_preference:
            game_file = GameFile(file_path)
            game = self.db.getGameByFile(game_file)
            if game:
                game_file.importCredentials(game)
            game_file.src = file_path
            game_file.dest = self.getDestination(game_file)
            return [game_file]
        elif ext=='zip':
            if os.path.getsize(file_path)>MAX_ZIP_FILE_SIZE:
                return []
            game_files = []
            with zipfile.ZipFile(file_path) as zf:
                for zfname in zf.namelist():
                    zfext = os.path.splitext(zfname)[1][1:].lower()
                    if zfext not in self.formats_preference:
                        continue
                    game_file = GameFile(file_path)
                    game_file.format = zfext
                    game_file.crc32 = hex(zf.getinfo(zfname).CRC)[2:]
                    unzipped_file = zf.read(zfname)
                    unzipped_file_md5 = hashlib.md5(unzipped_file).hexdigest()
                    game_file.md5 = unzipped_file_md5
                    game = self.db.getGameByFileMD5(unzipped_file_md5)
                    if game:
                        game_file = game.findFileByMD5(unzipped_file_md5)
                        game_file.release = game.releases[game_file.release_seq]
                        game_file.tosec_path = None
                    game_file.src = file_path
                    game_file.dest = self.getDestination(game_file)
                    game_files.append(game_file)
            return game_files

    def getDestination(self, game_file):
        subfolders_dict = game_file.getOutputPathFormatKwargs()
        dest = self.output_folder_structure.format(**subfolders_dict)
        dest = os.path.join(self.output_location, dest, game_file.getTOSECName())
        return dest

    def filterCollectedFiles(self):
        for game_wos_id, files in self.collected_files.items():
            min_release = min([file.getReleaseSeq() for file in files])
            for i, file in enumerate(files):
                if self.ignore_rereleases and file.getReleaseSeq()>min_release:
                    self.collected_files[game_wos_id][i] = None
                if self.ignore_alternate and file.isAlternate():
                    self.collected_files[game_wos_id][i] = None
                if self.ignore_hacks and file.isHack():
                    self.collected_files[game_wos_id][i] = None
                if self.ignore_bad_dumps and file.isBadDump():
                    self.collected_files[game_wos_id][i] = None
            files = [file for file in files if file]

            if self.ignore_alternate_formats and files and game_wos_id:
                self.collected_files[game_wos_id] = self.filterOutAlternateFormats(files)
        return self.collected_files

    def filterOutAlternateFormats(self, files):
        equals_found_flag = True
        while equals_found_flag == True:
            equals_found_flag = False
            best_candidate = None
            equals = []
            for file in files:
                equals = file.getEquals(files)
                if len(equals)==1:
                    continue
                elif equals==0:
                    print(files)
                    raise Exception('Equals not found!')
                else:
                    equals_found_flag = True
                    best_candidate = self.getBestCandidate(equals)
                    break
            if best_candidate:
                for file in equals:
                    if file in files and file!=best_candidate:
                        files.remove(file)
        return files

    def getBestCandidate(self, files):
        files = sorted(files, key=lambda file: file.getSortIndex(self.formats_preference))
        return files[0]

    def redistributeFiles(self):
        if self.gui:
            self.gui.updateProgressBar(0, self.getCollectedFilesCount(), 'Redistributing files...')
        files_array = self.getFilesArray(self.collected_files)
        for i, file in enumerate(files_array):
            if self.should_cancel:
                break
            if i % 100 == 0:
                print('Redistributed files:', i-1, 'of', len(files_array))
                if self.gui:
                    self.gui.updateProgressBar(i)
            try:
                os.makedirs(os.path.dirname(file.dest), exist_ok=True)
            except OSError:
                print('Could not make dires:', file.dest, 'for', file.src)
                print(traceback.format_exc())
                continue
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

    def getFilesArray(self, collected_files):
        files_array = []
        for files in collected_files.values():
            for file in files:
                if not file:
                    continue
                else:
                    files_array.append(file)
        return files_array

    def getInputFilesCount(self):
        return len(self.input_files)

    def getCollectedFilesCount(self):
        return sum([len(x) for x in self.collected_files.values()])

    def unpackFile(self, game_file):
        with zipfile.ZipFile(game_file.src) as zf:
            for zfname in zf.namelist():
                crc32 = hex(zf.getinfo(zfname).CRC)[2:]
                if crc32 == game_file.crc32:
                    data = zf.read(zfname)
                    try:
                        with open(game_file.getDestination(), 'wb') as output:
                            output.write(data)
                    except PermissionError:
                        os.chmod(game_file.getDestination(), stat.S_IWRITE)
                        with open(game_file.getDestination(), 'wb') as output:
                            output.write(data)
                    break

    def cancel(self):
        self.should_cancel = True