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
        game_file = GameFile('ftp\pub\sinclair\games\e\E.T.X..tap.zip', game=game)
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

    def test_lord_bromleys_estate(self):
        file = GameFile("007 - Lord Bromley's Estate (1990)(Domark).zip")
        self.assertEqual(file.game.name, "007 - Lord Bromley's Estate")
        self.assertEqual(file.game.getYear(), '1990')

    def test_cascade_games(self):
        file = GameFile('Spectral Skiing (1983)(Cascade Games)[16K].zip')
        self.assertEqual(file.game.publisher, 'Cascade Games')
        self.assertEqual(file.game.getPublisher(), 'Cascade Games')

    def test_demo(self):
        file = GameFile('A Treat! (demo) (1985)(Firebird Software).zip')
        self.assertEqual(file.game.getPublisher(), 'Firebird Software')
        self.assertEqual(file.game.getYear(), '1985')
        self.assertEqual(file.game.name, 'A Treat!')

if __name__=='__main__':
    unittest.main()