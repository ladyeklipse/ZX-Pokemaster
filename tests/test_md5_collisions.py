import unittest
import os
from classes.database import *

if (os.getcwd().endswith('tests')):
    os.chdir('..')

db = Database()
db.loadCache()

class TestMD5Collisions(unittest.TestCase):

    def test_md5_table(self):
        md5_collisions_table = db.execute('SELECT * from files_with_same_md5')
        self.assertEqual(len(md5_collisions_table), 0)

    def test_all_files_represented(self):
        files_not_represented = []
        with open('same_md5.csv', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.split(';')
                md5 = line[4]
                if not md5 or md5 in db.cache_by_md5:
                    continue
                files_not_represented.append([line[9], line[10], line[11]])
        for record in files_not_represented:
            print(record)
        self.assertEqual(len(files_not_represented), 0)

