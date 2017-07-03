from classes.game import Game
from classes.game_release import *
import  unittest
if (os.getcwd().endswith('tests')):
    os.chdir('..')

class TestGameRelease(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGameRelease, self).__init__(*args, **kwargs)

    # def test_search_string(self):
    #     game = Game('La Abadia Del Crimen')
    #     release = GameRelease(game=game)
    #     search_string = release.getSearchString()
    #     self.assertEqual(search_string, 'abadiadelcrimen')
    #     game = Game('Abadia Del Crimen, La')
    #     release = GameRelease(game=game)
    #     search_string = release.getSearchString()
    #     self.assertEqual(search_string, 'abadiadelcrimen')
