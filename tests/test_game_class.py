from classes.game import Game
import unittest

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
        self.assertTrue(tosec_name=='Test')
        g.publisher = 'Something software'
        tosec_name = g.getTOSECName()
        self.assertTrue(tosec_name=='Test (Something software)')
        g.year = 1999
        tosec_name = g.getTOSECName()
        self.assertTrue(tosec_name == 'Test (1999) (Something software)')
        g.parts = 2
        tosec_name = g.getTOSECName(part=2)
        self.assertTrue(tosec_name == 'Test (1999) (Something software) (Part 2 of 2)')
        g.machine_type = '48k'
        tosec_name = g.getTOSECName(part=2)
        self.assertTrue(tosec_name == 'Test (1999) (Something software) (48k) (Part 2 of 2)')

    def testSetPublisher(self):
        g = Game()
        g.setPublisher('Ariolasoft UK Ltd')
        self.assertEqual(g.publisher, 'Ariolasoft UK')
        g.setPublisher('Incentive Software Ltd')
        self.assertEqual(g.publisher, 'Incentive Software')



if __name__=='__main__':
    unittest.main()