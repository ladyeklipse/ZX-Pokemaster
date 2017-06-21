from scrape_tosec import *
from classes.database import *
import unittest

class TestScrapingTOSEC(unittest.TestCase):

    def test_adding_distribution_denied_game(self):
        paths = [
            'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game).zip',
            'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game)[a].zip',
            'tosec_games\[TAP]\Alien 8 (1985)(Ultimate Play The Game)[t IQ Soft].zip',
        ]
        scrapeTOSEC(paths)
        db = Database()
        game = db.getGameByWosID(9302)
        for file in game.files:
            if file.format=='tap':
                self.assertGreater(file.size, 0)

