from classes.tosec_dat import *
from classes.database import *
import  unittest
import os

if (os.getcwd().endswith('tests')):
    os.chdir('..')

class TestTOSECDat(unittest.TestCase):

    def test_export(self):
        dat = TOSECDat('_Test - Text - [Mixed]')
        db = Database()
        game = db.getGameByWosID(1)
        dat.addFiles(game.getFiles())
        dat.export()
        os.startfile(dat.getExportPath())


if __name__=='__main__':
    t = TestTOSECDat()
    t.test_export()