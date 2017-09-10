from scripts.restore_db import *
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
        game = ts.db.getGameByFileMD5('2911f21ca8af69be1ceff10be53702c6')
        self.assertEqual(game.genre, 'Utilities')

    def test_fikus_pikus(self):
        sql = 'DELETE FROM game_file WHERE tosec_path LIKE "tosec\\%"'
        ts.db.execute(sql)
        sql = 'DELETE FROM game WHERE name LIKE "Fikus Pikus%" AND wos_id>9000000'
        ts.db.execute(sql)
        sql = 'DELETE FROM game_release WHERE name LIKE "Fikus Pikus%" AND wos_id>9000000'
        ts.db.execute(sql)
        ts.db.commit()
        # ts.db.loadCache()
        ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\ZXAAA Compilations\\Fikus Pikus Games')
        ts.paths = ts.paths[:5]
        ts.scrapeTOSEC()
        ts.addUnscraped()
        game = ts.db.getGameByName('Fikus Pikus Games')
        self.assertEqual(game.genre, 'Compilation - Games')
        self.assertGreater(len(game.getFiles()), 2)
        self.assertGreater(game.parts, 2)
        for file in game.getFiles():
            self.assertEqual(file.getCountry(), 'RU')
            self.assertGreater(file.part, 0)

    def test_missing_files(self):
        dat_files = ['tests/files/Sinclair ZX Spectrum - Games - [Z80] (miss).dat',
                     ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()
        ts.addUnscraped()
        # ts.db.loadCache()
        md5s = [
            'ba78c16a2e6dbb3fdf47a6e23d805a7e',
            'e07dcc8d415684c71f246ffce6ebcf5c',
            '8a859a78004768254db5d0dc98b46414',
            '76065f95ab3d67694f37cf4fd0039790'
        ]
        for md5 in md5s:
            game = ts.db.getGameByFileMD5(md5)
            if not game:
                self.fail()
            self.assertNotEqual(game.wos_id, 0)

    def test_educational(self):
        dat_files = ['tosec/Sinclair ZX Spectrum - Compilations - Educational - [TRD] (TOSEC-v2011-09-24_CM).dat',
                     ]
        ts.paths = ts.generateTOSECPathsArrayFromDatFiles(dat_files)
        ts.scrapeTOSEC()

    def test_mia(self):
        sql = 'DELETE FROM game_file WHERE tosec_path LIKE "tosec\\%"'
        ts.db.execute(sql)
        ts.db.commit()
        ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\mia')
        ts.scrapeTOSEC()
        ts.updateTOSECAliasesCSV()
        ts.addUnscraped()
        ts.db.commit()
        game = ts.db.getGameByFileMD5('dbb91c0fb3a0d583fe14363bd68d3b58')
        self.assertGreater(game.wos_id, 0)

    def test_getting_ext_from_zip_files(self):
        ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\test')
        ts.paths = ts.generateTOSECPathsArrayFromList([
            'tosec\itch.io\Games\Break-Space v1.1 (2017-06-14)(Blerkotron)[BASIC Jam].tap'])
        for path in ts.paths:
            print(path)
            game_file = ts.getGameFileFromFilePathDict(path)
            print('tosec_path=',game_file.tosec_path)
            self.assertTrue(game_file.format in GAME_EXTENSIONS)

    def test_version_as_release(self):
        sql = 'DELETE FROM game_file WHERE game_wos_id=30410 AND (wos_name="" OR wos_name IS NULL)'
        ts.db.execute(sql)
        sql = 'DELETE FROM game WHERE name = "Break-Space" AND wos_id>9000000'
        ts.db.execute(sql)
        sql = 'DELETE FROM game_release WHERE name = "Break-Space" AND wos_id>9000000'
        ts.db.execute(sql)
        ts.db.commit()
        ts.paths = ts.generateTOSECPathsArrayFromList([
            'tosec\itch.io\Games\Break-Space v1.1 (2017-06-14)(Blerkotron)[BASIC Jam].tap'])
        ts.scrapeTOSEC()
        ts.db.commit()
        game = ts.db.getGameByWosID(30410)
        self.assertGreater(len(game.getFiles()), 0)
        for file in game.getFiles():
            self.assertNotEqual(file.content_desc, '')
            self.assertEqual(file.release.year, 2017)
            self.assertEqual(file.release_date, '2017-06-14')

    def test_csscgc(self):
        # ts.db.conn.close()
        # restoreDB()
        # ts.db = Database()
        sql = 'DELETE FROM game_file WHERE game_wos_id=1299 AND notes="[CSSCGC]"'
        ts.db.execute(sql)
        sql = 'DELETE FROM game WHERE name="Car" and publisher="Yates, Damion"'
        ts.db.execute(sql)
        sql = 'DELETE FROM game_release WHERE name="Car" and publisher="Yates, Damion"'
        ts.db.execute(sql)
        ts.db.commit()
        # ts.db.loadCache(force_reload=True)
        ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\csscgc Games test\\')
        ts.scrapeTOSEC()
        ts.addUnscraped()
        ts.db.commit()
        game = ts.db.getGameByWosID(1299)
        for file in game.getFiles():
            self.assertNotIn('[CSSCGC]', file.notes)

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
