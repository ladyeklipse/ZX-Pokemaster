import subprocess
# import sys
import os
import traceback
import hashlib
import zipfile
import stat

SEVENZIP_LIST_CMD = '7z l -slt "{archive_path}" -sccUTF-8'
SEVENZIP_EXTRACT_CMD = '7z e "{archive_path}" -o"{dest_dir}" "{src_file}" -y -sccUTF-8'
SEVENZIP_DELETE_CMD = '7z d "{archive_path}" "{file_path}" -y -sccUTF-8'

class Archive():

    def __init__(self, filepath):
        if self.__class__==Archive:
            if filepath.lower().endswith('zip'):
                self.__class__ = ZipArchive
            else:
                self.__class__ = SevenZipArchive
        self.filepath = filepath

class SevenZipArchive(Archive):

    def listFiles(self):
        command = SEVENZIP_LIST_CMD.format(archive_path=self.filepath)
        s = subprocess.Popen(command,
                               stdout=subprocess.PIPE,
                               stderr=subprocess.PIPE,
                               shell=True,
                               )
        output = s.communicate()[0].decode('UTF-8').replace('\r\n', '\n')
        # print(output)
        if 'Errors:' in output:
            errors = output.split('Error')[1]
            raise Exception('Could not open ' + self.filepath + ':' + errors)
        raw_files_list = output.split('----------')[-1].split('\n\n')
        files = []
        for item in raw_files_list:
            if item and 'Folder = +' not in item:
                file = ArchivedFile(sevenzip_text=item, parent=self)
                if not file.path:
                    continue
                files.append(file)
        return files

class ZipArchive(Archive):

    def listFiles(self):
        files = []
        try:
            with zipfile.ZipFile(self.filepath) as zf:
                for zfname in zf.namelist():
                    zfinfo = zf.getinfo(zfname)
                    file = ArchivedFile(zipfileinfo=zfinfo, parent=self)
                    files.append(file)
        except zipfile.BadZipFile:
            self.__class__ = SevenZipArchive
            files = self.listFiles()
        return files

class ArchivedFile():

    path = ''
    crc32 = ''
    size = 0

    def __init__(self, sevenzip_text=None, zipfileinfo=None, parent=None):
        self.parent = parent
        if sevenzip_text:
            info = sevenzip_text.split('\n')
            for key_value_pair in info:
                if ' = ' not in key_value_pair:
                    continue
                key, value = key_value_pair.split(' = ')
                if key == 'Size':
                    self.size = int(value)
                elif key == 'Path':
                    self.path = value
                elif key == 'CRC':
                    self.crc32 = value.lower()
        elif zipfileinfo:
            self.crc32 = hex(zipfileinfo.CRC)[2:].zfill(8)
            self.size = zipfileinfo.file_size
            self.path = zipfileinfo.filename
        else:
            raise Exception('Could not initialize ArchiveFile with no data.')

    def extractTo(self, dest_path):
        dest_dir, dest_name = os.path.dirname(dest_path), os.path.basename(dest_path)
        if type(self.parent).__name__=='ZipArchive':
            try:
                with zipfile.ZipFile(self.parent.filepath) as zf:
                    data = zf.read(self.path)
                    try:
                        os.makedirs(dest_dir, exist_ok=True)
                        with open(dest_path, 'wb+') as output:
                            output.write(data)
                    except PermissionError:
                        os.chmod(dest_path, stat.S_IWRITE)
                        with open(dest_path, 'wb+') as output:
                            output.write(data)
            except (zipfile.BadZipFile, NotImplementedError):
                self.parent.__class__ = SevenZipArchive
                self.extractTo(dest_path)
        else:
            command = SEVENZIP_EXTRACT_CMD.format(
                archive_path=self.parent.filepath,
                dest_dir=dest_dir,
                src_file=self.path)
            print(command)
            s = subprocess.Popen(command,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             shell=True)
            print(s.communicate()[0].decode('UTF-8'))
            unrenamed_path = os.path.join(dest_dir, os.path.basename(self.path))
            if os.path.exists(unrenamed_path):
                os.replace(unrenamed_path, dest_path)
        return True

    def getMD5hash(self):
        if type(self.parent).__name__=='ZipArchive':
            with zipfile.ZipFile(self.parent.filepath) as zf:
                unzipped_file = zf.read(self.path)
                md5 = hashlib.md5(unzipped_file).hexdigest()
                return md5
        elif type(self.parent).__name__=='SevenZipArchive':
            dest_dir = '_temp'
            command = SEVENZIP_EXTRACT_CMD.format(
                archive_path=self.parent.filepath,
                dest_dir=dest_dir,
                src_file=self.path)
            print(command)
            s = subprocess.Popen(command,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             shell=True)
            print(s.communicate()[0].decode('UTF-8'))
            temp_unpacked_path = os.path.join(dest_dir, os.path.basename(self.path))
            if os.path.exists(temp_unpacked_path):
                with open(temp_unpacked_path, 'rb') as f:
                    contents = f.read()
                    md5 = hashlib.md5(contents).hexdigest()
                os.remove(temp_unpacked_path)
                return md5
            else:
                return None

    def remove(self):
        #Removes file from archive.
        #Also removes the archive itself, if after removing of the file it becomes empty.
        # if type(self.parent).__name__=='ZipArchive':
        #     with zipfile.ZipFile(self.parent.filepath) as zf:
        #
        # elif type(self.parent).__name__ == 'SevenZipArchive':
            command = SEVENZIP_DELETE_CMD.format(
                archive_path=self.parent.filepath,
                file_path=self.path)
            print(command)
            s = subprocess.Popen(command,
                             stdout = subprocess.PIPE,
                             stderr = subprocess.PIPE,
                             shell=True)
            s.wait()
            # print(s.communicate()[0].decode('UTF-8'))
            files = self.parent.listFiles()
            if not files:
                os.unlink(self.parent.filepath)