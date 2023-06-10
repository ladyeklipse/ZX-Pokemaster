from classes.database import *
from classes.file_bundler import *
from classes.archive_handler import *
from functions.game_name_functions import *
from settings import *
import os
import stat
import shutil
import zipfile
import hashlib
import json
import traceback
import glob
import time
from copy import copy
import operator

db = Database()

class Sorter():

    def __init__(self, *args, **kwargs):
        self.backup_location_name = None
        self.log_path = ''
        self.gui = kwargs.get('gui', None)
        self.files_sorted = 0
        self.files_skipped = 0
        self.input_files = []
        self.collected_files = {}
        self.files_not_in_database = []
        self.should_cancel = False
        self.original_output_location = None
        self.too_long_path = None
        if not kwargs:
            kwargs = self.loadSettings()
        self.input_locations = kwargs.get('input_locations', [])
        self.traverse_subfolders= kwargs.get('traverse_subfolders', True)
        self.output_location = kwargs.get('output_location', 'sorted')
        # self.formats_preference = kwargs.get('formats_preference', GAME_EXTENSIONS) \
        #     if kwargs.get("format_filter_on") else GAME_EXTENSIONS
        self.include_only = kwargs.get('include_only', GAME_EXTENSIONS) \
            if kwargs.get("include_filter_on") else GAME_EXTENSIONS
        self.exclude = kwargs.get('exclude', []) if kwargs.get("exclude_filter_on") else []
        # print("formats:", self.formats_preference)
        print("include only:", self.include_only)
        print("exclude:", self.exclude)
        # if not self.formats_preference:
        #     self.formats_preference = GAME_EXTENSIONS
        self.languages = kwargs.get('languages', [])
        self.max_files_per_folder = kwargs.get('max_files_per_folder', None)
        self.bundle_key_length = kwargs.get('bundle_key_length', 3)
        self.output_folder_structure = kwargs.get('output_folder_structure', '')
        self.output_filename_structure = kwargs.get('output_filename_structure', TOSEC_COMPLIANT_FILENAME_STRUCTURE)
        self.include_alternate = kwargs.get('include_alternate', False)
        self.include_alternate_formats = kwargs.get('include_alternate_formats', True)
        self.include_rereleases = kwargs.get('include_rereleases', True)
        self.include_hacks = kwargs.get('include_hacks', True)
        self.include_xrated = kwargs.get('include_xrated', True)
        self.include_bad_dumps = kwargs.get('include_bad_dumps', False)
        self.include_unknown_files = kwargs.get('include_unknown_files', True)
        self.separate_unknown_files = kwargs.get('separate_unknown_files', True)
        self.retain_relative_structure = kwargs.get('retain_relative_structure', False)
        self.include_supplementary_files = kwargs.get('include_supplementary_files', False)
        self.delete_source_files = kwargs.get('delete_source_files', False)
        self.max_archive_size = int(kwargs.get('max_archive_size', 1))*1024*1024
        self.short_filenames = kwargs.get('short_filenames', False)
        self.use_camel_case = kwargs.get('use_camel_case', False)
        self.place_pok_files_in_pokes_subfolders = kwargs.get('place_pok_files_in_pokes_subfolders', True)
        if self.place_pok_files_in_pokes_subfolders and self.max_files_per_folder:
            self.max_files_per_folder -= 1
        if self.output_location in self.input_locations:
            self.original_output_location = self.output_location
            self.output_location = os.path.join(os.path.dirname(self.output_location), '%s_temp' % self.output_location)
        self.errors = ''
        if not self.checkOutputPath():
            return
        if kwargs.get('cache', True):
            if self.gui:
                self.gui.updateProgressBar(0, 0, 'Loading database cache...')
            db.loadCache()

    def loadSettings(self):
        if not os.path.exists('settings.json'):
            return {}
        with open('settings.json', 'r', encoding='utf-8') as f:
            settings = json.load(f)
        return settings

    def sortFiles(self):
        if not self.input_files:
            self.input_files = self.getInputFiles()
        print('Got', len(self.input_files), 'raw input files')
        self.collected_files = self.collectFiles(self.input_files)
        print('Files collected')
        if not self.include_hacks or \
            not self.include_alternate or \
            not self.include_rereleases or \
            self.languages:
            self.filterCollectedFiles()
        if self.max_files_per_folder:
            bundle_depth = self.getBundleDepth()
            fileBundler = FileBundler(self.max_files_per_folder, bundle_depth, self.bundle_key_length)
            fileBundler.bundleFilesInEqualFolders(self.collected_files)
        self.redistributeFiles()
        if self.delete_source_files:
            self.removeEmptyDirs()
        if self.original_output_location:
            self.renameOutputLocation()
        self.saveLog()

    def checkOutputPath(self):
        gf = GameFile('test.tap')
        gf.game.zxdb_id = 9999999
        try:
            self.getDestination(gf)
            return True
        except KeyError as e:
            key = e.args[0]
            self.errors = 'Invalid output path structure component: '+key
            return False

    def renameOutputLocation(self):
        backup_location_name = self.original_output_location+'_old'
        if os.path.exists(backup_location_name):
            i = 2
            while os.path.exists(backup_location_name+'_'+str(i)):
                i += 1
            backup_location_name = backup_location_name + '_' + str(i)
        os.rename(self.original_output_location, backup_location_name)
        os.rename(self.output_location, self.original_output_location)
        self.backup_location_name = backup_location_name
        if len(os.listdir(self.backup_location_name))==0:
            os.rmdir(self.backup_location_name)

    def getBundleDepth(self):
        self.output_folder_structure = self.output_folder_structure.replace('/', '\\')
        return len([x for x in self.output_folder_structure.split('\\') if x]) + 1

    def collectFiles(self, input_files):
        if self.gui:
            self.gui.updateProgressBar(0, len(input_files), 'Examining files...')
        collected_files = {}
        tosec_compliant = \
            self.output_filename_structure==TOSEC_COMPLIANT_FILENAME_STRUCTURE or \
            self.output_filename_structure=='{TOSECName}'
        for i, file_path in enumerate(input_files):
            if self.should_cancel:
                break
            try:
                if i % 100 == 0 and self.gui:
                    self.gui.updateProgressBar(i)
                game_files = self.getGameFilesFromInputPath(file_path)
                if not game_files:
                    # print('Nothing found for', file_path)
                    continue
                if not self.short_filenames:
                    for game_file in game_files:
                        self.shortenGameFileDestination(game_file)
                if self.too_long_path:
                    print('Path', self.too_long_path, 'is too long. Exiting prematurely.')
                    break
                for game_file in game_files:
                    game_name = game_file.getGameName(short=self.short_filenames)
                    if game_name not in collected_files.keys():
                        collected_files[game_name] = []
                    else:
                        if game_file in collected_files[game_name]:
                            existing_game_file = [x for x in collected_files[game_name] if x==game_file][0]
                            if game_file.file_in_archive and not game_file.file_is_alone_in_archive:
                                    existing_game_file.alt_files_in_archives.append(game_file.file_in_archive)
                            else:
                                existing_game_file.alt_src.append(game_file.src)
                            continue
                        if game_file.game.zxdb_id:
                            copies_count = game_file.countAlternateDumpsIn(collected_files[game_name])
                        else:
                            copies_count = game_file.countFilesWithSameDestIn(collected_files[game_name])
                        if not tosec_compliant:
                            copies_count = game_file.countFilesWithSameDestIn(collected_files[game_name])
                        game_file.addAlternateModFlag(copies_count,
                                                      tosec_compliant=tosec_compliant,
                                                      short_filenames=self.short_filenames)
                    collected_files[game_name].append(copy(game_file))
            except:
                game_files = None
                self.errors += 'Error while examining {}\n{}\n'.format(file_path, traceback.format_exc())
                self.files_skipped += 1
                print(traceback.format_exc())
        return collected_files

    def shortenGameFileDestination(self, game_file):
        abs_dest = game_file.getAbsoluteDestPath()
        if len(abs_dest) > MAX_DESTINATION_PATH_LENGTH:
            for game_name_length in range(MAX_GAME_NAME_LENGTH, MIN_GAME_NAME_LENGTH-10, -10):
                game_file.dest = self.getDestination(game_file,
                                                     game_name_length=game_name_length)
                abs_dest = game_file.getAbsoluteDestPath()
                if len(abs_dest) <= MAX_DESTINATION_PATH_LENGTH:
                    break
        if len(abs_dest) > MAX_DESTINATION_PATH_LENGTH:
            self.too_long_path = abs_dest

    def getCamelCasePath(self, path):
        path = ''.join([x[0].upper() + x[1:] for x in path.split(' ') if x])
        path = path.replace(',', '')
        return path

    def getInputFiles(self, input_locations=None):
        if not input_locations:
            input_locations = self.input_locations
        input_files = []
        formats = GAME_EXTENSIONS + ARCHIVE_EXTENSIONS
        for location in input_locations:
            if self.should_cancel:
                break
            if self.gui:
                self.gui.updateProgressBar(0, 0, 'Traversing '+location)
            for root, dirs, files in os.walk(location):
                for file in files:
                    ext = os.path.splitext(file)[-1].lower()[1:]
                    if ext in formats:
                        input_files.append(os.path.join(root, file))
                if not self.traverse_subfolders:
                    break
        return input_files

    def getGameFilesFromInputPath(self, file_path):
        game_files = []
        ext = os.path.splitext(file_path)[1][1:].lower()
        if ext in self.include_only and ext not in self.exclude: #file is not in archive
            game_file = GameFile(file_path)
            game = db.getGameByFile(game_file)
            if game:
                game_file.importCredentialsFromGame(game, overwrite = True)
            else:
                self.files_not_in_database.append(game_file)
            game_file.src = file_path
            game_file.dest = self.getDestination(game_file)
            game_files.append(game_file)
        elif ext in ARCHIVE_EXTENSIONS:
            if os.path.getsize(file_path)>self.max_archive_size:
                return []
            archive = Archive(file_path)
            archive_files = archive.listFiles()
            for file in archive_files:
                basename, ext = os.path.splitext(file.path)
                ext = ext[1:].lower()
                if ext not in self.include_only or ext in self.exclude:
                    continue
                game_file = GameFile(file_path)
                game_file.format = ext
                game_file.crc32 = file.crc32
                games, game = [], None
                if game_file.crc32:
                    games = db.getGamesByFileCRC32(game_file.crc32)
                if not game_file.crc32 or len(games)>1:
                    md5 = file.getMD5hash()
                    game = db.getGameByFileMD5(md5)
                    if game:
                        game_file = game.findFileByMD5(md5)
                        game_file.release = game.releases[game_file.release_seq]
                elif len(games)==1:
                    game = games[0]
                    game_file = game.findFileByCRC32(game_file.crc32)
                    game_file.release = game.releases[game_file.release_seq]
                if not game:
                    self.files_not_in_database.append(game_file)
                    game_file_lower = game_file.game.name.lower()
                    basename_lower = basename.lower()
                    if basename_lower not in game_file_lower and \
                        game_file_lower not in basename_lower:
                        game_file.content_desc = ' - '+basename
                # game_file.path_in_archive = file.path
                game_file.file_in_archive = file
                if len(archive_files)==1:
                    game_file.file_is_alone_in_archive = True
                game_file.src = file_path
                game_file.dest = self.getDestination(game_file)
                game_file.alt_dest = ''
                game_file.alt_mod_flag = ''
                game_file.game_name_differentiator = ''
                game_file.bundled_times = 0
                game_files.append(game_file)
        return game_files

    def getDestination(self, game_file, game_name_length=MAX_GAME_NAME_LENGTH):
        #Publisher name will be cropped to 3 words if dest length is too long
        if game_file.game.zxdb_id or not self.separate_unknown_files:
            kwargs = game_file.getOutputPathFormatKwargs(
                game_name_length=game_name_length)
            structure = self.output_folder_structure
            if '{Type}' in structure and '{Genre}' in structure and \
                kwargs['Type'] not in ['Applications', 'Games']:
                structure = structure.replace('{Genre}', '')
            dest_dir = structure.format(**kwargs)
        elif not game_file.game.zxdb_id and self.retain_relative_structure:
            original_path = os.path.dirname(game_file.src)
            for path in self.input_locations:
                original_path = original_path.replace(path, '')
            dest_dir = 'Unknown Files\\' + original_path
        else:
            dest_dir = 'Unknown Files'
        if game_file.game.zxdb_id:
            dest_filename = game_file.getOutputName(structure=self.output_filename_structure,
                                                    game_name_length=game_name_length)
        elif game_file.file_in_archive:
            dest_dir = os.path.join(dest_dir, os.path.dirname(game_file.file_in_archive.path))
            dest_filename = os.path.basename(game_file.file_in_archive.path)
        else:
            dest_filename = os.path.basename(game_file.src)
        if self.short_filenames:
            dest_filename = ''.join((getMeaningfulEightLetterName(game_file.getGameName()), '.', game_file.format.upper()))
            dest_dir = dest_dir.split(os.sep)
            dest_dir = [getMeaningfulEightLetterName(x) for x in dest_dir]
            dest_dir = os.path.join(*dest_dir)
        dest = os.path.join(dest_dir, dest_filename)
        dest = os.sep.join([x for x in dest.split(os.sep) if x])
        if self.use_camel_case:
            dest = self.getCamelCasePath(dest)
        dest = os.path.join(self.output_location, dest)
        return dest

    def filterCollectedFiles(self):
        for game_name, files in self.collected_files.items():
            min_release = min([file.getReleaseSeq() for file in files])
            for i, file in enumerate(files):
                if not self.include_unknown_files and not file.game.zxdb_id:
                    self.collected_files[game_name][i] = None
                if not self.include_rereleases and file.getReleaseSeq()>min_release:
                    self.collected_files[game_name][i] = None
                if not self.include_alternate and file.isAlternate():
                    self.collected_files[game_name][i] = None
                if not self.include_hacks and file.isHack():
                    self.collected_files[game_name][i] = None
                if not self.include_bad_dumps and file.isBadDump():
                    self.collected_files[game_name][i] = None
                if not self.include_xrated and file.isXRated():
                    self.collected_files[game_name][i] = None
                if self.languages and file.getLanguage() not in self.languages:
                    self.collected_files[game_name][i] = None
            files = [file for file in files if file]
            if not self.include_alternate_formats and files and game_name:
                self.collected_files[game_name] = self.filterOutAlternateFormats(files)
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
        files = sorted(files, key=lambda file: file.getSortIndex(self.include_only))
        return files[0]

    def redistributeFiles(self):
        if self.gui:
            self.gui.updateProgressBar(0, self.getCollectedFilesCount(), 'Redistributing files...')
        files_array = self.getFilesArray()
        #sort alphabetically, so people don't have to use SD Sorter afterwards.
        files_array = sorted(files_array, key=operator.attrgetter('dest'))
        for i, file in enumerate(files_array):
            if self.should_cancel:
                break
            if i % 100 == 0:
                if self.gui:
                    self.gui.updateProgressBar(i)
            try:
                if file.file_in_archive:
                    self.unpackFile(file)
                else:
                    self.copyFile(file)
                if self.include_supplementary_files:
                    self.copySupplementaryFiles(file)
                self.extractPokFile(file)
            except:
                self.errors += 'Error while redistributing {}:\n{}\n'.format(
                    file.src, traceback.format_exc())
                self.files_skipped += 1

    def copyFile(self, game_file):
        dest = game_file.getDestPath()
        try:
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            shutil.copyfile(game_file.src, dest)
        except PermissionError:
            os.chmod(game_file.dest, stat.S_IWUSR | stat.S_IWOTH | stat.S_IWGRP)
            shutil.copyfile(game_file.src, dest)
        finally:
            if self.delete_source_files:
                self.removeAllSourceFiles(game_file)
            self.files_sorted += 1

    def removeAllSourceFiles(self, game_file):
        for src in [game_file.src] + game_file.alt_src:
            self.removeFile(src)
            pok_path = os.path.splitext(game_file.src)[0] + '.pok'
            if os.path.exists(pok_path):
                self.removeFile(pok_path)
            alt_pok_path = os.path.join(os.path.dirname(pok_path), 'POKES', os.path.basename(pok_path))
            if os.path.exists(alt_pok_path):
                self.removeFile(alt_pok_path)
        for file in [game_file.file_in_archive] + game_file.alt_files_in_archives:
            if file:
                file.remove()

    def removeFile(self, src):
        try:
            print('src=',src)
            os.unlink(src)
        except PermissionError:
            os.chmod(src, stat.S_IWUSR | stat.S_IWOTH | stat.S_IWGRP)
            os.unlink(src)

    def removeEmptyDirs(self):
        for path in self.input_locations:
            for dirpath, _, _ in os.walk(path, topdown=False):  # Listing the files
                if dirpath == path:
                    break
                try:
                    os.rmdir(dirpath)
                except OSError as ex:
                    pass
                    # print(ex)

    def copySupplementaryFiles(self, file):
        dirname = os.path.dirname(file.src)
        filename = os.path.splitext(os.path.basename(file.src))[0]
        glob_regex = dirname+'/*/'+filename+'.*'
        glob_regex = glob_regex.translate({ord('['):'[\[]', ord(']'):'[\]]'})
        for sup_file in glob.glob(glob_regex):
            subdirname = os.path.split(os.path.dirname(sup_file))[-1]
            ext = os.path.splitext(sup_file)[-1].lower()
            if ext[1:] in DISALLOWED_SUPPLEMENTARY_FILES:
                continue
            dest = file.getDestPath()
            dest_dir = os.path.dirname(dest)
            dest_filename = os.path.splitext(os.path.basename(dest))[0]
            dest = os.path.join(dest_dir, subdirname, dest_filename)+ext
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if not self.delete_source_files:
                shutil.copy(sup_file, dest)
            else:
                shutil.move(sup_file, dest)
        glob_regex = dirname+'/'+filename+'.*'
        glob_regex = glob_regex.translate({ord('['):'[[]', ord(']'):'[]]'})
        for sup_file in glob.glob(glob_regex):
            ext = os.path.splitext(sup_file)[-1]
            if ext[1:] in DISALLOWED_SUPPLEMENTARY_FILES:
                continue
            dest = file.getDestPath()
            dest_dir = os.path.dirname(dest)
            dest_filename = os.path.splitext(os.path.basename(dest))[0]
            dest = os.path.join(dest_dir, dest_filename)+ext
            os.makedirs(os.path.dirname(dest), exist_ok=True)
            if not self.delete_source_files:
                shutil.copy(sup_file, dest)
            else:
                shutil.move(sup_file, dest)

    def extractPokFile(self, file):
        dest = file.getDestPath()
        if file.game.cheats:
            pok_dir_path = os.path.dirname(dest)
            pok_file_name = os.path.splitext(os.path.basename(dest))[0] + '.pok'
            if self.place_pok_files_in_pokes_subfolders:
                pok_dir_path = os.path.join(pok_dir_path, 'POKES')
                os.makedirs(pok_dir_path, exist_ok=True)
            pok_file_path = os.path.join(pok_dir_path, pok_file_name)
            file.game.exportPokFile(pok_file_path)

    def getFilesArray(self):
        files_array = []
        for files in self.collected_files.values():
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
        game_file.file_in_archive.extractTo(game_file.getDestPath())
        if self.delete_source_files:
            self.removeAllSourceFiles(game_file)
        self.files_sorted += 1
            # game_file.file_in_archive.remove()
        # archive = Archive(game_file.src)
        # files = archive.listFiles()
        # for file in files:
        #     if game_file.path_in_archive == file.path:
        #         file.extractTo(game_file.getDestPath())
        #         self.files_sorted += 1
        #         if self.delete_source_files:
        #             if len(files)==1:
        #                 self.removeFile(archive.filepath)
        #             else:
        #                 file.remove()
        #         break

    def cancel(self):
        self.should_cancel = True

    def saveLog(self):
        if not self.files_skipped and not self.files_not_in_database and \
            not self.errors:
            return
        log_name = time.strftime('%Y-%m-%d %H-%M report.log')
        self.log_path = os.path.abspath(os.path.join('logs', log_name))
        os.makedirs('logs', exist_ok=True)
        with open(self.log_path, 'w+', encoding='utf-8') as f:
            f.write('ZX Pokemaster version: {}\n\n'.format(ZX_POKEMASTER_VERSION))
            f.write('Files sorted: {}\n'.format(self.files_sorted))
            f.write('Files skipped: {}\n'.format(self.files_skipped))
            f.write('\n')
            if self.files_not_in_database:
                f.write('Files not in database: {}\n'.format(len(self.files_not_in_database)))
                f.write('-' * 20 + '\n')
                for file in self.files_not_in_database:
                    f.write('{} --> {}\n'.format(file.getSrcPathForLog(), file.getDestPath()))
            f.write('\nErrors: \n')
            f.write('-' * 20 + '\n')
            f.write(self.errors)