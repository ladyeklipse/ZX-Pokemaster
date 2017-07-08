from classes.game import *
from classes.game_file import *
from classes.database import *
from classes.sorter import *
import argparse

if __name__=='__main__':
    input_locations = ['ftp', 'tosec']
    input_locations = ['ftp/pub/sinclair/utils']
    input_locations = ['tosec']
    s = Sorter(input_locations=input_locations,
               output_location='sorted',
               ignore_alternate=False,
               cache=True)
    s.sortFiles()