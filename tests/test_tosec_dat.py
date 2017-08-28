from classes.tosec_dat import *
from classes.database import *
import  unittest
import os

if (os.getcwd().endswith('tests')):
    os.chdir('..')

class TestTOSECDat(unittest.TestCase):

    def test_export(self):
        dat = TOSECDat('_Test - Test - [TZX]')
        db = Database()
        game = db.getGameByWosID(9)
        dat.addFiles([file for file in game.getFiles() if file.format=='tzx'])
        dat.export()
        os.startfile(dat.getExportPath())


if __name__=='__main__':
    t = TestTOSECDat()
    t.test_export()