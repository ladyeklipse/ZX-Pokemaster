from classes.game import *
from classes.game_file import *
from classes.database import *
import argparse

def sortFiles(input_locations,
              output_location='sorted',
              store_all_game_files=False,
              formats_preference=['tap', 'z80', 'dsk', 'trd', 'tzx'],
              output_folder_structure='{Genre}/{Year}/{Letter}',
              delete_original_files=False,
              files_per_folder=None):
    pass

if __name__=='__main__':
    sortFiles(['ftp', 'tosec_games'])