from classes.game import *
from classes.game_file import *
from classes.database import *
from classes.sorter import *
import argparse

if __name__=='__main__':
    s = Sorter(input_locations=['ftp', 'tosec'],
               cache=False)
    s.sortFiles()