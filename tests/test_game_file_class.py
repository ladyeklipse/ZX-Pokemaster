from classes.game_file import GameFile
import unittest

class GameFileTests(unittest.TestCase):

    def test_md5(self):
        game_file = GameFile('E.T.X..tap.zip')
        expected_md5 = 'B04C5D9BF88EB5A008696D83EEEE69AC'.lower()
        game_file_md5 = game_file.getMD5()
        self.assertEqual(expected_md5, game_file_md5)

if __name__=='__main__':
    unittest.main()