from classes.game_file import GameFile
from classes.game import Game
import unittest
import os
print(os.getcwd())
if (os.getcwd().endswith('tests')):
    os.chdir('..')


class GameFileTests(unittest.TestCase):

    def test_hashsums(self):
        print(os.getcwd())
        game = Game(wos_id=1660)
        game_file = GameFile('ftp\pub\sinclair\games\e\E.T.X..tap.zip', game=game)
        expected_md5 = 'b04c5d9bf88eb5a008696d83eeee69ac'
        self.assertEqual(expected_md5, game_file.getMD5())
        expected_sha1 = 'a879037fd3ba64170e83d4d44652681b1eb097e3'
        self.assertEqual(expected_sha1, game_file.getSHA1())
        expected_crc32 = '3699934d'
        self.assertEqual(expected_crc32, game_file.getCRC32())

    def test_weird_md5(self):
        game_file = GameFile('ftp/pub/sinclair/utils/3DGameMaker(GraphicEditor3D).tap.zip')
        self.assertTrue(os.path.exists(game_file.getLocalPath()))
        self.assertGreater(len(game_file.getMD5()), 0)
        game_file = GameFile('ftp\zxdb\sinclair\entries\\0030083\DogmoleTuppowski.scl.zip')
        self.assertTrue(os.path.exists(game_file.getLocalPath()))
        self.assertGreater(len(game_file.getMD5()), 0)

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
        file = GameFile("007 - Lord Bromley's Estate (1990)(Domark)[cr].zip")
        self.assertEqual(file.game.name, "007 - Lord Bromley's Estate")
        self.assertEqual(file.game.getYear(), '1990')
        self.assertEqual(file.game.getLanguage(), 'en')
        self.assertEqual(file.mod_flags, '[cr]')

    def test_mod_flags(self):
        file = GameFile("Test (19xx)(Publisher)[a]")
        self.assertEqual(file.mod_flags, '')
        file = GameFile("Test (19xx)(Publisher)[m]")
        self.assertEqual(file.mod_flags, '[m]')
        file = GameFile("Test (19xx)(Publisher)[a][m][hacked]")
        self.assertEqual(file.mod_flags, '[m][hacked]')
        file = GameFile("Test (19xx)(Publisher)[a][re-release]")
        self.assertEqual(file.mod_flags, '')
        file = GameFile("Test (19xx)(Publisher)[t][a]")
        self.assertEqual(file.mod_flags, '[t]')

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