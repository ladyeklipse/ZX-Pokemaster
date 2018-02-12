import unittest
from functions.game_name_functions import *

class TestFunctions(unittest.TestCase):
    longMessage = True

def make_short_game_name_test(test_number, original, expected):
    def test(self):
        # print(original)
        result = getMeaningfulEightLetterName(original)
        self.assertEqual(expected, result)
    return test

def make_filesystem_friendly_name_test(test_number, original, expected):
    def test(self):
        # print(original)
        result = getFileSystemFriendlyName(original)
        self.assertEqual(expected, result)
    return test

if __name__=='__main__':
    print('Tests started')
    game_names = [
        ('Manic Miner 6 - The Buddha of Suburbia', 'MANIMIN6'),
        ('A B C', 'ABC'),
        ('1994 - Ten Years After', '199TENYE'),
        ('A, B, C ... Lift-Off!', 'ABCLIFTO'),
        ('ABC ... Lift Off!', 'ABCLIFOF'),
        ('d_hard2remade', 'DHARD2RE'),
        ('19 Part 1 - Boot Camp', '19PART1B'),
        ('Virtue da Dirty Soul', 'VIRTDADI'),
        ('Arcade - Action', 'ARCADACT'),
        ('16K Multitasking', '16KMULTI'),
        ('Saboteur II', 'SABOTEU2'),
        ('Licence to Kill', 'LICETOKI'),
        ('Saboteur', 'SABOTEUR'),
        ('Penetrator, The',  'PENETRAT'),
        ('Sport of Kings Challenge, The', 'SPOKINCH'),
        ('Sports Pack, The', 'SPORTPAC'),
        ('Star Fly, The', 'STARFLY'),
        ('Steelyard Blues, The', 'STEELBLU'),
        ('Stimpo Disassembler, The v3.0', 'STIMPDIS'),
        ('Story So Far Vol 4, The - Wonder Boy', 'STORSOFA')
    ]
    for i, game_name in enumerate(game_names):
        test_f = make_short_game_name_test(i, game_name[0], game_name[1])
        setattr(TestFunctions, 'test_short_game_name_%d' % i, test_f)

    game_names = [
        ('jetSet Willy II', 'jetSet Willy II'),
        ('AlchNews 23', 'AlchNews 23')
    ]
    for i, game_name in enumerate(game_names):
        test_f = make_filesystem_friendly_name_test(i, game_name[0], game_name[1])
        setattr(TestFunctions, 'test_winfriendly_game_name_%d' % i, test_f)

    unittest.main()