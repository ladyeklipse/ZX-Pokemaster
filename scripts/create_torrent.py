
'''
Algorythm.
1. Use Pokemaster to create sorted files with structure similar to TOSEC.
2. FOR DIRECTORY IN sorted structure:
2.1. Read corresponding DAT file:
    dict md5_dat_files = {
        'md5':file_name_from_dat),
        ...
    }
2.2. FOR FILE in directory:
    if file.md5 IN dict:
        - Create ZipFile in os.path.join(dat_dir, md5_dat_files[file.md5]
        - Add file under zipfile's name with file's extension to new zipfile.
3. Create torrent file.
4. End.
'''
import makeTorrent
import os
import shutil
import hashlib
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
from classes.sorter import Sorter
from classes.tosec_dat import *
from classes.database import Database

db = Database()
db.loadCache()


def sortFilesTOSECStyle():
    s = Sorter()
    s.input_locations = [
        # 'tosec/Sinclair ZX Spectrum/Applications/[TZX]',
        'ftp/pub/sinclair/utils',
        'ftp/pub/sinclair/compilations',
        'ftp/pub/sinclair/demos',
        'ftp/pub/sinclair/games',
        'ftp/pub/sinclair/games-extras',
        'ftp/pub/sinclair/misc',
        'ftp/pub/sinclair/magazines',
        'ftp/pub/sinclair/timex',
        'ftp/pub/sinclair/trdos',
        'ftp/zxdb',
        'tosec/reviewed files',
        'tosec/Sinclair ZX Spectrum'
    ]
    s.output_location = 'sorted\\tosec-style'
    s.output_folder_structure = '{Type}\\[{Format}]'
    s.include_supplementary_files = False
    s.ignore_alternate = False
    s.ignore_alternate_formats = False
    s.ignore_bad_dumps = False
    s.sortFiles()

def renameFilesUsingDATs():
    for root, dirs, files in os.walk('tosec\\my dats\\'):
        latest_dats_dir = os.path.join(root, next(reversed(dirs)))
        break
    total_missing_files = 0
    for root, dirs, files in os.walk(latest_dats_dir):
        for file in files:
            if 'Unknown' not in file:
                total_missing_files += renameDirUsingDAT(os.path.join(root, file))
    print('Total missing files:', total_missing_files)

def renameDirUsingDAT(dat_path):
    dat_name = os.path.basename(dat_path)
    dir_path = '\\'.join(dat_name.split('(')[0].split(' - ')[1:]).strip()
    # new_dat_path = os.path.join('tosec', 'ROMVault', 'DATRoot', dir_path, dat_name)
    # os.makedirs(os.path.dirname(new_dat_path), exist_ok=True)
    # shutil.copy(dat_path, new_dat_path)
    # dir_path = os.path.join('tosec', 'ROMVault', 'ToSort', dir_path).strip()
    dir_path = os.path.join('sorted', 'tosec-style', dir_path).strip()
    # print(dir_path)
    if not os.path.exists(dir_path):
        print('Skipped ', dir_path)
        return 0
    md5_dat_files = {}
    with open(dat_path, 'rb') as f:
        contents = f.read()
        root = etree.XML(contents)
        games = [tag for tag in root[1:] if tag.tag in ['game', 'machine']]
        for game in games:
            roms = [tag for tag in game if tag.tag == 'rom']
            for rom in roms:
                filename = rom.attrib['name']
                md5_dat_files[rom.attrib['md5']] = filename
    for root, dirs, files in os.walk(dir_path):
        for file in files:
            filepath = os.path.join(root, file)
            file_handle = open(filepath, 'rb').read()
            md5 = hashlib.md5(file_handle).hexdigest()
            if md5_dat_files.get(md5):
                src = filepath
                # dest = src.replace('tosec-style', 'tosec-style-renamed')
                del md5_dat_files[md5]
    if len(md5_dat_files):
        print(dat_name)
        print('Missing files:', len(md5_dat_files))
        for key, value in md5_dat_files.items():
            # print(value)
            game = db.getGameByFileMD5(key)
            file = game.findFileByMD5(key)
            if not file.crc32:
                raise Exception("Really missing file found: "+value)
            print(file.crc32, file.wos_path, file.tosec_path, file.game.wos_id, 'new name='+value)
    return len(md5_dat_files)

def torrentZipEachFile():
    pass

def createTOSECTorrentFile():
    pass

if __name__=='__main__':
    pass
    # if not os.path.exists('sorted\\tosec-style'):
    # sortFilesTOSECStyle()
    # renameFilesUsingDATs()
