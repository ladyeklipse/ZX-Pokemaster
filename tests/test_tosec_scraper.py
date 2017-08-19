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
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Aknadach (1990)(Proxima Software)(cs)[128K].zip"
            ]
        self.scrape(paths, 133)

    def test_100_km(self):
        paths = [
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\\100 km Race (19xx)(Coyote Software).zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\\100 km Race (19xx)(Coyote Software).zip"
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
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1989)(Encore)[re-release].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Erbe Software)(Side A)[re-release].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Erbe Software)(Side B)[re-release].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Erbe Software)[re-release].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)(pl)[a].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software).zip",
            "tosec\Sinclair ZX Spectrum\Games\[TAP]\Saboteur II - Avenging Angel (1987)(Durell Software).zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software).zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TAP]\Saboteur II - Avenging Angel (1987)(Durell Software)[128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a2].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a2].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a2][128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a2][128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a3].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a3].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a3][128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a4].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TAP]\Saboteur II - Avenging Angel (1987)(Durell Software)[a].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TZX]\Saboteur II - Avenging Angel (1987)(Durell Software)[a][128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[a][128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[TAP]\Saboteur II - Avenging Angel (1987)(Durell Software)[cr Wixet][t +2 Wixet][128K].zip",
            "tosec\Sinclair ZX Spectrum\Games\[Z80]\Saboteur II - Avenging Angel (1987)(Durell Software)[t].zip",
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
        dat_files = ['tests/files/Sinclair ZX Spectrum - Games - [TAP] (test).dat',
                     'tests/files/Sinclair ZX Spectrum - Games - [TZX] (test).dat',
                     ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()
        unscraped = ts.showUnscraped()
        self.assertEqual(len(unscraped), 0)

    def test_popeye_collection(self):
        wos_id = 12013
        sql = 'DELETE FROM game_file WHERE game_wos_id={} AND (wos_name="" OR wos_name IS NULL)'.format(wos_id)
        ts.db.execute(sql)
        sql = 'UPDATE game_file SET tosec_path="" WHERE game_wos_id={}'.format(wos_id)
        ts.db.execute(sql)
        ts.db.commit()
        # ts.db.loadCache()
        dat_files = ['tests/files/Sinclair ZX Spectrum - Compilations - Games - [TZX] (test).dat',
                     ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()
        game = ts.db.getGameByWosID(12013)
        for file in game.getFiles():
            print(file.tosec_path, 'content_desc='+file.content_desc, file.md5)
            self.assertGreater(len(file.content_desc), 0)

    def test_1942(self):
        wos_id = 9297
        sql = 'DELETE FROM game_file WHERE game_wos_id={} AND (wos_name="" OR wos_name IS NULL)'.format(wos_id)
        ts.db.execute(sql)
        sql = 'DELETE FROM game WHERE wos_id>9000000'.format(wos_id)
        ts.db.execute(sql)
        sql = 'DELETE FROM game_release WHERE wos_id>9000000'.format(wos_id)
        ts.db.execute(sql)
        sql = 'DELETE FROM game_file WHERE game_wos_id>9000000'.format(wos_id)
        ts.db.execute(sql)
        sql = 'UPDATE game_file SET tosec_path="" WHERE game_wos_id={}'.format(wos_id)
        ts.db.execute(sql)
        ts.db.commit()
        # ts.db.loadCache()
        dat_files = ['tests/files/Sinclair ZX Spectrum - Games - [TZX] (1942).dat',
                     ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()
        game = ts.db.getGameByWosID(wos_id)
        self.assertGreater(len(game.getFiles()), 0)

    def test_ghostbusters(self):
        wos_id = 2025
        sql = 'DELETE FROM game_file WHERE game_wos_id in({}, 14372, 7433) AND (wos_name="" OR wos_name IS NULL)'.format(wos_id)
        ts.db.execute(sql)
        sql = 'DELETE FROM game WHERE wos_id>9000000'.format(wos_id)
        ts.db.execute(sql)
        sql = 'DELETE FROM game_release WHERE wos_id>9000000'.format(wos_id)
        ts.db.execute(sql)
        sql = 'DELETE FROM game_file WHERE game_wos_id>9000000'.format(wos_id)
        ts.db.execute(sql)
        sql = 'UPDATE game_file SET tosec_path="" WHERE game_wos_id={}'.format(wos_id)
        ts.db.execute(sql)
        ts.db.commit()
        # ts.db.loadCache()
        dat_files = ['tests/files/Sinclair ZX Spectrum - Games - [TZX] (Ghostbusters).dat',
                     ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()
        game = ts.db.getGameByWosID(wos_id)
        for release in game.releases:
            if release.release_seq==1:
                self.assertGreater(len(release.files), 0)
            if release.release_seq==4:
                self.assertGreater(len(release.files), 0)

    def test_knight_lore_editor_with_error(self):
        dat_files = [
            'tests/files/Sinclair ZX Spectrum - Applications - [TZX] (Knight Lore Editor).dat',
        ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()
        ts.addUnscraped()
        ts.db.loadCache()
        game = ts.db.getGameByFileMD5('9b70e0851f635a3e9fdef222b5aa62f2')
        self.assertGreater(len(game.getFiles()), 0)

    def test_educational_dats(self):
        dat_files = ['tosec/Sinclair ZX Spectrum - Compilations - Educational - [TRD] (TOSEC-v2011-09-24_CM).dat',
                     ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()
        ts.addUnscraped()
        ts.db.loadCache()
        game = ts.db.getGameByFileMD5('3bb8fca89941bb3b9ad26ae823c15899')
        if not game:
            self.fail()
        self.assertNotEqual(game.wos_id, 0)

    def test_unpacked_files_folder(self):
        ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\lost_and_found')[:20]
        self.assertGreater(len(ts.paths), 0)
        ts.scrapeTOSEC()
        game = ts.db.getGameByFileMD5('4ec946e32464a0fde05bb27728d23b56')

    def test_unknown_genre(self):
        ts.paths = [
            'tosec\\Sinclair ZX Spectrum\Applications\[TAP]\Turbo Load (1988)(Your Sinclair).zip'
        ]
        ts.scrapeTOSEC()
        game = ts.gb.getGameByFileMD5('2911f21ca8af69be1ceff10be53702c6')
        self.assertEqual(game.genre, 'Utilities')

    def test_fikus_pikus(self):
        ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\fikus-pikus\\renamed')
        ts.scrapeTOSEC()
        game = ts.db.getGameByName('Fikus Pikus Games')
        self.assertEqual(game.genre, 'Compilation - Games')
        self.assertGreater(len(game.getFiles()), 200)
        for file in game.getFiles():
            self.assertGreater(file.part, 0)

    def scrape(self, paths, wos_id):
        sql = 'DELETE FROM game_file WHERE game_wos_id={} AND (wos_name="" OR wos_name IS NULL)'.format(wos_id)
        ts.db.execute(sql)
        ts.db.commit()
        ts.db.loadCache()
        ts.paths = paths
        ts.scrapeTOSEC()
        ts.addUnscraped()
        unscraped = ts.showUnscraped()
        self.assertEqual(len(unscraped), 0)
