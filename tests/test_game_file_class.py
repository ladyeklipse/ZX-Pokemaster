from classes.game_file import GameFile
from classes.game_file import GameRelease
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
        game_file = GameFile('\pub\sinclair\games\e\E.T.X..tap.zip', game=game)
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
        self.assertEqual(file.getSide(), 'Side B')
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

    def test_notes(self):
        file = GameFile("Test (19xx)(Publisher)[t][a][re-release]")
        self.assertEqual(file.notes, '[re-release]')
        path = 'Sinclair ZX Spectrum\Games\[TAP]\Backpackers Guide to the Universe (1984)(Fantasy Software)[passworded].zip'
        file = GameFile(path)
        self.assertEqual(file.notes, '[passworded]')


    def test_cascade_games(self):
        file = GameFile('Spectral Skiing (1983)(Cascade Games)[16K].zip')
        self.assertEqual(file.game.publisher, 'Cascade Games')
        self.assertEqual(file.game.getPublisher(), 'Cascade Games')

    def test_demo(self):
        file = GameFile('A Treat! (demo) (1985)(Firebird Software).zip')
        self.assertEqual(file.game.getPublisher(), 'Firebird Software')
        self.assertEqual(file.game.getYear(), '1985')
        self.assertEqual(file.game.name, 'A Treat!')

    def test_tape_as_part(self):
        file = GameFile('tosec\Games\[TZX]\Blood of Bogmole, The (1986)(Compass Software)[Master Tape].zip')
        self.assertEqual(file.part, 0)
        file = GameFile('tosec\Games\[TZX]\Blood of Bogmole, The (1986)(Compass Software)(Tape 1).zip')
        self.assertEqual(file.part, 1)
        file = GameFile('tosec\Games\[TZX]\Blood of Bogmole, The (1986)(Compass Software)(Part 2).zip')
        self.assertEqual(file.part, 2)

    def test_multilanguage(self):
        file = GameFile('tosec\Games\[TZX]\Blood of Bogmole, The (1986)(Compass Software)(M3).zip')
        self.assertEqual(file.language, 'M3')

    def test_content_desc(self):
        file = GameFile('Sinclair ZX Spectrum\Applications\[TAP]\HiSoft BASIC v1.0 (1986)(HiSoft)[a].zip')
        game_name = 'HiSoft BASIC'
        file.game.wos_id=1
        file.game.name = game_name
        file.release.aliases = [game_name]
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, ' v1.0')
        game_name = 'Treasure Island Dizzy'
        file = GameFile('Sinclair ZX Spectrum\Games\[TZX]\Dizzy II - Treasure Island Dizzy (1988)(Codemasters).zip')
        file.game.wos_id=1
        file.game.name = game_name
        file.release.aliases = [game_name]
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, '')
        file = GameFile('Sinclair ZX Spectrum\Games\[Z80]\\007 - Live and Let Die (1988)(Domark).zip')
        game_name = 'Live and Let Die'
        file.game.wos_id=1
        file.game.name = game_name
        file.release.aliases = 'Live and Let Die - The Computer Game/Live and Let Die/Aquablast'.split('/')
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, '')
        file = GameFile('Sinclair ZX Spectrum\Games\[Z80]\Hunter II - Olympus-Mons (1985)(David Rushall).zip')
        game_name = 'Hunter II - Olympus-mons'
        file.game.wos_id=1
        file.game.name = game_name
        file.release.aliases = 'Hunter II - Olympus-mons/Hunter II - Olympus-mons'.split('/')
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, '')

    def test_duplicate_spaces(self):
        game_file = GameFile('Format  Utility (1994)(MI & DI  Software).trd')
        out_name = game_file.getOutputName()
        self.assertEqual(out_name, 'Format Utility (1994)(MI & DI Software).trd')

    def test_picking_best_release_name(self):
        g = Game('Everyday Tale of a Seeker of Gold, An')
        r = GameRelease(game=g, aliases=\
        'Everyday Tale of a Seeker of Gold, An/An Everyday Tale of a Seeker of Gold'.split('/'))
        f = GameFile('test.mgt')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Everyday Tale of a Seeker of Gold, An (19xx)(-).mgt')
        g = Game('Live and Let Die')
        r = GameRelease(game=g, aliases=['Aquablast', 'Live and Let Die - The Computer Game'])
        f = GameFile('test.tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Live and Let Die - The Computer Game (19xx)(-)[aka Aquablast].tap')
        g = Game('Where Time Stood Still')
        r = GameRelease(game=g, aliases=['Land That Time Forgot, The', 'Where Time Stood Still', 'Tibet'])
        f = GameFile('test.tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Where Time Stood Still (19xx)(-)[aka Land That Time Forgot, The][aka Tibet].tap')
        g = Game('Adventures of St. Bernard, The')
        r = GameRelease(game=g, aliases=\
        'Adventures of Saint Bernard, The/Adventures of St. Bernard, The/The Adventures of St. Bernard'.split('/'))
        f = GameFile('test.tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Adventures of St. Bernard, The (19xx)(-)[aka Adventures of Saint Bernard, The].tap')




if __name__=='__main__':
    unittest.main()