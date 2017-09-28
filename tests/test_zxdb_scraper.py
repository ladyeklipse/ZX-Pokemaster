from classes.zxdb_scraper import *
from classes.database import *
import unittest

zxdb = ZXDBScraper()
db = Database()

class TestZXDBScraper(unittest.TestCase):

    def test_crime_busters(self):
        where_clause = 'AND entries.id=1155'
        games = zxdb.getGames(where_clause)
        for game in games:
            for release in game.releases:
                release.getInfoFromLocalFiles()
            db.addGame(game)
        db.commit()
        game = db.getGameByWosID(1155)
        self.assertTrue(len(game.releases[0].aliases), 2)
        self.assertTrue('Crime Busters' in game.releases[0].aliases)
        for file in game.getFiles():
            if file.md5=='c358b7b95459f583c9e2bc11d9830d68':
                self.assertGreater(len(file.wos_path), 0)
                self.assertGreater(len(file.wos_name), 0)


    def test_multirelease_game(self):
        where_clause = 'AND entries.id=4'
        games = zxdb.getGames(where_clause)
        game = games[0]
        for release in game.releases:
            release.getInfoFromLocalFiles()
        self.assertEqual(len(game.releases), 4)
        db.addGame(games[0])
        db.commit()
        game = db.getGameByWosID(4)
        self.assertEqual(len(game.releases), 4)
        print(game.releases)

    def test_square_brackets_elimination(self):
        where_clause = 'AND entries.id = 26303'
        games = zxdb.getGames(where_clause)
        for game in games:
            for release in game.releases:
                release.getInfoFromLocalFiles()
        db.addGame(games[0])
        db.commit()
        game = db.getGameByWosID(26303)
        release = game.releases[0]
        self.assertEqual(release.publisher, "Load 'n' Run")
        self.assertIn('Tombola', release.aliases)
        self.assertNotIn('Tombola [2]', release.aliases)

    def test_crc32_and_sha1_hashes(self):
        where_clause = 'AND entries.id = 10'
        games= zxdb.getGames(where_clause)
        for release in games[0].releases:
            release.getInfoFromLocalFiles()
        db.addGame(games[0])
        db.commit()
        game = db.getGameByWosID(10)
        for file in game.getFiles():
            self.assertGreater(len(file.crc32), 0)
            self.assertGreater(len(file.sha1), 0)

    def test_games_with_format_mismatch(self):
        where_clause = 'AND entries.id = 26541'
        games= zxdb.getGames(where_clause)
        for release in games[0].releases:
            release.getInfoFromLocalFiles()
        db.addGame(games[0])
        db.commit()
        game = db.getGameByWosID(26541)
        for file in game.getFiles():
            if file.md5 == '4c279cc851f59bcffffd6a34c7236b75':
                self.assertEqual(file.format, 'z80')

    def test_multiplayer_type(self):
        where_clause = 'AND entries.id = 30265'
        games = zxdb.getGames(where_clause)
        for release in games[0].releases:
            release.getInfoFromLocalFiles()
        db.addGame(games[0])
        db.commit()
        game = db.getGameByWosID(30265)
        self.assertEqual(game.getMultiplayerType(), 'Vs')

    def test_side(self):
        where_clause = 'AND entries.id = 5856'
        games = zxdb.getGames(where_clause)
        for release in games[0].releases:
            release.getInfoFromLocalFiles()
        wos_names = [file.wos_name for file in games[0].getFiles()]
        self.assertIn('Zip-Zap - Alternate - Side 1.tzx', wos_names)
        self.assertIn('Zip-Zap - Alternate - Side 2.tzx', wos_names)
        db.addGame(games[0])
        db.commit()
        game = db.getGameByWosID(5856)
        wos_names = [file.wos_name for file in game.getFiles()]
        self.assertIn('Zip-Zap - Alternate - Side 1.tzx', wos_names)
        self.assertIn('Zip-Zap - Alternate - Side 2.tzx', wos_names)

    def test_home_computer_club_the(self):
        where_clause = 'AND entries.id = 22695'
        games = zxdb.getGames(where_clause)
        self.assertEqual(games[0].getPublisher(), 'Home Computer Club, The')
        for release in games[0].releases:
            self.assertEqual(release.getPublisher(), 'Home Computer Club, The')

    def test_3d_games(self):
        where_clause = 'AND entries.id = 25677'
        games = zxdb.getGames(where_clause)
        aliases = games[0].releases[0].getAllAliases()
        self.assertEqual(aliases, ['3D Plotter', 'Technical Drawing'])
        where_clause = 'AND entries.id = 5140'
        games = zxdb.getGames(where_clause)
        aliases = games[0].releases[2].getAllAliases()
        self.assertEqual(aliases, ['3D-Tanx', '3D Tanks'])

    def test_multitape_game(self):
        where_clause = 'AND entries.id = 11433'
        games = zxdb.getGames(where_clause)
        release = games[0].releases[0]
        release.getInfoFromLocalFiles()
        for file in release.files:
            self.assertGreater(file.part, 0)

    def test_sanitizing_alias(self):
        alias = 'Jet Set Willy (again)'
        new_alias = zxdb.sanitizeAlias(alias)
        game = Game(new_alias)
        self.assertEqual(game.name, 'Jet Set Willy - Again')

    def test_alt_content_desc(self):
        where_clause = 'AND entries.id IN (30155, 11170)'
        games = zxdb.getGames(where_clause)
        for game in games:
            for release in game.releases:
                release.getInfoFromLocalFiles()
            game.setContentDescForZXDBFiles(zxdb.manually_corrected_content_descriptions)
            for file in game.getFiles():
                if game.wos_id==30155:
                    self.assertGreater(len(file.content_desc), 0)
                else:
                    self.assertEqual(len(file.content_desc), 0)

    def test_file_release_date(self):
        where_clause = 'AND entries.id = 20176'
        games = zxdb.getGames(where_clause)
        for game in games:
            for release in game.releases:
                release.getInfoFromLocalFiles()
        game.setContentDescForZXDBFiles(zxdb.manually_corrected_content_descriptions)
        for file in game.getFiles():
            self.assertEqual(file.release_date, '')
        db.addGame(game)
        db.commit()
        game = db.getGameByWosID(20176)
        for file in game.getFiles():
            self.assertNotEqual(file.content_desc, '')
            self.assertEqual(file.release_date, '')

    def test_authors_as_publishers(self):
        where_clause = 'AND entries.id IN (30155, 21575, 7727)'
        games = zxdb.getGames(where_clause)
        for game in games:
            if game.wos_id == 30155:
                self.assertEqual(game.publisher, 'Grussu, Alessandro')
            elif game.wos_id == 21575:
                self.assertEqual(game.publisher, 'Owen, Andrew')
            elif game.wos_id == 7727:
                self.assertEqual(game.publisher, 'Mad Max')

    def test_downloading(self):
        where_clause = 'AND entries.id IN (24888)'
        games = zxdb.getGames(where_clause)
        zxdb.downloadMissingFilesForGames(games)

