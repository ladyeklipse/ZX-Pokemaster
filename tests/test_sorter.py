from classes.sorter import *
import unittest
import shutil

class TestSorter(unittest.TestCase):

    def test_sorting_single_file(self):
        s = Sorter(input_locations=['tests/sort_single_file_in'],
                   output_location='tests/sort_single_file_out',
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_single_file_out/Zaxxon (1985)(US Gold).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_single_file_out/POKES/Zaxxon (1985)(US Gold).pok'
        self.assertTrue(os.path.exists(expected_file))
        self.assertGreater(os.path.getsize(expected_file), 0)

    def test_placing_pokes_alongside_files(self):
        s = Sorter(input_locations=['tests/sort_single_file_in'],
                   output_location='tests/sort_single_file_out_2',
                   output_folder_structure='',
                   place_pok_files_in_pokes_subfolders=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_single_file_out_2/Zaxxon (1985)(US Gold).pok'
        self.assertTrue(os.path.exists(expected_file))
        self.assertGreater(os.path.getsize(expected_file), 0)

    def test_all_subfolder_kwargs(self):
        structure = '{Language}/{MachineType}/{NumberOfPlayers}/{Genre}/{Publisher}/{Year}/{Letter}/{GameName}'
        s = Sorter(input_locations=['tests/sort_single_file_in'],
                   output_location='tests/sort_single_file_out_3',
                   output_folder_structure=structure,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_single_file_out_3/en/48K/2P/Arcade - Shoot-em-up/US Gold/1985/z/Zaxxon/Zaxxon (1985)(US Gold).tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_alt_files(self):
        s = Sorter(input_locations=['tests/sort_alt_files_in'],
                   output_location='tests/sort_alt_files_out',
                   output_folder_structure='',
                   ignore_alternate=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es).tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(MCM Software)(es).tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[m].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[a].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[a2].tzx'
        self.assertTrue(os.path.exists(expected_file))

    def test_picking_best_candidate(self):
        #This is format preference for DivIDE firmwares, which have poor TZX support. TZX files will be ignored.
        #In the later version of ZX Pokemaster, this test will be modified to convert TZX to TAP if no other candidates found.
        #This will happen only if there will turn out to be a lot of games which are represented by TZX format only.
        s = Sorter(input_locations=['tests/sort_best_candidates_in'],
                   output_location='tests/sort_best_candidates_out',
                   output_folder_structure='',
                   formats_preference=['tap', 'z80', 'dsk', 'trd'],
                   ignore_alternate=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/3D Master Game (1983)(Supersoft Systems).z80'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es).tzx'
        self.assertFalse(os.path.exists(not_expected_file))
        not_expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es).z80'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_sorting_unzipped_files(self):
        s = Sorter(input_locations=['tests/sort_unzipped_in'],
                   output_location='tests/sort_unzipped_out',
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests\sort_unzipped_out\WordSheep (1984)(ZX Computing).tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_collecting_info_for_files_with_unknown_hashsum(self):
        s = Sorter(input_locations=['tests/sort_unknown_files_in'],
                   output_location='tests/sort_unknown_files_out',
                   output_folder_structure='{Genre}/{Publisher}/{Language}/{Year}',
                   formats_preference=['tap', 'z80', 'dsk', 'trd'],
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_unknown_files_out/Unknown/Rebit Soft Bank/it/19xx/Air Fire (19xx)(Rebit Soft Bank)(it).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_unknown_files_out/Unknown\Alchemist Research\en\\1991/Alchemist News - Issue 01 (1991)(Alchemist Research).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_unknown_files_out/Unknown\Alchemist Research\en\\1992/Alchemist News - Issue 02 (1992)(Alchemist Research).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_unknown_files_out/Unknown\Alchemist Research\en\\1993/Alchemist News - Issue 09 (1993)(Alchemist Research).z80'
        self.assertTrue(os.path.exists(expected_file))



