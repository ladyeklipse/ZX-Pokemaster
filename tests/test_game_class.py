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
        self.assertTrue(tosec_name=='Test (19xx)(-)')
        g.publisher = 'Something software'
        tosec_name = g.getTOSECName()
        self.assertTrue(tosec_name=='Test (19xx)(Something software)')
        g.year = 1999
        tosec_name = g.getTOSECName()
        self.assertTrue(tosec_name == 'Test (1999)(Something software)')
        g.setPublisher('16/48k Tape Magazine')
        self.assertEqual(g.getTOSECName(), 'Test (1999)(16-48k Tape Magazine)')
        g.setPublisher('Test [1]')
        self.assertEqual(g.getTOSECName(), 'Test (1999)(Test)')
        g.setPublisher('Test [test]')
        self.assertEqual(g.getTOSECName(), 'Test (1999)(Test)')

    def test_set_publisher(self):
        g = Game()
        g.setPublisher('Apogee Software [1]')
        self.assertEqual(g.publisher, 'Apogee Software')
        g.setPublisher('Ariolasoft UK Ltd')
        self.assertEqual(g.publisher, 'Ariolasoft UK')
        g.setPublisher('Incentive Software Ltd')
        self.assertEqual(g.publisher, 'Incentive Software')
        g.setPublisher('16/48 Tape Magazine')
        self.assertEqual(g.publisher, '16-48 Tape Magazine')

    def test_set_genre(self):
        g = Game()
        g.setGenre("Arcade: Race 'n' Chase")
        self.assertEqual(g.genre, "Arcade - Race 'n' Chase")

    def test_colon_in_name(self):
        g = Game('Ace 2: Combat')
        self.assertEqual(g.getTOSECName(), 'Ace 2 - Combat (19xx)(-)')

if __name__=='__main__':
    unittest.main()