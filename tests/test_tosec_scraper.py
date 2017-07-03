from classes.tosec_scraper import *
import  unittest
if (os.getcwd().endswith('tests')):
    os.chdir('..')

class TestTOSECScraper(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestTOSECScraper, self).__init__(*args, **kwargs)

    def test_abadia_del_crimen(self):
        self.ts = TOSECScraper(cache=False)
        paths = self.ts.generateTOSECPathsArray()
        self.ts.paths = [path for path in paths if 'Abadia del Crimen' in path]
        # self.ts.paths = [
        #     'tosec\Games\[DSK]\Abadia del Crimen, La (1988)(Opera Soft)(es).zip'
        # ]
        sql = 'DELETE FROM game_file WHERE game_wos_id=47 AND (wos_name="" OR wos_name IS NULL)'
        self.ts.db.execute(sql)
        self.ts.db.commit()
        self.ts.db.loadCache()
        self.ts.scrapeTOSEC()
        unscraped = self.ts.showUnscraped()
        self.assertEqual(len(unscraped), 0)

    def test_aknadach(self):
        self.ts = TOSECScraper(cache=False)
        paths = [
            "tosec\Games\[Z80]\Aknadach (1990)(Proxima Software)(cs)[128K].zip"
            ]
        sql = 'DELETE FROM game_file WHERE game_wos_id=133 AND (wos_name="" OR wos_name IS NULL)'
        self.ts.db.execute(sql)
        self.ts.db.commit()
        self.ts.db.loadCache()
        self.ts.paths = paths
        self.ts.scrapeTOSEC()
        unscraped = self.ts.showUnscraped()
        self.assertEqual(len(unscraped), 0)