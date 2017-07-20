from classes.tosec_scraper import *
import  unittest
if (os.getcwd().endswith('tests')):
    os.chdir('..')

ts = TOSECScraper(cache=False)

class TestTOSECScraper(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTOSECScraper, self).__init__(*args, **kwargs)

    def test_abadia_del_crimen(self):
        paths = ts.generateTOSECPathsArray()
        ts.paths = [path for path in paths if 'Abadia del Crimen' in path]
        self.scrape(paths, 47)

    def test_aknadach(self):
        paths = [
            "tosec\Games\[Z80]\Aknadach (1990)(Proxima Software)(cs)[128K].zip"
            ]
        self.scrape(paths, 133)

    def test_100_km(self):
        paths = [
            "tosec\Games\[TZX]\\100 km Race (19xx)(Coyote Software).zip",
            "tosec\Games\[Z80]\\100 km Race (19xx)(Coyote Software).zip"
        ]
        wos_id = 10
        self.scrape(paths, wos_id)
        game = ts.db.getGameByWosID(wos_id)
        self.assertTrue(len(game.getFiles())>=2)
        for file in game.getFiles():
            self.assertGreater(len(file.crc32), 0)
            self.assertGreater(len(file.sha1), 0)

    def test_saboteur_2(self):
        paths = [
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1989)(Encore)[re-release].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Erbe Software)(Side A)[re-release].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Erbe Software)(Side B)[re-release].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Erbe Software)[re-release].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)(pl)[a].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software).zip",
            "tosec\Games\[TAP]\Saboteur II - Avenging Angel (1987)(Durell Software).zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software).zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[128K].zip",
            "tosec\Games\[TAP]\Saboteur II - Avenging Angel (1987)(Durell Software)[128K].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[128K].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a2].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a2].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a2][128K].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a2][128K].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a3].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a3].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a3][128K].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a4].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a].zip",
            "tosec\Games\[TAP]\Saboteur II - Avenging Angel (1987)(Durell Software)[a].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a].zip",
            "tosec\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a][128K].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a][128K].zip",
            "tosec\Games\[TAP]\Saboteur II - Avenging Angel (1987)(Durell Software)[cr Wixet][t +2 Wixet][128K].zip",
            "tosec\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[t].zip",
        ]
        wos_id = 4295
        self.scrape(paths, wos_id)
        game = ts.db.getGameByWosID(wos_id)
        self.assertTrue(len(game.getFiles())>=2)
        for file in game.getFiles():
            if 'Durell Software' in file.tosec_path:
                self.assertEqual(file.getReleaseSeq(), 0)

    def test_dat_files_scraping(self):
        wos_id = 9
        sql = 'DELETE FROM game_file WHERE game_wos_id={} AND (wos_name="" OR wos_name IS NULL)'.format(wos_id)
        ts.db.execute(sql)
        sql = 'UPDATE game_file SET tosec_path="" WHERE game_wos_id={}'.format(wos_id)
        ts.db.execute(sql)
        ts.db.commit()
        ts.db.loadCache()
        dat_files = ['tests/Sinclair ZX Spectrum - Games - [TAP] (test).dat',
                     'tests/Sinclair ZX Spectrum - Games - [TZX] (test).dat',
                     ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()
        unscraped = ts.showUnscraped()
        self.assertEqual(len(unscraped), 0)


    def scrape(self, paths, wos_id):
        sql = 'DELETE FROM game_file WHERE game_wos_id={} AND (wos_name="" OR wos_name IS NULL)'.format(wos_id)
        ts.db.execute(sql)
        ts.db.commit()
        ts.db.loadCache()
        ts.paths = paths
        ts.scrapeTOSEC()
        unscraped = ts.showUnscraped()
        self.assertEqual(len(unscraped), 0)
