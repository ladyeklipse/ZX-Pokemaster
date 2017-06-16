from classes.game import *
from classes.wos_scraper import *
import unittest
import os

class PokReader(unittest.TestCase):

    def test_find_ambiguous_pok_file(self):
        expected_pok_file_basename = 'Invaders (1983)(DK\'Tronics)(16k).pok'
        game = Game('Invaders', wos_id=2531)
        ws = WosScraper()
        ws.scrapeGameData(game)
        self.assertEqual(game.publisher, 'DK\'Tronics')
        pok_file_path = game.findPokFile()
        print(pok_file_path)
        self.assertEqual(os.path.basename(pok_file_path), expected_pok_file_basename)

    def test_pok_import(self):
        game = Game(name="Ghost Hunters", wos_id=9350)
        game.importPokFile()
        self.assertEqual(len(game.cheats), 22)
        first_cheat = game.cheats[0]
        last_cheat = game.cheats[-1]
        self.assertEqual(first_cheat.name, 'Infinite Energy')
        self.assertEqual(last_cheat.name, 'You don\'t need shoe (You see the EXIT)')
        self.assertEqual(len(first_cheat.pokes), 1)
        first_cheat_poke = first_cheat.pokes[0]
        self.assertEqual(first_cheat_poke.address, 55510)
        self.assertEqual(first_cheat_poke.value, 0)
        self.assertEqual(first_cheat_poke.memory_bank, 8)
        last_cheat_poke = last_cheat.pokes[0]
        self.assertEqual(last_cheat_poke.address, 44842)
        self.assertEqual(last_cheat_poke.value, 130)
        self.assertEqual(last_cheat_poke.memory_bank, 8)

    def test_pok_from_text(self):
        game = Game(name='Test game', wos_id=99999)
        pok_file_contents ="""
NCheat 1
Z 8 22222 120 0
NCheat 2
M 8 22223 120 12
M 7 22225 220 0
Z 8 22226 120 0
Y
        """.strip()
        game.importPokFile(text=pok_file_contents)
        self.assertEqual(len(game.cheats), 2)
        self.assertEqual(len(game.cheats[1].pokes), 3)
        self.assertEqual(game.cheats[1].pokes[1].address, 22225)
        self.assertEqual(game.cheats[1].pokes[1].value, 220)
        self.assertEqual(game.cheats[1].pokes[-1].address, 22226)
        self.assertEqual(game.cheats[1].pokes[-1].value, 120)
        game.exportPokFile('test.pok')
        with open('test.pok', 'r') as f:
            contents = f.read()
            self.assertEqual(contents, pok_file_contents)
