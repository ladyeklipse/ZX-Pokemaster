from classes.game_file import GameFile
from classes.game_file import GameRelease
from classes.game import Game
from classes.database import Database
from settings import *
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
        file = GameFile('Gonzzalezz (1989)(Opera Soft)(es)(Side B).tap')
        self.assertEqual(file.game.name, 'Gonzzalezz')
        self.assertEqual(file.game.getYear(), '1989')
        self.assertEqual(file.game.getPublisher(), 'Opera Soft')
        self.assertEqual(file.getLanguage(), 'es')
        self.assertEqual(file.getSide(), 'Side B')
        file = GameFile('Gonzzalezz.tap')
        self.assertEqual(file.game.name, 'Gonzzalezz')

    def test_lord_bromleys_estate(self):
        file = GameFile("007 - Lord Bromley's Estate (1990)(Domark)[cr].tap")
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
        self.assertEqual(file.mod_flags, '[m]')
        file = GameFile("Test (19xx)(Publisher)[a][h by SKiDROW][m]")
        self.assertEqual(file.mod_flags, '[h by SKiDROW][m]')
        file = GameFile("Test (19xx)(Publisher)[a][re-release]")
        self.assertEqual(file.mod_flags, '')
        file = GameFile("Test (19xx)(Publisher)[t][a]")
        self.assertEqual(file.mod_flags, '[t]')

    def test_notes(self):
        path = 'Sinclair ZX Spectrum\Games\[TAP]\Backpackers Guide to the Universe (1984)(Fantasy Software)[passworded].tap'
        file = GameFile(path)
        self.assertEqual(file.notes, '[passworded]')
        file = GameFile("Test (19xx)(Publisher)[t][a][re-release]")
        self.assertEqual(file.notes, '')


    def test_cascade_games(self):
        file = GameFile('Spectral Skiing (1983)(Cascade Games)[16K].tap')
        self.assertEqual(file.game.publisher, 'Cascade Games')
        self.assertEqual(file.game.getPublisher(), 'Cascade Games')

    def test_demo(self):
        file = GameFile('A Treat! (demo) (1985)(Firebird Software).tap')
        self.assertEqual(file.game.getPublisher(), 'Firebird')
        self.assertEqual(file.game.getYear(), '1985')
        self.assertEqual(file.game.name, 'A Treat!')

    def test_tape_as_part(self):
        file = GameFile('Bridge Master (1983)(Serin Software)(Tape 1 of 2 Side A).tzx')
        self.assertEqual(file.part, 1)
        self.assertEqual(file.side, 1)
        file = GameFile('tosec\Games\[TZX]\Blood of Bogmole, The (1986)(Compass Software)[Master Tape].tap')
        self.assertEqual(file.part, 0)
        file = GameFile('tosec\Games\[TZX]\Blood of Bogmole, The (1986)(Compass Software)(Tape 1).tap')
        self.assertEqual(file.part, 1)
        file = GameFile('tosec\Games\[TZX]\Blood of Bogmole, The (1986)(Compass Software)(Part 2).tap')
        self.assertEqual(file.part, 2)

    def test_multilanguage(self):
        file = GameFile('tosec\Games\[TZX]\Blood of Bogmole, The (1986)(Compass Software)(M3).tap')
        self.assertEqual(file.language, 'M3')

    def test_content_desc(self):
        file = GameFile('Adventure F - Eye of Bain - The Eye of Bain (1984)(Artic Computing).z80')
        game_name = 'Adventure F - Eye of Bain'
        file.release.aliases = [game_name]
        file.game.name = game_name
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, '')
        file = GameFile('Sinclair ZX Spectrum\Applications\[TAP]\HiSoft BASIC v1.0 (1986)(HiSoft)[a].tap')
        game_name = 'HiSoft BASIC'
        file.game.wos_id=1
        file.game.name = game_name
        file.release.aliases = [game_name]
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, ' v1.0')
        game_name = 'Treasure Island Dizzy'
        file = GameFile('Sinclair ZX Spectrum\Games\[TZX]\Dizzy II - Treasure Island Dizzy (1988)(Codemasters).tap')
        file.game.wos_id=1
        file.game.name = game_name
        file.release.aliases = [game_name]
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, '')
        file = GameFile('Sinclair ZX Spectrum\Games\[Z80]\\007 - Live and Let Die (1988)(Domark).tap')
        game_name = 'Live and Let Die'
        file.game.wos_id=1
        file.game.name = game_name
        file.release.aliases = 'Live and Let Die - The Computer Game/Live and Let Die/Aquablast'.split('/')
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, '')
        file = GameFile('Sinclair ZX Spectrum\Games\[Z80]\Hunter II - Olympus-Mons (1985)(David Rushall).tap')
        game_name = 'Hunter II - Olympus-mons'
        file.game.wos_id=1
        file.game.name = game_name
        file.release.aliases = 'Hunter II - Olympus-mons/Hunter II - Olympus-mons'.split('/')
        file.setContentDesc(os.path.basename(file.path))
        self.assertEqual(file.content_desc, '')

    def test_duplicate_spaces(self):
        game_file = GameFile('Format  Utility (1994)(MI & DI  Software).trd')
        out_name = game_file.getOutputName()
        self.assertEqual(out_name, 'Format Utility (1994)(MI & DI).trd')

    def test_picking_best_release_name(self):
        g = Game('Dizzy 2 - Treasure Island Dizzy')
        r = GameRelease(game=g)
        f = GameFile('Dizzy II - Treasure Island Dizzy (19xx)(-).tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Dizzy 2 - Treasure Island Dizzy (19xx)(-).tap')
        g = Game('Bug-Eyes')
        r = GameRelease(game=g)
        f = GameFile('Bor-Fies (19xx)(-)[aka Bug-Eyes].tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Bug-Eyes (19xx)(-)[aka Bor-Fies].tap')
        db = Database()
        g = db.getGameByWosID(1799)
        r = g.releases[3]
        f = GameFile('Sinclair ZX Spectrum\Games\[TZX]\Picapiedra, Los (1989)(MCM Software)[48-128K][aka Flintstones, The].tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(),'Picapiedra, Los (1989)(MCM)(48K-128K)(ES)(en)[aka Flintstones, The].tap')
        g = Game('Alcatraz II')
        r = GameRelease(game=g, aliases='Alcatraz II - The Doomsday Mission/Alcatraz II/Alcatrazz 2 - The Doomsday Mission'.split('/'))
        f = GameFile('Doomsday Mission.tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(),
                         'Alcatraz II - The Doomsday Mission (19xx)(-)[aka Alcatrazz 2 - The Doomsday Mission].tap')
        g = Game('Cribbage')
        r = GameRelease(game=g)
        f = GameFile('Cribbage - Intro (19xx)(-).tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Cribbage (19xx)(-).tap')
        g = Game('Everyday Tale of a Seeker of Gold, An')
        r = GameRelease(game=g, aliases= \
            'Everyday Tale of a Seeker of Gold, An/An Everyday Tale of a Seeker of Gold'.split('/'))
        f = GameFile('Tale of a Seeker of Gold.mgt')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Everyday Tale of a Seeker of Gold, An (19xx)(-).mgt')
        g = Game('Live and Let Die')
        r = GameRelease(game=g, aliases=['Aquablast', 'Live and Let Die - The Computer Game'])
        f = GameFile('Aquablast.tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Live and Let Die - The Computer Game (19xx)(-)[aka Aquablast].tap')
        g = Game('Where Time Stood Still')
        r = GameRelease(game=g, aliases=['Land That Time Forgot, The', 'Where Time Stood Still', 'Tibet'])
        f = GameFile('where time stood still.tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Where Time Stood Still (19xx)(-)[aka Land That Time Forgot, The][aka Tibet].tap')
        g = Game('Adventures of St. Bernard, The')
        r = GameRelease(game=g, aliases= \
            'Adventures of Saint Bernard, The/Adventures of St. Bernard, The/The Adventures of St. Bernard'.split('/'))
        f = GameFile('saint bernard.tap')
        r.addFile(f)
        f.setAka()
        self.assertEqual(f.getTOSECName(), 'Adventures of St. Bernard, The (19xx)(-)[aka Adventures of Saint Bernard, The].tap')

    def test_sort_mod_flags(self):
        game_file = GameFile('Game (19xx)(-)[f +2][cr by Someone][MaxBoot]')
        game_file.sortModFlags()
        self.assertEqual(game_file.mod_flags, '[cr by Someone][f +2]')
        self.assertEqual(game_file.notes, '[MaxBoot]')

    def  test_set_country(self):
        game_file = GameFile('Sinclair ZX Spectrum\Demos\[SCL]\#AAABOG (2016)(wbr)(128K)(RU).tap', source='tosec')
        self.assertEqual(game_file.release.country, 'RU')

    def test_country(self):
        game_file = GameFile('Game (19xx)(Publisher).tap')
        game_file.release.country = 'GB'
        game_file.language = 'en'
        self.assertEqual(game_file.getTOSECName(), 'Game (19xx)(Publisher).tap')
        game_file.release.country = 'CZ'
        game_file.language = 'cz'
        self.assertEqual(game_file.getTOSECName(), 'Game (19xx)(Publisher)(CZ).tap')
        game_file.release.country = 'GB'
        game_file.language = 'es'
        self.assertEqual(game_file.getTOSECName(), 'Game (19xx)(Publisher)(GB)(es).tap')
        game_file.release.country = 'RU'
        game_file.language = 'en'
        self.assertEqual(game_file.getTOSECName(), 'Game (19xx)(Publisher)(RU)(en).tap')
        game_file.release.country = ''
        game_file.language = 'en'
        self.assertEqual(game_file.getTOSECName(), 'Game (19xx)(Publisher).tap')
        game_file = GameFile('Sinclair ZX Spectrum\Games\[TAP]\Mihotabpa (19xx)(-)(ru).tap')
        self.assertEqual(game_file.getTOSECName(), 'Mihotabpa (19xx)(-)(ru).tap')
        game_file = GameFile('Sinclair ZX Spectrum\Games\[TAP]\Mihotabpa (19xx)(-)(ru)[tr ru].tap')
        self.assertEqual(game_file.getTOSECName(), 'Mihotabpa (19xx)(-)[tr ru].tap')

    def test_set_part(self):
        game_file = GameFile('Test(Part5).tap')
        game_file.setPart('Test(Part5).tap')
        self.assertEqual(game_file.part, 5)
        game_file = GameFile('tosec\fikus-pikus\renamed\Compilations\Demos\[TRD]\Fikus Pikus Demos (19xx)(Flash)(Disk 5 of 140).trd')
        self.assertEqual(game_file.getType(), 'Compilations\\Demos')
        self.assertEqual(game_file.part, 5)
        game_file = GameFile('tosec\fikus-pikus\renamed\Compilations\Demos\[TRD]\Fikus Pikus Demos (19xx)(Flash)(Disk 101 of 140).trd')
        self.assertEqual(game_file.getType(), 'Compilations\\Demos')
        self.assertEqual(game_file.part, 101)

    # def test_preserve_aka(self):
    #     game_file = GameFile("DreamWalker (2014)(RetroSouls)(48K-128K)(RU)(en)[aka Alter Ego 2].tap")
    #     self.assertTrue('Alter Ego 2' in game_file.release.getAllAliases())
    #     self.assertTrue('DreamWalker' in game_file.release.getAllAliases())
    #     game_file = GameFile("DreamWalker (2014)(RetroSouls)(48K-128K)(RU)(en)[aka Alter Ego 2][aka DreamWalker].tap")
    #     self.assertTrue('Alter Ego 2' in game_file.release.getAllAliases())
    #     self.assertTrue('DreamWalker' in game_file.release.getAllAliases())
    #     self.assertEqual(len(game_file.release.getAllAliases()), 2)
    #
    # def test_remove_aka(self):
    #     game_file = GameFile(
    #         'Professional Adventure Writer (1986)(Gilsoft International)(48K-128K)(Side A)[aka Professional Adventure Writing System, The][aka PAW].tzx')
    #     g = Game('Where Time Stood Still')
    #     r = GameRelease(game=g, aliases=['Land That Time Forgot, The', 'Where Time Stood Still', 'Tibet'])
    #     r.addFile(game_file)
    #     game_file.setAka()
    #     self.assertEqual(game_file.notes, '[aka Land That Time Forgot, The][aka Tibet]')
    #     game_file.removeAka()
    #     self.assertEqual(game_file.notes, '[aka Tibet]')
    #     game_file.removeAka()
    #     self.assertEqual(game_file.notes, '')

    def test_preserve_version(self):
        game_file = GameFile("DreamWalker v1.0 (2014)(RetroSouls)(48K-128K)(RU)(en)[aka Alter Ego 2][aka DreamWalker].tap")
        self.assertEqual(game_file.game.name, 'DreamWalker')
        self.assertEqual(game_file.content_desc, ' v1.0')

    def test_preserve_date(self):
        game_file = GameFile('Game (2017-06-06)(Company).tzx')
        tosec_output_name = game_file.getTOSECName()
        self.assertEqual(tosec_output_name, 'Game (2017-06-06)(Company).tzx')
        db = Database()
        game = db.getGameByWosID(30408)
        game_file = GameFile('tosec\itch.io\Games\Robot 1 in... The Ship of Doom (2017-06-18)(Recardo, Mat)(48K-128K).tzx',
                             source='tosec')
        game.addFile(game_file)
        self.assertEqual(game_file.release.year, '2017-06-18')
        tosec_output_name = game_file.getTOSECName()
        self.assertEqual(tosec_output_name, 'Robot 1 in... The Ship of Doom (2017-06-18)(Recardo, Mat)(48K-128K).tzx')

    def test_trainer_as_machine_type(self):
        game_file = GameFile('Sinclair ZX Spectrum\Games\[TAP]\Predator (1987)(Activision)[t +2].tap')
        self.assertFalse(game_file.machine_type=='+2')

    def test_strip_name_if_no_mod_flags(self):
        pattern = '{GameName} ({Year}) ({Publisher}) ({MachineType}) {ModFlags}'
        game_file = GameFile('Game (19xx)(-).tap')
        output_name = game_file.getOutputName(pattern)
        self.assertEqual(output_name, 'Game (19xx) (-).tap')
        game_file = GameFile('Game (19xx)(-)[m].tap')
        output_name = game_file.getOutputName(pattern)
        self.assertEqual(output_name, 'Game (19xx) (-) [m].tap')

    def test_bilinguic_file(self):
        game_file = GameFile('Game (19xx)(-)(en-es).tap')
        language = game_file.getLanguage()
        self.assertEqual(language, 'en-es')

    def test_adult_game(self):
        game_file = GameFile('Game (19xx)(-).tap')
        game_file.game.x_rated = True
        game_file.alt_mod_flag = '[a]'
        tosec_name = game_file.getTOSECName()
        self.assertEqual(tosec_name, 'Game (19xx)(-)[a][adult].tap')

    def test_game_type(self):
        game_file = GameFile('C:\ZX Pokemaster\\tosec\\reviewed files\\CSSCGC Games Reviewed\\1997\\Advanced Advocacy Simulator (1997)(Jolly, Derek)[CSSCGC].sna')
        self.assertEqual(game_file.getTOSECDatName(), 'Sinclair ZX Spectrum - Games - [SNA]')
        self.assertEqual(game_file.game.getGenre(), 'Various Games')
        self.assertEqual(game_file.getType(), 'Games')

    def test_file_length(self):
        game_file = GameFile("ZX Spectrum+ User Guide Companion Cassette (1984)(Dorling Kindersley)(GB)(es)(Side A).tap")
        game_file.notes = "[aka ZX Spectrum+ GuideCassette De L'Utilisateur][aka ZX Spectrum+ Kaseta sa Uputstvom za Upotrebu][aka ZX Spectrum+ Guia Para el Empleo][aka Cassetta Di Guida Per L'Utente][aka Kilavuz Ve Yardimci Kaset][aka Cassette Bij Handleiding][aka Kassette fur Benutzer][aka Kayttajan Opaskasetti]"
        game_file.alt_dest = game_file.getTOSECName()
        MAX_GAME_NAME_LENGTH=200
        MAX_DESTINATION_PATH_LENGTH=200
        if len(game_file.alt_dest) > MAX_DESTINATION_PATH_LENGTH:
            for game_name_length in range(MAX_GAME_NAME_LENGTH, MIN_GAME_NAME_LENGTH-10, -10):
                game_file.removeAka()
                game_file.alt_dest = game_file.getTOSECName(game_name_length=game_name_length)
                if len(game_file.alt_dest) <= MAX_DESTINATION_PATH_LENGTH:
                    break
        self.assertLessEqual(len(game_file.alt_dest), 200)

    def test_language_detection(self):
        game_file = GameFile('Three Octopuses (2017)(kas29)(RU).tap')
        self.assertEqual(game_file.getLanguage(), 'ru')

    def test_dot_in_game_name(self):
        game = Game('H.E.R.O.')
        file = GameFile('H.E.R.O. (19xx)(-).tap')
        file.game = game
        self.assertEqual(file.getTOSECName(),'H.E.R.O. (19xx)(-).tap')

    def test_double_tr_ru(self):
        game = Game('Saboteur II')
        file = GameFile('Saboteur II (19xx)(-)[h Crudesoft ru][t][tr ru].tap')
        file.getParamsFromTOSECPath('Saboteur II (19xx)(-)[tr ru Rybkin].tap')
        self.assertEqual(file.mod_flags, '[h Crudesoft ru][t][tr ru Rybkin]')
        file = GameFile('Saboteur II (19xx)(-)[h Crudesoft ru][t][tr ru Rybkin].tap')
        file.getParamsFromTOSECPath('Saboteur II (19xx)(-)[tr ru].tap')
        file.sortModFlags()
        self.assertEqual(file.mod_flags, '[h Crudesoft ru][t][tr ru Rybkin]')

    def test_multipublisher(self):
        file = GameFile('test (19xx)(Your Sinclair - crash - Orion)')
        file.sortPublishers()
        self.assertEqual('crash - Orion - Your Sinclair', file.getPublisher())

if __name__=='__main__':
    unittest.main()