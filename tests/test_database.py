from classes.database import *
from classes.game import *
from classes.game_file import *
from classes.wos_scraper import *
from classes.tipshop_scraper import *
import  unittest
if (os.getcwd().endswith('tests')):
    os.chdir('..')

class TestDatabase(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestDatabase, self).__init__(*args, **kwargs)
        self.db = Database()

    # def test_adding_game(self):
    #     game = Game(name='Tujad', wos_id=5448)
    #     ws = WosScraper()
    #     ws.scrapeGameData(game)
    #     game.getInfoFromLocalFiles()
    #     ts = TipshopScraper()
    #     ts.scrapePokes(game)
    #     self.db.addGame(game)
    #     self.db.commit()

    def test_adding_broken_wos_id(self):
        game = Game()
        with self.assertRaises(Exception):
            self.db.addGame(game)

    def test_getting_game_by_wos_id(self):
        game = self.db.getGameByWosID(5448)
        self.check_if_game_is_tujad(game)

    def check_if_game_is_tujad(self, game):
        self.assertEqual(game.name, 'Tujad')
        self.assertEqual(game.publisher, 'Ariolasoft UK')
        self.assertEqual(game.year, 1986)
        self.assertEqual(game.number_of_players, 1)
        self.assertEqual(game.genre, 'Arcade: Maze')
        self.assertEqual(game.machine_type, '48K')
        self.assertTrue(len(game.getFiles())>0)
        self.assertEqual(game.getRemoteLoadingScreenUrl('scr'),
                         'http://www.worldofspectrum.org/pub/sinclair/screens/load/t/scr/Tujad.scr')
        self.assertEqual(game.getRemoteLoadingScreenUrl('gif'),
                         'http://www.worldofspectrum.org/pub/sinclair/screens/load/t/gif/Tujad.gif')
        self.assertEqual(game.getRemoteIngameScreenUrl('gif'),
                         'http://www.worldofspectrum.org/pub/sinclair/screens/in-game/t/Tujad.gif')
        self.assertEqual(game.getRemoteManualUrl(), 'http://www.worldofspectrum.org/pub/sinclair/games-info/t/Tujad.txt')

    def test_getting_game_by_md5(self):
        file = GameFile('ftp/pub/sinclair/games/t/Tujad.tap.zip')
        # md5_zipped = 'c603e4d7b60561c7f88036a89d84b950'
        # self.assertEqual(md5_zipped, file.getMD5(zipped=True))
        # game = self.db.getGameByFileMD5(file.getMD5(zipped=True), zipped=True)
        # self.check_if_game_is_tujad(game)
        # file = GameFile('wos_games/t/TUJAD.TAP')
        md5 = '200c35cb8984a40257dd8b317263d752'
        self.assertEqual(md5, file.getMD5(zipped=False))
        game = self.db.getGameByFileMD5(file.getMD5(zipped=False))
        self.check_if_game_is_tujad(game)

    # def test_getting_all_games(self):
    #     games = self.db.getAllGames()
    #     for game in games:
    #         if game.name=='Tujad':
    #             self.check_if_game_is_tujad(game)
    #             break

    def test_importing_corrupt_pok_file(self):
        game = self.db.getGameByWosID(26046)
        self.assertEqual(len(game.cheats), 0)

    def test_getting_game_by_file_name(self):
        filename = '66 (19xx)(Stankinsoft)(de).zip'
        game = self.db.getGameByFileName(filename)
        self.assertEqual(game.wos_id, 39)
        filename = "Giant's Revenge (1984)(Thor Computer Software).zip"
        game = self.db.getGameByFileName(filename)
        self.assertEqual(game.wos_id, 2040)

    # def test_appending_tosec_file_info(self):
    #     filename = "Gonzzalezz (1989)(Opera Soft)(es)(Side B).zip"
    #     file_path = os.path.join('tosec_games', '[TAP]', filename)
    #     game_file = GameFile(file_path)
    #     file_md5_zipped = game_file.getMD5(zipped=True)
    #     print(file_md5_zipped)
    #     game = self.db.getGameByFileMD5(file_md5_zipped, zipped=True)
    #     self.assertEqual(game.wos_id, 2097)

    # def test_adding_multipart_files(self):
    #     game = Game('19 Part 1: Boot Camp', 16)
    #     game.getInfoFromDB(self.db)
        # ws = WosScraper()
        # ws.scrapeGameData(game)
        # ws.downloadFiles(game)
        # game.getInfoFromLocalFiles()
        # self.db.addGame(game)
        # self.db.commit()
        # game = Game('19 Part 1: Boot Camp', 16)
        # game.getInfoFromDB(self.db)
        # self.assertEqual(len(game.files), 7)
        # file = self.get_file_from_game_by_wos_name(game, '19 Part 1 - Boot Camp - Side A.tzx')
        # self.assertEqual(file.wos_name, '19 Part 1 - Boot Camp - Side A.tzx')
        # self.assertEqual(file.md5, '33ab1b76b8fd735299c10307981a912e')
        # self.assertEqual(file.md5_zipped, 'e2a767c63a268fb2794de50fc5e60f3a')
        # file = self.get_file_from_game_by_wos_name(game, '19 Part 1 - Boot Camp - Side B.tzx')
        # self.assertEqual(file.wos_name, '19 Part 1 - Boot Camp - Side B.tzx')
        # self.assertEqual(file.md5, 'bf2b3dbae671bbaf10b6c94b712c4ed8')
        # self.assertEqual(file.md5_zipped, 'e2a767c63a268fb2794de50fc5e60f3a')
        # for file in game.files:
        #     self.assertEqual(file.machine_type, '')
        #     self.assertEqual(file.language, '')

    def test_game_by_filename(self):
        gamefile = GameFile('tosec_games/[TAP]/Alien 8 (1985)(Ultimate Play The Game).zip')
        game = self.db.getGameByFile(gamefile)
        self.assertEqual(game.name, 'Alien 8')

    # def test_alta_tension(self):
    #     game = Game('Alta tension', 6)
    #     ws = WosScraper()
    #     ws.scrapeGameData(game)
    #     ws.downloadFiles(game)
    #     game.getInfoFromLocalFiles()
    #     self.db.addGame(game)
    #     self.db.commit()
    #     game = Game('alta tension', 6)
    #     game.getInfoFromDB(self.db)
    #     self.assertGreater(len(game.files), 2)

    def test_jswilly_3(self):
        game_file = GameFile('tosec//Games//[Z80]//Jet Set Willy III (1985)(MB - APG Software).zip')
        game = self.db.getGameByFile(game_file)
        self.assertEqual(game.name, 'JetSet Willy III')

    def get_file_from_game_by_wos_name(self, game, filename):
        for file in game.getFiles:
            if file.wos_name==filename:
                return file

    def test_find_game_file_with_article_and_alias(self):
        game = self.db.getGameByFilePath('Time of the End, The (1986)(Mandarin Software).zip')
        print(game.releases[0].aliases)
        self.assertEqual(game.name, 'Time of the End')
        game = self.db.getGameByFilePath('Zipper Flipper (1984)(R.E.D).zip')
        self.assertEqual(game.wos_id, 5857)

    def test_multiple_releases(self):
        game = self.db.getGameByWosID(1)
        self.assertEqual(len(game.releases), 4)
        self.assertEqual(game.releases[0].publisher, 'Domark')
        self.assertEqual(game.releases[1].publisher, 'Erbe Software')
        self.assertEqual(game.releases[2].publisher, 'Musical 1')
        self.assertEqual(game.releases[3].publisher, 'The Hit Squad')

    def test_zzzz(self):
        game_file = GameFile('tosec\Games\[TZX]\Zzzz (1986)(Zenobi Software)[re-release].zip')
        game_file.format = 'tzx'
        game = self.db.getGameByFile(game_file)
        self.assertEqual(game.name, 'Zzzz')
        self.assertEqual(len(game.releases), 2)
        release = game.findReleaseByFile(GameFile('Zzzz (1986)(Zenobi Software)'))
        self.assertEqual(release.release_seq, 1)
        release = game.findReleaseByFile(GameFile('Zzzz (1986)(Mastertronic)'))
        self.assertEqual(release.release_seq, 0)
        for release in game.releases:
            print(release, release.files)

    def test_9hole_golf(self):
        md5 = '98fa942231a33b03d55f351afb3006fa'
        game = self.db.getGameByFileMD5(md5)
        self.assertEqual(game.name, '9-Hole Golf')
        self.assertEqual(len(game.releases), 1)

if __name__=='__main__':
    t = TestDatabase()
    # t.test_zzzz()
    # t.test_multiple_releases()
    # t.test_9hole_golf()
    t.db.loadCache()
    t.test_zzzz()
    t.test_multiple_releases()
    t.test_9hole_golf()
    # t.test_zzzz()
    # t.test_find_game_file_with_article_and_alias()
    # unittest.main()