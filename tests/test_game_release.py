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
        self.assertEqual('Saboteur II', aliases[0])

    def test_badanov_bug(self):
        g = Game('Треугольник')
        r = GameRelease(game=g)
        self.assertEqual(["Треугольник"], r.aliases)
        g = Game('3угольник')
        r = GameRelease(game=g)
        self.assertEqual(["3угольник"], r.aliases)
        g = Game('Минидрайвер дисковых операций')
        r = GameRelease(game=g)
        aliases = r.getAllAliases()
        self.assertEqual(aliases, ['Минидрайвер дисковых операций'])