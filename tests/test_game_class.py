from classes.game import Game
import unittest
import os
if (os.getcwd().endswith('tests')):
    os.chdir('..')

def getWosSubfolder(filename):
    return '123' if filename[0].isdigit() else filename[0].upper()

class GameTests(unittest.TestCase):

    def test_wos_id(self):
        g = Game(name='test')
        self.assertTrue(g.getWosID()=='0000000')
        g = Game(name='test', wos_id=245)
        self.assertTrue(g.getWosID() == '0000245')

    def test_tosec_name(self):
        g = Game(name='Test')
        tosec_name = g.getTOSECName()
        self.assertTrue(tosec_name=='Test (19--)(-)')
        g.publisher = 'Something software'
        tosec_name = g.getTOSECName()
        self.assertTrue(tosec_name=='Test (19--)(Something software)')
        g.year = 1999
        tosec_name = g.getTOSECName()
        self.assertTrue(tosec_name == 'Test (1999)(Something software)')
        g.setPublisher('16/48k Tape Magazine')
        self.assertEqual(g.getTOSECName(), 'Test (1999)(16-48k Tape Magazine)')

    def testSetPublisher(self):
        g = Game()
        g.setPublisher('Ariolasoft UK Ltd')
        self.assertEqual(g.publisher, 'Ariolasoft UK')
        g.setPublisher('Incentive Software Ltd')
        self.assertEqual(g.publisher, 'Incentive Software')


if __name__=='__main__':
    unittest.main()