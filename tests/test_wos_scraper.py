#
#   DEPRECATED
#

from classes.wos_scraper import *
from settings import *
import unittest

class WosScraperTests(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(WosScraperTests, self).__init__(*args, **kwargs)
        self.ws = WosScraper()

    def test_games_list_loading(self):
        print(os.getcwd())
        games_list = self.ws.loadGamesListForLetter('1')
        self.assertFalse(len(games_list)==0)
        self.assertTrue(games_list[0] != None)
        print(games_list)

    def test_missing_in_action(self):
        game = Game('Alpha Conundrum', 19644)
        self.ws.scrapeGameData(game)
        self.assertTrue(game.availability == AVAILABILITY_MISSING_IN_ACTION)

    def test_dist_denied(self):
        game = Game('11-a-Side Soccer', 9296)
        self.ws.scrapeGameData(game)
        self.assertEqual(len(game.files), 0)

    def test_no_game_files(self):
        game = Game('15, The', 16830)
        self.ws.scrapeGameData(game)
        self.assertEqual(len(game.files), 0)

    def test_game_scraping(self):
        game = Game('Tujad', 5448)
        self.ws.scrapeGameData(game)
        # print(game)
        self.assertEqual(game.publisher,'Ariolasoft UK')
        self.assertEqual(game.year,1986)
        self.assertEqual(game.number_of_players,1)
        self.assertEqual(game.genre,'Arcade: Maze')
        self.assertEqual(game.machine_type,'48K')
        self.assertEqual(game.files[0].machine_type, '')
        self.assertEqual(len(game.files), 2)
        self.assertEqual(game.getRemoteLoadingScreenUrl('scr'), 'http://www.worldofspectrum.org/pub/sinclair/screens/load/t/scr/Tujad.scr')
        self.assertEqual(game.loading_screen_scr_size, 6912)
        self.assertEqual(game.getRemoteLoadingScreenUrl('gif'), 'http://www.worldofspectrum.org/pub/sinclair/screens/load/t/gif/Tujad.gif')
        self.assertEqual(game.loading_screen_gif_size, 7394)
        self.assertEqual(game.getRemoteIngameScreenUrl('gif'), 'http://www.worldofspectrum.org/pub/sinclair/screens/in-game/t/Tujad.gif')
        self.assertEqual(game.ingame_screen_gif_size, 4613)
        self.assertEqual(game.getRemoteManualUrl(), 'http://www.worldofspectrum.org/pub/sinclair/games-info/t/Tujad.txt')
        self.assertEqual(game.manual_size, 2726)

    def test_cabal(self):
        game = Game('Cabal', 780)
        self.ws.scrapeGameData(game)
        self.assertEqual(game.year, 1989)
        self.assertEqual(len(game.files), 9)

    def test_local_paths(self):
        g = Game(name='Voidrunner', wos_id=5600)
        self.ws.scrapeGameData(g)
        self.assertEqual(g.getLocalIngameScreenPath(),
                         'wos_ingame_screens\scr\\v\Voidrunner.scr')
        self.assertEqual(g.getLocalLoadingScreenPath(),
                         'wos_loading_screens\scr\\v\Voidrunner.scr')
        self.assertEqual(g.getLocalIngameScreenPath(format='gif'),
                         'wos_ingame_screens\gif\\v\Voidrunner.gif')
        self.assertEqual(g.getLocalLoadingScreenPath(format='gif'),
                         'wos_loading_screens\gif\\v\Voidrunner.gif')
        self.assertEqual(g.getLocalManualPath(),
                         'wos_manuals\\v\Voidrunner.txt')

    def prepare_downloading(self):
        files = [
            'wos_games/V/Voidrunner.tap.zip',
            'wos_games/V/Voidrunner.tzx.zip',
            'wos_ingame_screens/gif/V/Voidrunner.gif',
            'wos_loading_screens/gif/V/Voidrunner.gif',
            'wos_loading_screens/scr/V/Voidrunner.scr',
            'wos_manuals/V/Voidrunner.txt'
        ]
        for file in files:
            if os.path.exists(file):
                os.unlink(file)

    def test_downloading_files(self):
        g = Game(name='Voidrunner', wos_id=5600)
        self.ws.scrapeGameData(g)
        self.ws.downloadFiles(g)
        self.assertTrue(os.path.exists(g.getLocalLoadingScreenPath(format='gif')))
        self.assertEqual(g.loading_screen_gif_size,
                         os.path.getsize(g.getLocalLoadingScreenPath(format='gif')))
        self.assertTrue(os.path.exists(g.getLocalLoadingScreenPath(format='scr')))
        self.assertEqual(g.loading_screen_scr_size,
                         os.path.getsize(g.getLocalLoadingScreenPath(format='scr')))
        self.assertTrue(os.path.exists(g.getLocalIngameScreenPath(format='gif')))
        self.assertEqual(g.ingame_screen_gif_size,
                         os.path.getsize(g.getLocalIngameScreenPath(format='gif')))
        self.assertTrue(os.path.exists(g.getLocalManualPath()))
        # self.assertEqual(g.manual_size,
        #                  os.path.getsize(g.getLocalManualPath()))
        for file in g.files:
            local_path = file.getLocalPath(zipped=True)
            print(local_path)
            self.assertTrue(os.path.exists(local_path))
            self.assertEqual(os.path.getsize(local_path),
                            file.size)

    def test_importing_wos_pokes(self):
        g = Game(name='Voidrunner', wos_id=5600)
        self.ws.scrapeGameData(g)
        g.getInfoFromLocalFiles()
        cheat = g.cheats[0]
        poke = cheat.pokes[0]
        tap_file = g.files[1] #Voidrunner.tap
        self.assertEqual(tap_file.md5_zipped, '526D63D9511BE77E3270D476CB8B9C62'.lower())
        self.assertEqual(tap_file.md5, '620419942A3707C0FC85334DF489DE94'.lower())
        self.assertEqual(poke.address, 39935)
        self.assertEqual(poke.value, 0)
        self.assertEqual(poke.original_value, 61)

    def test_wrong_file(self):
        game = Game(name='Pac-Man Emulator', wos_id=27394)
        self.ws.scrapeGameData(game)
        game.getInfoFromLocalFiles()
        self.assertEqual(len(game.files), 0)

    def test_mod_game_name(self):
        game = Game(name='Big Bad John', wos_id=516)
        self.ws.scrapeGameData(game)
        self.assertEqual(game.name, 'Big Bad John')

    def test_unknown_publisher(self):
        game = Game('Q-Bertus', 3962)
        self.ws.scrapeGameData(game)
        self.assertEqual(game.getPublisher(), '-')

    def test_get_info_from_local_files(self):
        game = Game(name='Breakout', wos_id=690)
        self.ws.scrapeGameData(game)
        game.getInfoFromLocalFiles()

    def test_archives_with_multiple_files(self):
        game = Game('Gonzzalezz', 2097)
        self.ws.scrapeGameData(game)
        game.getInfoFromLocalFiles()
        self.assertTrue(len(game.files), 4)
        print(game.files)

    def test_weird_loading_screen_url(self):
        game = Game('Cueva del Tiempo, La',27409)
        self.ws.scrapeGameData(game)
        self.assertEqual(game.getRemoteLoadingScreenUrl('scr'),
                         'http://www.worldofspectrum.org/pub/sinclair/screens/load/c/scr/CuevaDelTiempoLa.scr')

    def test_time_and_magik(self):
        game = Game('Time and Magik', 11376)
        self.ws.scrapeGameData(game)
        self.assertEqual(len(game.files), 2)

    def test_correct_filename(self):
        game = Game('4krace', 18314)
        self.ws.scrapeGameData(game)
        self.ws.downloadFiles(game)
        game.getInfoFromLocalFiles()
        self.assertEqual(game.files[0].wos_name, '4krace.tap')

    def test_alta_tension(self):
        game = Game('Alta tension', 6)
        self.ws.scrapeGameData(game)
        self.ws.downloadFiles(game)
        game.getInfoFromLocalFiles()
        self.assertGreater(len(game.files), 2)

if __name__=='__main__':
    w = WosScraperTests()
    # w.test_missing_in_action()
    # w.test_dist_denied()
    # w.test_no_game_files()
    # w.test_game_scraping()
    # w.test_prepare_downloading()
    unittest.main()