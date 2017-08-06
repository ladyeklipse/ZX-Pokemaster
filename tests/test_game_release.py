from classes.game import Game
from classes.game_release import *
import  unittest
if (os.getcwd().endswith('tests')):
    os.chdir('..')

class TestGameRelease(unittest.TestCase):

    def __init__(self, *args, **kwargs):
        super(TestGameRelease, self).__init__(*args, **kwargs)


    def test_colon_in_name(self):
        g = Game('Ace 2: Combat')
        r = GameRelease(game=g)
        self.assertEqual(r.getTOSECName(), 'Ace 2 - Combat (19xx)(-)')

    def test_aliases(self):
        g = Game('Saboteur II')
        r = GameRelease(game=g)
        r.addAliases(['Saboteur II', 'Saboteur 2 - The Avenging Angel'])
        aliases = r.getAllAliases()
        self.assertEqual(aliases[0], 'Saboteur II')

    # def test_search_string(self):
    #     game = Game('La Abadia Del Crimen')
    #     release = GameRelease(game=game)
    #     search_string = release.getSearchString()
    #     self.assertEqual(search_string, 'abadiadelcrimen')
    #     game = Game('Abadia Del Crimen, La')
    #     release = GameRelease(game=game)
    #     search_string = release.getSearchString()
    #     self.assertEqual(search_string, 'abadiadelcrimen')
