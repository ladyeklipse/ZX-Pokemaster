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

    def scrape(self, paths, wos_id):
        sql = 'DELETE FROM game_file WHERE game_wos_id={} AND (wos_name="" OR wos_name IS NULL)'.format(wos_id)
        ts.db.execute(sql)
        ts.db.commit()
        ts.db.loadCache()
        ts.paths = paths
        ts.scrapeTOSEC()
        unscraped = ts.showUnscraped()
        self.assertEqual(len(unscraped), 0)
