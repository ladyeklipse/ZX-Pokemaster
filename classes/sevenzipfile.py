import subprocess
import sys
import os
import traceback

# def get_console_enc(sys_enc="utf-8"):
#     try:
#         enc = sys_enc
#         if sys.platform.startswith("win"):
#             import ctypes
#             enc = "cp%d" % ctypes.windll.kernel32.GetOEMCP()
#         else: #Linux
#             enc = (sys.stdout.encoding if sys.stdout.isatty() else
#                         sys.stderr.encoding if sys.stderr.isatty() else
#                             sys.getfilesystemencoding() or sys_enc)
#     except Exception as e:
#         print(traceback.format_exc())
#     finally:
#         return enc
SEVENZIP_LIST_CMD = '7z l -slt {archive_path} -sccUTF-8'
SEVENZIP_EXTRACT_CMD = '7z e {archive_path} -o{dest_dir} {src_file} -y -sccUTF-8'

class SevenZipFile():

    def __init__(self, filepath):
        self.filepath = filepath

    def listFiles(self):
        command = SEVENZIP_LIST_CMD.format(archive_path=self.filepath)
        s = subprocess.Popen(command,
                                           stdout=subprocess.PIPE,
                                           stderr=subprocess.PIPE,
                                           shell=True,
                                           )
        output = s.communicate()[0].decode('UTF-8').replace('\r\n', '\n')
        raw_files_list = output.split('----------')[-1].split('\n\n')
        files = []
        for item in raw_files_list:
            file = ArchivedFile(item, parent=self)
            if not file.path:
                continue
            files.append(file)
            # print(file.__dict__)
        return files

class ArchivedFile():

    path = ''
    crc32 = ''
    size = 0

    def __init__(self, text, parent=None):
        self.parent = parent
        info = text.split('\n')
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

    def extractTo(self, dest_path):
        dest_dir, dest_name = os.path.dirname(dest_path), os.path.basename(dest_path)
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
            os.rename(unrenamed_path, dest_path)
