import  unittest
import os
from classes.archive_handler import *
if (os.getcwd().endswith('tests')):
    os.chdir('..')

class TestSevenZip(unittest.TestCase):

    test_dir = 'tests/test_seven_zip'

    def test_bad_archive(self):
        file_path = os.path.join(self.test_dir, 'bad_file.gz')
        archive = ZipArchive(file_path)
        with self.assertRaises(Exception):
            files = archive.listFiles()

    def test_broken_zip_file(self):
        file_path = os.path.join(self.test_dir, 'breakout_2.tzx.zip')
        archive = ZipArchive(file_path)
        files = archive.listFiles()
        self.assertGreater(len(files), 0)
        files[0].extractTo(self.test_dir+'\\breakout.tzx')

    def test_files_listing_rar(self):
        file_path = os.path.join(self.test_dir, 'arkos.rar')
        archive = ZipArchive(file_path)
        files = archive.listFiles()
        self.assertEqual(3, len(files))
        self.assertEqual('Arkos (1988)(Zigurat)(ES)(Part 1 of 3)[Тест юникода].z80', files[0].path)
        self.assertEqual('e0bd1ed3', files[0].crc32)
        self.assertEqual(36986, files[2].size)

    def test_file_unpacking(self):
        file_path = os.path.join(self.test_dir, 'chars.rar')
        archive = ZipArchive(file_path)
        files = archive.listFiles()
        extraction_path = os.path.join(self.test_dir, '1', 'test.z80')
        for file in files:
            if file.crc32=='e0bd1ed3':
                file.extractTo(extraction_path)
        self.assertTrue(os.path.exists(extraction_path))

    def test_reading_md5(self):
        file_path = os.path.join(self.test_dir, 'sort_crc_collision out.rar')
        archive = Archive(file_path)
        files = archive.listFiles()
        for file in files:
            md5 = file.getMD5hash()
            if file.path == 'Vozrazhdenie 00 (1996-01-01)(Vozrazhdenie)(RU)[Omsk].udi':
                self.assertEqual('521ee9d2b56344455bbf226e987c8684', md5)
            if file.path == 'Vozrazhdenie 01 (1996-01-31)(Vozrazhdenie)(RU)[Omsk].udi':
                self.assertEqual('998716aebebcb24af76017ee0e19615b', md5)

    def test_zip_archive(self):
        file_path = os.path.join(self.test_dir, 'arkos.zip')
        archive = Archive(file_path)
        files = archive.listFiles()
        for file in files:
            self.assertGreater(len(file.crc32), 0)
            print(file.crc32)
            md5 = file.getMD5hash()
            self.assertGreater(len(md5), 0)
            print(file.getMD5hash())

    def test_bad_zip_archive(self):
        file_paths = ['MIRAGE4.ZIP', 'Spf13.zip', 'Tranto1r.zip']
        for file_path in file_paths:
            archive = Archive(os.path.join(self.test_dir, file_path))
            files = archive.listFiles()
            self.assertGreater(len(files), 0)
            for file in files:
                file.extractTo(os.path.join(self.test_dir, 'bad_zip', file.path))

    def test_iso(self):
        file_path = 'E:\Emulators\\ZX Spectrum\iso\COLLECTION.ISO'
        archive = Archive(file_path)
        files = archive.listFiles()
        self.assertGreater(len(files), 0)