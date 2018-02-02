import  unittest
import os
from classes.sevenzipfile import *
if (os.getcwd().endswith('tests')):
    os.chdir('..')

class TestSevenZip(unittest.TestCase):

    test_dir = 'tests/test_seven_zip'

    def test_files_listing_rar(self):
        file_path = os.path.join(self.test_dir, 'arkos.rar')
        archive = SevenZipFile(file_path)
        files = archive.listFiles()
        self.assertEqual(3, len(files))
        self.assertEqual('Arkos (1988)(Zigurat)(ES)(Part 1 of 3)[Тест юникода].z80', files[0].path)
        self.assertEqual('e0bd1ed3', files[0].crc32)
        self.assertEqual(36986, files[2].size)

    def test_file_unpacking(self):
        file_path = os.path.join(self.test_dir, 'chars.rar')
        archive = SevenZipFile(file_path)
        files = archive.listFiles()
        extraction_path = os.path.join(self.test_dir, '1', 'test.z80')
        for file in files:
            if file.crc32=='e0bd1ed3':
                file.extractTo(extraction_path)
        self.assertTrue(os.path.exists(extraction_path))