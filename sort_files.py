from classes.game import *
from classes.game_file import *
from classes.database import *
from classes.sorter import *
import argparse

if __name__=='__main__':
    input_locations = ['ftp/pub/sinclair/games', 'ftp/zxdb', 'tosec']
    # input_locations = ['ftp/pub/sinclair/utils']
    input_locations = ['tosec']
    # s = Sorter(input_locations=input_locations,
    #            output_location='sorted/sorted_by_publisher',
    #            output_folder_structure='{Publisher}',
    #            ignore_alternate=False,
    #            # short_filenames=True,
    #            files_per_folder=255,
    #            cache=True)
    s = Sorter()
    s.sortFiles()