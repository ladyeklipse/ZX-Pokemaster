from classes.game_file import GameFile
from classes.game import Game
import unittest
import os
print(os.getcwd())
if (os.getcwd().endswith('tests')):
    os.chdir('..')


class GameFileTests(unittest.TestCase):

    def test_md5(self):
        print(os.getcwd())
        game = Game(wos_id=1660)
        game_file = GameFile('wos_games\e\E.T.X..tap.zip', game=game)
        expected_md5 = '1C057504487D076514C19CA181498590'.lower()
        game_file_md5 = game_file.getMD5(zipped=True)
        self.assertEqual(expected_md5, game_file_md5)
        expected_md5 = 'B04C5D9BF88EB5A008696D83EEEE69AC'.lower()
        game_file_md5 = game_file.getMD5(zipped=False)
        self.assertEqual(expected_md5, game_file_md5)

    def test_getting_info_from_tosec_name(self):
        file = GameFile('Gonzzalezz (1989)(Opera Soft)(es)(Side B).zip')
        self.assertEqual(file.game.name, 'Gonzzalezz')
        self.assertEqual(file.game.getYear(), '1989')
        self.assertEqual(file.game.getPublisher(), 'Opera Soft')
        self.assertEqual(file.getLanguage(), 'es')
        self.assertEqual(file.getSide(), 'B')
        file = GameFile('Gonzzalezz.zip')
        self.assertEqual(file.game.name, 'Gonzzalezz')

if __name__=='__main__':
    unittest.main()