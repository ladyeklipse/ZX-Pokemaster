from classes.sorter import *
import unittest
import shutil
import os
if (os.getcwd().endswith('tests')):
    os.chdir('..')
print(os.getcwd())

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
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(MCM Software)(es)[128K].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K][m].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K][a].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K][a2].tzx'
        self.assertTrue(os.path.exists(expected_file))

    def test_picking_best_candidate(self):
        s = Sorter(input_locations=['tests/sort_best_candidates_in'],
                   output_location='tests/sort_best_candidates_out',
                   output_folder_structure='',
                   formats_preference=['tap', 'z80', 'dsk', 'trd'],
                   ignore_alternate=True,
                   ignore_alternate_formats=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_best_candidates_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_best_candidates_out/3D Master Game (1983)(Supersoft Systems).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_best_candidates_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].z80'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/sort_best_candidates_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].tzx'
        self.assertFalse(os.path.exists(not_expected_file))
        not_expected_file = 'tests/sort_best_candidates_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K][a].z80'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_ignoring_alternate_formats(self):
        #This is format preference for DivIDE firmwares, which have poor TZX support. TZX files will be ignored
        #unless the game is available only in TZX format.
        s = Sorter(input_locations=['tests/sort_best_candidates_in'],
                   output_location='tests/sort_ignoring_alternate_formats_out',
                   output_folder_structure='',
                   formats_preference=['tap', 'z80', 'dsk', 'trd', 'tzx'],
                   ignore_alternate=True,
                   ignore_alternate_formats=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_ignoring_alternate_formats_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_ignoring_alternate_formats_out/3D Master Game (1983)(Supersoft Systems).z80'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/sort_ignoring_alternate_formats_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].tzx'
        self.assertFalse(os.path.exists(not_expected_file))
        not_expected_file = 'tests/sort_ignoring_alternate_formats_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].z80'
        self.assertFalse(os.path.exists(not_expected_file))
        not_expected_file = 'tests/sort_ignoring_alternate_formats_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K][a].z80'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_sorting_unzipped_files(self):
        s = Sorter(input_locations=['tests/sort_unzipped_in'],
                   output_location='tests/sort_unzipped_out',
                   output_folder_structure='',
                   ignore_alternate=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests\sort_unzipped_out\ZXMASTER (19xx)(-).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests\sort_unzipped_out\Race, The (1990)(Players Premier).z80'
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
        expected_file = 'tests/sort_unknown_files_out/Unknown Games/Rebit Soft Bank/it/19xx/Air Fire (19xx)(Rebit Soft Bank)(it).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_unknown_files_out/Electronic Magazine\Alchemist Research\en\\1991/Alchemist News - Issue 01 (1991)(Alchemist Research).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_unknown_files_out/Electronic Magazine\Alchemist Research\en\\1992/Alchemist News - Issue 02 (1992)(Alchemist Research).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_unknown_files_out/Electronic Magazine\Alchemist Research\en\\1993/Alchemist News - Issue 09 (1993)(Alchemist Research)[128K].z80'
        self.assertTrue(os.path.exists(expected_file))

    def test_doublesided_archive(self):
        s = Sorter(input_locations=['tests/sort_doublesided_in'],
                   output_location='tests/sort_doublesided_out',
                   output_folder_structure='',
                   ignore_alternate=False,
                   cache=True)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_doublesided_out/Arkos (1988)(Zigurat Software)(es)(Part 1 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_doublesided_out/Arkos (1988)(Zigurat Software)(es)(Part 2 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_doublesided_out/Arkos (1988)(Zigurat Software)(es)(Part 3 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_doublesided_out/Fourth Protocol, The (1985)(Hutchinson Computer Publishing)(Part 1 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_ignore_rereleases(self):
        s = Sorter(input_locations=['tests/sort_ignore_rereleases_in'],
                   output_location='tests/sort_ignore_rereleases_out',
                   output_folder_structure='',
                   ignore_rereleases=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_ignore_rereleases_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].tzx'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/sort_ignore_rereleases_out/Abadia del Crimen, La (1988)(MCM Software)(es)[128K].tzx'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_ignore_hacks(self):
        s = Sorter(input_locations=['tests/sort_ignore_hacks_in'],
                   output_location='tests/sort_ignore_hacks_out',
                   output_folder_structure='',
                   ignore_hacks=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_ignore_hacks_out/Abadia del Crimen, La (1988)(Opera Soft)(es)[128K].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_ignore_hacks_out/Abadia del Crimen, La (1988)(MCM Software)(es)[128K].tzx'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/sort_ignore_hacks_out/Abadia del Crimen, La (1988)(Opera Soft)(ES)[128K][m].tzx'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_winfriendly_filenames(self):
        s = Sorter(input_locations=['tests/sort_winfriendly_in'],
                   output_location='tests/sort_winfriendly_out',
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_winfriendly_out/19 Part 1 - Boot Camp (1988)(Cascade Games)[48-128K].tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_permission_denied(self):
        s = Sorter(input_locations=['tests/sort_permission_denied_in'],
                   output_location='tests/sort_permission_denied_out',
                   output_folder_structure='',
                   cache=False)
        s.sortFiles()
        expected_file = 'tests/sort_permission_denied_out/19 Part 1 - Boot Camp (1988)(Cascade Games)[48-128K].tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_sort_false_alt(self):
        s = Sorter(
                   input_locations=['tests/sort_false_alt_in'],
                   output_location='tests/sort_false_alt_out',
                   formats_preference='tap,dsk,z80,sna,tzx,trd'.split(','),
                   ignore_alternate_formats=True,
                   ignore_alternate=False,
                   ignore_rereleases=False,
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_false_alt_out/Dizzy Elusive (19xx)(Jura)(ru).trd'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/sort_false_alt_out/Dizzy Elusive (19xx)(Jura)[a].trd'
        self.assertFalse(os.path.exists(not_expected_file))
        not_expected_file = 'tests/sort_false_alt_out/Dizzy Elusive (19xx)(Jura)(ru)[a].trd'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_sorting_multilang_games(self):
        s = Sorter(
                   input_locations=['tests/sort_multilang_in'],
                   output_location='tests/sort_multilang_out',
                   formats_preference='tap,dsk,z80,sna,tzx,trd'.split(','),
                   ignore_alternate_formats=True,
                   ignore_alternate=True,
                   ignore_rereleases=True,
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        #Bug-eyes has both English and Italian versions, should retain both
        expected_file = 'tests/sort_multilang_out/Bug-Eyes (1985)(Icon Software)(it).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_multilang_out/Bug-Eyes (1985)(Icon Software).z80'
        self.assertTrue(os.path.exists(expected_file))
        #Drazen Petrovic Basket has only spanish version.
        expected_file = 'tests/sort_multilang_out/Drazen Petrovic Basket (1989)(Topo Soft)(es)[48-128K].tap'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/sort_multilang_out/Drazen Petrovic Basket (1989)(Topo Soft)[48-128K].tap'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_sorting_multipart_games(self):
        s = Sorter(
                   input_locations=['tests/sort_multipart_in'],
                   output_location='tests/sort_multipart_out',
                   formats_preference=['tap', 'z80'],
                   ignore_alternate_formats=True,
                   ignore_alternate=True,
                   ignore_rereleases=True,
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_multipart_out/Arkos (1988)(Zigurat Software)(es)(Part 1 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_multipart_out/Arkos (1988)(Zigurat Software)(es)(Part 2 of 3).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_multipart_out/Arkos (1988)(Zigurat Software)(es)(Part 3 of 3).z80'
        self.assertTrue(os.path.exists(expected_file))

    def test_sorting_extremely_long_filename(self):
        s = Sorter(
                   input_locations=['tests/sort_extremely_long_in'],
                   output_location='tests/sort_extremely_long_out',
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_extremely_long_out/Maritrini, Freelance Monster Slayer en - Las Increibles Vicisitudes de Despertarse Resacosa con Fred  (2012)(The Mojon Twins)(es).tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_saboteur_2(self):
        s = Sorter(
                   input_locations=['tests/sort_saboteur_in'],
                   output_location='tests/sort_saboteur_out',
                   output_folder_structure='',
                   ignore_alternate_formats=True,
                   ignore_alternate=True,
                   ignore_rereleases=True,
                   ignore_hacks=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_saboteur_out/Saboteur II (1987)(Durell Software).tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_two_disks_two_sides(self):
        s = Sorter(
                   input_locations=['tests/sort_two_disks_two_sides_in'],
                   output_location='tests/sort_two_disks_two_sides_out',
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/sort_two_disks_two_sides_out/Epyx 21 (1990)(US Gold)(Disk 2 of 2).dsk'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_two_disks_two_sides_out/Epyx 21 (1990)(US Gold)(Disk 1 of 2)(Side A).dsk'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/sort_two_disks_two_sides_out/Epyx 21 (1990)(US Gold)(Disk 1 of 2)(Side B).dsk'
        self.assertTrue(os.path.exists(expected_file))

