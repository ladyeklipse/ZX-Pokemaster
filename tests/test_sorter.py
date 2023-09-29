import os
if (os.getcwd().endswith('tests')):
    os.chdir('..')
print(os.getcwd())

from classes.sorter import *
import unittest
import shutil

class TestSorter(unittest.TestCase):

    def test_sorting_single_file(self):
        s = Sorter(input_locations=['tests/files/sort_single_file_in'],
                   output_location='tests/files/sort_single_file_out',
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_single_file_out/Zaxxon (1985)(U.S. Gold).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_single_file_out/POKES/Zaxxon (1985)(U.S. Gold).pok'
        self.assertTrue(os.path.exists(expected_file))
        self.assertGreater(os.path.getsize(expected_file), 0)
        self.assertEqual(len(s.errors), 0)

    def test_sorting_by_author(self):
        s = Sorter(input_locations=['tests/files/sort_single_file_in'],
                   output_location='tests/files/sort_by_author_out',
                   output_folder_structure='{Author}',
                   output_filename_structure='{GameName} ({Year})({Author})',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_by_author_out/Platinum Productions - Thorpe, F. David/Zaxxon (1985)(Platinum Productions - Thorpe, F. David).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_by_author_out/Platinum Productions - Thorpe, F. David/POKES/Zaxxon (1985)(Platinum Productions - Thorpe, F. David).pok'
        self.assertTrue(os.path.exists(expected_file))
        self.assertGreater(os.path.getsize(expected_file), 0)
        self.assertEqual(len(s.errors), 0)

    def test_placing_pokes_alongside_files(self):
        s = Sorter(input_locations=['tests/files/sort_single_file_in'],
                   output_location='tests/files/sort_single_file_out_2',
                   output_folder_structure='',
                   place_pok_files_in_pokes_subfolders=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_single_file_out_2/Zaxxon (1985)(U.S. Gold).pok'
        self.assertTrue(os.path.exists(expected_file))
        self.assertGreater(os.path.getsize(expected_file), 0)

    def test_all_subfolder_kwargs(self):
        structure = '{Language}/{MachineType}/{MaxPlayers}/{Genre}/{Publisher}/{Year}/{Letter}/{GameName}'
        s = Sorter(input_locations=['tests/files/sort_single_file_in'],
                   output_location='tests/files/sort_single_file_out_3',
                   output_folder_structure=structure,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_single_file_out_3/en/48K/2P/Arcade Game - Shoot-em-up/U.S. Gold/1985/z/Zaxxon/Zaxxon (1985)(U.S. Gold).tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_alt_files(self):
        s = Sorter(input_locations=['tests/files/sort_alt_files_in'],
                   output_location='tests/files/sort_alt_files_out',
                   output_folder_structure='',
                   include_alternate=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_alt_files_out/Abadia del Crimen, La (1988)(MCM)(128K)(es)[re-release].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es)[m].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es)[a].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_alt_files_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es)[a2].tzx'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_picking_best_candidate(self):
        s = Sorter(input_locations=['tests/files/sort_best_candidates_in'],
                   output_location='tests/files/sort_best_candidates_out',
                   output_folder_structure='',
                   include_only=['tap', 'z80', 'dsk', 'trd'],
                   include_filter_on=True,
                   include_alternate=False,
                   include_alternate_formats=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_best_candidates_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_best_candidates_out/3D Master Game (1983)(Supersoft Systems)[aka 3D Noughts and Crosses].z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_best_candidates_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es)[needs tape load].z80'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/files/sort_best_candidates_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).tzx'
        self.assertFalse(os.path.exists(not_expected_file))
        not_expected_file = 'tests/files/sort_best_candidates_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es)[a].z80'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_ignoring_alternate_formats(self):
        #This is format preference for DivIDE firmwares, which have poor TZX support. TZX files will be ignored
        #unless the game is available only in TZX format.
        s = Sorter(input_locations=['tests/files/sort_best_candidates_in'],
                   output_location='tests/files/sort_ignoring_alternate_formats_out',
                   output_folder_structure='',
                   formats_preference=['tap', 'z80', 'dsk', 'trd', 'tzx'],
                   include_alternate=False,
                   include_alternate_formats=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_ignoring_alternate_formats_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_ignoring_alternate_formats_out/3D Master Game (1983)(Supersoft Systems)[aka 3D Noughts and Crosses].z80'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/files/sort_ignoring_alternate_formats_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).tzx'
        self.assertFalse(os.path.exists(not_expected_file))
        not_expected_file = 'tests/files/sort_ignoring_alternate_formats_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).z80'
        self.assertFalse(os.path.exists(not_expected_file))
        not_expected_file = 'tests/files/sort_ignoring_alternate_formats_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es)[a].z80'
        self.assertFalse(os.path.exists(not_expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_sorting_unzipped_files(self):
        s = Sorter(input_locations=['tests/files/sort_unzipped_in'],
                   output_location='tests/files/sort_unzipped_out',
                   output_folder_structure='',
                   include_alternate=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = s.output_location+'\Mastering Machine Code (19xx)(ZX Computing).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = s.output_location+'\Race, The (1990)(Players Premier)(48K-128K).z80'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_collecting_info_for_files_with_unknown_hashsum(self):
        s = Sorter(input_locations=['tests/files/sort_unknown_files_in'],
                   output_location='tests/files/sort_unknown_files_out',
                   output_folder_structure='{Genre}/{Publisher}/{Language}/{Year}',
                   formats_preference=['tap', 'z80', 'dsk', 'trd'],
                   include_unknown_files=True,
                   separate_unknown_files=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_unknown_files_out/Various Games/Rebit Soft Bank/it/19xx/Air Fire (19xx)(Rebit Soft Bank)(it).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = \
            'tests/files/sort_unknown_files_out/Electronic Magazine\Alchemist Research\en\\1991/AlchNews 01 (1991)(Alchemist Research).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_unknown_files_out/Electronic Magazine\Alchemist Research\en\\1992/Alchemist News 02 (1992)(Alchemist Research).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_unknown_files_out/Electronic Magazine\Alchemist Research\en\\1993/Alchemist News 09 (1993)(Alchemist Research)(128K).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_unknown_files_out/Unknown/Unknown Publisher/en/2017/Треугольник (2017).tap'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)
        s.separate_unknown_files = True
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileExists('tests/files/sort_unknown_files_out/Unknown Files/Треугольник (2017).tap')
        self.assertFileExists('tests/files/sort_unknown_files_out/Unknown Files/AlchNews 01 (1991)(Alchemist Research).z80')
        self.assertFileExists('tests/files/sort_unknown_files_out/Unknown Files/AlchNews 01 (1991)(Alchemist Research)_2.z80')
        self.assertEqual(len(s.errors), 0)

    def test_retain_relative_structure(self):
        s = Sorter(input_locations=['tests/files/sort_unknown_files_in'],
                   output_location='tests/files/sort_unknown_files_out_3',
                   output_folder_structure='{Genre}/{Publisher}/{Language}/{Year}',
                   formats_preference=['tap', 'z80', 'dsk', 'trd'],
                   include_unknown_files=True,
                   separate_unknown_files=True,
                   retain_relative_structure=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileExists('tests/files/sort_unknown_files_out_3/Unknown Files/Треугольник (2017).tap')
        self.assertFileExists('tests/files/sort_unknown_files_out_3/Unknown Files/relative_structure/AlchNews 01 (1991)(Alchemist Research).z80')


    def test_doublesided_archive(self):
        s = Sorter(input_locations=['tests/files/sort_doublesided_in'],
                   output_location='tests/files/sort_doublesided_out',
                   output_folder_structure='',
                   include_alternate=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_doublesided_out/Arkos (1988)(Zigurat)(es)(Tape 1 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_doublesided_out/Arkos (1988)(Zigurat)(es)(Tape 2 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_doublesided_out/Arkos (1988)(Zigurat)(es)(Tape 3 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_doublesided_out/Fourth Protocol, The - The Game (1985)(Hutchinson Computer Publishing)(Tape 1 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_ignore_rereleases(self):
        s = Sorter(input_locations=['tests/files/sort_ignore_rereleases_in'],
                   output_location='tests/files/sort_ignore_rereleases_out',
                   output_folder_structure='',
                   include_rereleases=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_ignore_rereleases_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).tzx'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/files/sort_ignore_rereleases_out/Abadia del Crimen, La (1988)(MCM)(128K)(es).tzx'
        self.assertFalse(os.path.exists(not_expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_ignore_hacks(self):
        s = Sorter(input_locations=['tests/files/sort_ignore_hacks_in'],
                   output_location='tests/files/sort_ignore_hacks_out',
                   output_folder_structure='',
                   include_hacks=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_ignore_hacks_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_ignore_hacks_out/Abadia del Crimen, La (1988)(MCM)(128K)(es)[re-release].tzx'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/files/sort_ignore_hacks_out/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es)[m].tzx'
        self.assertFalse(os.path.exists(not_expected_file))

    def test_winfriendly_filenames(self):
        s = Sorter(input_locations=['tests/files/sort_winfriendly_in'],
                   output_location='tests/files/sort_winfriendly_out',
                   output_folder_structure='{Publisher}',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_winfriendly_out/Cascade Games/19 Part 1 - Boot Camp (1988)(Cascade Games)(48K-128K).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_winfriendly_out/David Amigaman/Serpes (2003)(David Amigaman)(es).z80'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_permission_denied(self):
        s = Sorter(input_locations=['tests/files/sort_permission_denied_in'],
                   output_location='tests/files/sort_permission_denied_out',
                   output_folder_structure='',
                   cache=False)
        s.sortFiles()
        expected_file = 'tests/files/sort_permission_denied_out/19 Part 1 - Boot Camp (1988)(Cascade Games)(48K-128K).tap'
        self.assertTrue(os.path.exists(expected_file))

    def test_sort_false_alt(self):
        s = Sorter(
                input_locations=['tests/files/sort_false_alt_in'],
                output_location='tests/files/sort_false_alt_out',
                formats_preference='tap,dsk,z80,sna,tzx,trd'.split(','),
                include_alternate_formats=False,
                include_alternate=True,
                include_rereleases=True,
                output_folder_structure='',
                cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_false_alt_out/Dizzy Elusive (19xx)(Jura)(RU)(en)[aka Dizzy Neulovimyj].trd'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/files/sort_false_alt_out/Dizzy Elusive (19xx)(Jura)(RU)(en)[a].trd'
        self.assertFalse(os.path.exists(not_expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_multilang_games(self):
        s = Sorter(input_locations=['tests/files/sort_multilang_in'],
                   output_location='tests/files/sort_multilang_out',
                   formats_preference='tap,dsk,z80,sna,tzx,trd'.split(','),
                   include_alternate_formats=False,
                   include_alternate=False,
                   include_rereleases=False,
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        #Bug-eyes has both English and Italian versions, should retain both
        expected_file = 'tests/files/sort_multilang_out/Bug-Eyes (1985)(Icon)(GB)(it)[aka Bor-Fies].tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_multilang_out/Bug-Eyes (1985)(Icon).z80'
        self.assertTrue(os.path.exists(expected_file))
        #Drazen Petrovic Basket has only spanish version.
        expected_file = 'tests/files/sort_multilang_out/Drazen Petrovic Basket (1989)(Topo Soft)(48K-128K)(es).tap'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = 'tests/files/sort_multilang_out/Drazen Petrovic Basket (1989)(Topo Soft)(48K-128K).tap'
        self.assertFalse(os.path.exists(not_expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_multipart_games(self):
        s = Sorter(
                input_locations=['C:/ZX Pokemaster/tests/files/sort_multipart_in'],
                output_location='C:/ZX Pokemaster/tests/files/sort_multipart_out',
                formats_preference=['tap', 'z80'],
                include_alternate_formats=False,
                include_alternate=False,
                include_rereleases=False,
                output_folder_structure='',
                cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_multipart_out/Arkos (1988)(Zigurat)(es)(Tape 1 of 3).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_multipart_out/Arkos (1988)(Zigurat)(es)(Part 2 of 3).z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_multipart_out/Arkos (1988)(Zigurat)(es)(Part 3 of 3).z80'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_extremely_long(self):
        s = Sorter(
                   input_locations=['tests/files/sort_extremely_long_in'],
                   output_location='tests/files/sort_extremely_long_out',
                   output_folder_structure='unnecessarily_long_subfolder_name\\{Publisher}\\{GameName}',
                   include_alternate=True,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertEqual(len(s.errors), 0)
        expected_file = s.output_location+'/unnecessarily_long_subfolder_name/Mojon Twins, The/Maritrini, Freelance Monster Slayer en - Las/Maritrini, Freelance Monster Slayer en - Las (2012)(Mojon Twins, The)(ES)(en).tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = s.output_location+'/unnecessarily_long_subfolder_name/Mojon Twins, The/Maritrini, Freelance Monster Slayer en - Las/POKES/Maritrini, Freelance Monster Slayer en - Las (2012)(Mojon Twins, The)(ES)(en).pok'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = s.output_location+'/unnecessarily_long_subfolder_name/Mojon Twins, The/Maritrini, Freelance Monster Slayer en - Las/Maritrini, Freelance Monster Slayer en - Las (2012)(Mojon Twins, The)(ES).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = s.output_location+'/unnecessarily_long_subfolder_name/Mojon Twins, The/Maritrini, Freelance Monster Slayer en - Las/POKES/Maritrini, Freelance Monster Slayer en - Las (2012)(Mojon Twins, The)(ES).pok'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_saboteur_2(self):
        s = Sorter(
                    input_locations=['tests/files/sort_saboteur_in'],
                    output_location='tests/files/sort_saboteur_out',
                    output_folder_structure='',
                    formats_preference=['tap', 'tzx', 'z80'],
                    include_alternate_formats=False,
                    include_alternate=False,
                    include_rereleases=False,
                    include_hacks=False,
                    cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_saboteur_out/Saboteur II - Avenging Angel (1987)(Durell)(128K).tap'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_two_disks_two_sides(self):
        s = Sorter(
                   input_locations=['tests/files/sort_two_disks_two_sides_in'],
                   output_location='tests/files/sort_two_disks_two_sides_out',
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_two_disks_two_sides_out/Epyx 21 (1990)(U.S. Gold)(+3)(Disk 2 of 2).dsk'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_two_disks_two_sides_out/Epyx 21 (1990)(U.S. Gold)(+3)(Disk 1 of 2 Side A).dsk'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = 'tests/files/sort_two_disks_two_sides_out/Epyx 21 (1990)(U.S. Gold)(+3)(Disk 1 of 2 Side B).dsk'
        self.assertTrue(os.path.exists(expected_file))

    def test_equal_input_and_output_paths(self):
        initial_location = 'tests/files/sort_equal_in'
        target_location = 'tests/files/sort_equal_in_out'
        if os.path.exists(target_location):
            shutil.rmtree(target_location)
        os.makedirs(target_location)
        os.makedirs(os.path.join(target_location, 'POKES'))
        for root, dir, files in os.walk(initial_location):
            for file in files:
                src = os.path.join(initial_location, file)
                dest = os.path.join(target_location, file)
                shutil.copy(src, dest)
        s = Sorter(
                   input_locations=[target_location],
                   output_location=target_location,
                   output_folder_structure='',
                   cache=False)
        s.sortFiles()
        self.assertEqual(len(s.errors), 0)

    def test_too_long_path(self):
        s = Sorter(
                   input_locations=['tests/files/sort_too_long_files_in'],
                   output_location='tests/files/sort_too_long_files_out',
                   output_folder_structure='{Publisher}/{GameName}',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertEqual(len(s.errors), 0)

    def test_dot_in_filename(self):
        s = Sorter(
                   input_locations=['tests/files/sort_dots_in'],
                   output_location='tests/files/sort_dots_out',
                   output_folder_structure='{Publisher}/{GameName}',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = s.output_location+'/Groot, Henk de/Spectrum Automatic Copier/Spectrum Automatic Copier (' \
                                          '1985)(Groot, Henk de)[aka Autocopy].z80'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = s.output_location+'/Creative Radical Alternative\Super Advanced Lawnmower Simulator Adventure 2 - The Sequel/Super Advanced Lawnmower Simulator Adventure 2 - The Sequel (1993)(Creative Radical Alternative).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = s.output_location+'/Proxima/Fuxoft Uvadi/Fuxoft Uvadi... (1992)(Proxima)(CZ).tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = s.output_location+'/Zenobi\Why is the World Round Anyway\Why is the World Round Anyway ... (demo) (1995)(Zenobi)(Side B).tzx'
        self.assertTrue(os.path.exists(expected_file))

    def test_weird_publisher(self):
        s = Sorter(
                   input_locations=['tests/files/sort_weird_publisher_in'],
                   output_location='tests/files/sort_weird_publisher_out',
                   output_folder_structure='{Publisher}',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_weird_publisher_out/A.A. Barulin/A.A. Barulin Utilities Collection (1992)(A.A. Barulin)(ru).trd'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_die_hard(self):
        s = Sorter(
                   input_locations=['tests/files/sort_die_hard_in'],
                   output_location='tests/files/sort_die_hard_out',
                   output_folder_structure='{Format}',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = 'tests/files/sort_die_hard_out/sna/Die Hard II (1999)(REMADE Corporation)(RU)(en).sna'
        self.assertTrue(os.path.exists(expected_file))

    def test_xrated(self):
        input_location = 'tests/files/sort_xrated_in'
        output_location = 'tests/files/sort_xrated_out'
        s = Sorter(
                   input_locations=[input_location],
                   output_location=output_location,
                   output_folder_structure='',
                   include_xrated=False,
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = output_location+'/Die Hard II (1999)(REMADE Corporation)(RU)(en).sna'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = output_location+'/Quest for Sex (19xx)(Carley Bros)[adult].z80'
        self.assertFalse(os.path.exists(not_expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_preferred_languages(self):
        input_location = 'tests/files/sort_preferred_language_in'
        output_location = 'tests/files/sort_preferred_language_out'
        s = Sorter(
                   input_locations=[input_location],
                   output_location=output_location,
                   languages=['es', 'ru'],
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = output_location+'/Tasword Two (1984)(MCI Iberica)(es)[re-release].tzx'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = output_location+'/Tasword Two - The Word Processor (1983)(Tasman)[tr ru][aka Tasword 2].tap'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = output_location+'/Tasword Two (1983)(Profisoft).tzx'
        self.assertFalse(os.path.exists(not_expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_not_traversing_subfolders(self):
        input_location = 'tests/files/sort_not_traversing_subfolders_in'
        output_location = 'tests/files/sort_not_traversing_subfolders_out'
        s = Sorter(
                   input_locations=[input_location],
                   output_location=output_location,
                   traverse_subfolders=False,
                   output_folder_structure='',
                   cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = output_location+'/Zaxxon (1985)(U.S. Gold).tap'
        self.assertTrue(os.path.exists(expected_file))
        not_expected_file = output_location+'/Abadia del Crimen, La (1988)(Opera Soft)(128K)(es).tap'
        self.assertFalse(os.path.exists(not_expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_8letter_paths(self):
        input_location = 'tests/files/sort_8letter_in'
        output_location = 'tests/files/sort_8letter_out'
        s = Sorter(
                   input_locations=[input_location],
                   output_location=output_location,
                   traverse_subfolders=True,
                   include_alternate=False,
                   short_filenames=True,
                   output_folder_structure='{Genre}\{MachineType}',
                   cache=False)
        if os.path.exists(s.output_location):
            # shutil.rmtree(s.output_location)
            os.system('rmtree "{}"'.format(s.output_location))
        s.sortFiles()
        expected_file = output_location + '/ARCGAMAD/128K/ABADELCR.TZX'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = output_location + '/ARCGAMAC/48K/DIEHARD2.SNA'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = output_location + '/ARCGAMAD/128K/ABADEL_2.TZX'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)
        for root, dirs, files in os.walk(
                os.path.join(output_location, 'SPOGAMAC', '48K')):
            self.assertEqual(len(files), 5)
        for root, dirs, files in os.walk(
                os.path.join(output_location, 'ELECTMAG', '48K')):
            self.assertEqual(len(files), 10)

    def test_files_per_folder(self):
        input_location = 'ftp/pub/sinclair/games/a'
        output_location = 'tests/files/sort_files_per_folder_out'
        s = Sorter(
            input_locations=[input_location],
            output_location=output_location,
            traverse_subfolders=False,
            include_alternate=False,
            output_folder_structure='',
            max_files_per_folder = 50,
            cache=True)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location, ignore_errors=True)
        s.sortFiles()
        self.assertEqual(len(s.errors), 0)
        for root, dirs, files in os.walk(output_location):
            print(root)
            self.assertGreater(len(dirs)+len(files), 0)
            self.assertLessEqual(len(files), s.max_files_per_folder)

    def test_folders_per_folder(self):
        input_location = 'tests/files/sort_folders_per_folder_in'
        output_location = 'tests/files/sort_folders_per_folder_out'
        s = Sorter(
            input_locations=[input_location],
            output_location=output_location,
            traverse_subfolders=True,
            include_alternate=True,
            output_folder_structure='{MachineType}/{Type}/{Genre}/{Format}',
            max_files_per_folder = 25,
            cache=True)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertEqual(len(s.errors), 0)
        unwanted_location = os.path.join(output_location, 'uti-uti')
        self.assertFalse(os.path.exists(unwanted_location))
        for root, dirs, files in os.walk(output_location):
            self.assertGreater(len(dirs)+len(files), 0)
            self.assertLessEqual(len(files), s.max_files_per_folder+1)
            if len(dirs)>s.max_files_per_folder+1:
                print(root)
            #+1 accounts for possible POKES subfolder
            self.assertLessEqual(len(dirs), s.max_files_per_folder+1)

    def test_files_by_language_per_folder(self):
        input_location = 'tests/files/sort_files_by_language_per_folder_in'
        output_location = 'tests/files/sort_files_by_language_per_folder_out'
        s = Sorter(
            input_locations=[input_location],
            output_location=output_location,
            traverse_subfolders=True,
            include_alternate=True,
            output_folder_structure='{Language}',
            max_files_per_folder = 10,
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertEqual(len(s.errors), 0)
        for root, dirs, files in os.walk(output_location):
            for dir in dirs:
                print(dir)
                self.assertTrue(len(dir) in [2, 5])
            break
        for root, dirs, files in os.walk(output_location+'\\en'):
            for dir in dirs:
                if len(dirs) > s.max_files_per_folder:
                    print(root)
                self.assertLessEqual(len(files), s.max_files_per_folder)
            break

    def test_complex_hierarchy_per_folder(self):
        input_location = 'tests/files/sort_complex_hierarchy_in'
        output_location = 'tests/files/sort_complex_hierarchy_out'
        s = Sorter(
            input_locations=[input_location],
            output_location=output_location,
            traverse_subfolders=True,
            include_alternate=True,
            output_folder_structure='{Language}\\{Format}\\{GameName}',
            max_files_per_folder = 10,
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertEqual(len(s.errors), 0)
        for root, dirs, files in os.walk(output_location+'\\Games'):
            for dir in dirs:
                print(dir)
                self.assertEqual(len(dir), 2)
            break
        for root, dirs, files in os.walk(output_location+'\\Games\\en\\dsk'):
            for dir in dirs:
                if len(dirs) > s.max_files_per_folder:
                    print(root)
                self.assertLessEqual(len(files), s.max_files_per_folder)
            break


    def test_content_desc(self):
        input_locations = [
            'tests/files/sort_contents_desc_in',
            # 'tosec/Sinclair ZX Spectrum/Compilations/Games/[TZX]'
        ]
        output_location = 'tests/files/sort_contents_desc_out'
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            traverse_subfolders=False,
            output_folder_structure='',
            # max_files_per_folder = 20,
            cache=True)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        expected_file = output_location+\
                        '/4 Game Pack No. 2 - Gunfighter + Periscope Up (1992)(Atlantis)(Side B).tzx'
        self.assertTrue(os.path.exists(expected_file))
        # expected_file = output_location+\
        #                 '/4 Most Megaheroes - Rogue Trooper + Capitan Sevilla (1991)(Alternative).tzx'
        # self.assertTrue(os.path.exists(expected_file))
        expected_file = output_location+\
                        '/16-48 Magazine Tape 02 (1983)(16-48 Tape Magazine)(16K)(Side A).tzx'
        self.assertTrue(os.path.exists(expected_file))

    def test_custom_file_naming_scheme(self):
        input_locations = [
            'tests/files/sort_saboteur_in',
            'tests/files/sort_extremely_long_in']
        output_location = 'tests/files/sort_custom_names_out'
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            include_alternate=False,
            output_filename_structure='{ZXDB_ID} - {GameName}',
            output_folder_structure='',
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        not_expected_file = output_location+'/Saboteur II (1987)(Durell).tap'
        self.assertFalse(os.path.exists(not_expected_file))
        expected_file = output_location+'/0004295 - Saboteur II - Avenging Angel.tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = output_location+'/0004295 - Saboteur II - Avenging Angel_2.tap'
        self.assertTrue(os.path.exists(expected_file))
        #Apparently, when this test was designed, we didn't know that this file is not an alternate, but a version with a different language (although ZXDB might be wrong in this case, we'll see
        # not_expected_file = output_location + '/0027953 - Maritrini, Freelance Monster Slayer en - Las Increibles Vicisitudes de Despertarse Resacosa con Fred_2.tap'
        # self.assertFalse(os.path.exists(not_expected_file))
        expected_md5 = '3610ee643dcefc3eb4ae12f2664ef004'
        expected_md5_found = False
        for root, dirs, files in os.walk(output_location):
            for file in files:
                gf = GameFile(os.path.join(root, file))
                if gf.getMD5()==expected_md5:
                    expected_md5_found = True
                    break
        if not expected_md5_found:
            self.fail()
        self.assertEqual(len(s.errors), 0)

    def test_camel_case(self):
        input_locations = [
            'tests/files/sort_saboteur_in',
            'tests/files/sort_extremely_long_in']
        output_location = os.path.abspath('tests/files/sort_camel_case_out/unnecessarily_long_path/unnecessarily_long_path/unnecessarily_long_path')
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            include_alternate=True,
            use_camel_case=True,
            output_folder_structure='{Publisher}',
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        not_expected_file = output_location+'/Durell/Saboteur II (1987)(Durell)(128K).tap'
        self.assertFalse(os.path.exists(not_expected_file))
        expected_file = output_location+'/Durell/SaboteurII-AvengingAngel(1987)(Durell)(128K).tap'
        self.assertTrue(os.path.exists(expected_file))
        expected_file = output_location + '/MojonTwinsThe/MaritriniFreelanceMonsterSlayerEn-LasIncreiblesVicisitudesDeDespertarse(2012)(MojonTwinsThe)(ES).tzx'
        self.assertTrue(os.path.exists(expected_file))
        self.assertEqual(len(s.errors), 0)

    def test_bad_zips(self):
        input_locations = [
            'tests/files/sort_bad_zips_in',
        ]
        output_location = 'tests/files/sort_bad_zips_out/'
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            include_alternate=True,
            use_camel_case=True,
            output_folder_structure='{Publisher}',
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertGreater(len(s.errors), 0)

    def test_3d_games(self):
        input_locations = [
            'tests/files/sort_3d_games_in',
        ]
        output_location = 'tests/files/sort_3d_games_out/'
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            include_alternate=True,
            output_folder_structure='',
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertEqual(len(s.errors), 0)
        for root, dirs, files in os.walk(output_location):
            for file in files:
                self.assertTrue(file.startswith('3D'))

    def test_same_name(self):
        input_locations = [
            'tests/files/sort_same_name_in',
        ]
        output_location = 'tests/files/sort_same_name_out/'
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            include_alternate=False,
            output_folder_structure='{GameName}',
            output_filename_structure='{GameName} {Publisher}',
            short_filenames=True,
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileExists(output_location+'/DEFENDER/DEFEND_5.TAP')

    def test_sort_by_type(self):
        input_locations = [
            'tosec/lost-and-found',
        ]
        output_location = 'tests/files/sort_by_type_out/'
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            include_alternate=False,
            output_folder_structure='{Type}\{Genre}',
            cache=True)
        if s.errors:
            print(s.errors)
            self.fail()
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileNotExists(s.output_location+'/Compilations/Applications/Compilation - Utilities')
        self.assertFileNotExists(s.output_location+'/Games/Scene Demo')
        self.assertFileNotExists(s.output_location+'/Games/Unknown')
        self.assertFileNotExists(s.output_location+'/Games/Programming - General')

    def test_original_name(self):
        input_locations = [
            'tests/files/sort_original_name_in',
        ]
        output_location = 'tests/files/sort_original_name_out/'
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            output_folder_structure='',
            output_filename_structure='{OriginalName} ({MachineType})',
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileExists(output_location+'/Dizzy VII - Crystal Kindom Dizzy (2017) (128K).tap')
        self.assertFileExists(output_location+'/CQuest (48K).tap')

    def test_supplementary_files(self):
        input_locations = [
            'tests/files/sort_supplementary_files_in',
        ]
        output_location = 'tests/files/sort_supplementary_files_out/'
        s = Sorter(
            input_locations=input_locations,
            output_location=output_location,
            include_supplementary_files=True,
            output_folder_structure='',
            cache=False)
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertEqual(s.errors, '')
        self.assertFileExists(output_location+'/SCRSHOT/A.I. Tic Tac Toe v1.0 (2005)(Zaniboni, Marcello)(IT)(en).gif')
        self.assertFileExists(output_location+'/Accelerator (1984)(Century City).gif')
        self.assertFileNotExists(output_location+'/Accelerator (1984)(Century City).zip')
        self.assertFileExists(output_location+"/UDG's Machine (1985)(Sagesoft)[aka UDG Machine].txt")

    def test_disappearing_files(self):
        s = Sorter(cache=True)
        s.input_locations = [
            'tests/files/sort_disappearing_files_in/',
        ]
        s.output_location = 'tests/files/sort_disappearing_files_out/'
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.output_folder_structure = ''
        s.include_supplementary_files = False
        s.include_alternate = True
        s.include_alternate_formats = True
        s.include_bad_dumps = True
        s.sortFiles()
        expected_crc = [
                        "adecd734", "2d91dd36", "7f16d967",
                        'b935fe51','37e6d2d1', '8406b797',
                                               "a7a9020b",
                                               "5e9b2c2d",
                                               "36465df4",
                                               "eea73628",
                                               "bc23eb73",
                        ]
        self.assertFilesWithCRCsExist(expected_crc, s.output_location)

    def test_max_archive_size(self):
        s= Sorter(cache=False)
        s.input_locations = [
            'tests/files/sort_max_archive_in/',
        ]
        s.output_location = 'tests/files/sort_max_archive_out/'
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.max_archive_size = 1*1024*1024
        s.sortFiles()
        self.assertFileNotExists('tests/files/sort_max_archive_out/Accelerator (1984)(Century City).z80')
        s.max_archive_size = 5*1024*1024
        s.sortFiles()
        self.assertFileExists('tests/files/sort_max_archive_out/Accelerator (1984)(Century City).z80')

    def test_other_archives(self):
        s = Sorter(cache=False)
        s.input_locations = [
            'tests/files/sort_other_archives_in/',
        ]
        s.output_location = 'tests/files/sort_other_archives_out/'
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileExists('tests/files/sort_other_archives_out/Zaxxon (1985)(U.S. Gold).tap')
        self.assertFileExists('tests/files/sort_other_archives_out/Crystal Kingdom Dizzy 2017 v1.0.4 (2017-04-15)('
                              'Barskiy, Evgeniy)(128K)(RU)(en).tap')
        self.assertFileExists('tests/files/sort_other_archives_out/Arkos (1988)(Zigurat)(ES)(Part 1 of 3).z80')
        self.assertFileExists('tests/files/sort_other_archives_out/Unknown files/LASTHERO.TRD')
        self.assertFileExists('tests/files/sort_other_archives_out/Unknown files/SPCOM9 - alt.TAP')
        gamefile = GameFile('tests/files/sort_other_archives_out/Unknown files/LASTHERO.TRD')
        self.assertEqual(gamefile.getCRC32(), '52725975')

    def test_crc_collision_zip(self):
        s = Sorter(cache=False)
        s.input_locations = [
            'tests/files/sort_crc_collision_zip_in/',
        ]
        s.output_location = 'tests/files/sort_crc_collision_out/'
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileExists('tests/files/sort_crc_collision_out/Vozrazhdenie 00 (1996-01-01)(Vozrazhdenie)(RU)[Omsk].udi')
        self.assertFileExists('tests/files/sort_crc_collision_out/Vozrazhdenie 01 (1996-01-31)(Vozrazhdenie)(RU)[Omsk].udi')

    def test_crc_collision_each_own_zip(self):
        s = Sorter(cache=False)
        s.input_locations = [
            'tests/files/sort_crc_collision_each_own_zip_in/',
        ]
        s.output_location = 'tests/files/sort_crc_collision_out/'
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileExists('tests/files/sort_crc_collision_out/Vozrazhdenie 00 (1996-01-01)(Vozrazhdenie)(RU)[Omsk].udi')
        self.assertFileExists('tests/files/sort_crc_collision_out/Vozrazhdenie 01 (1996-01-31)(Vozrazhdenie)(RU)[Omsk].udi')

    def test_cyrillic(self):
        s = Sorter(cache=False)
        s.input_locations = [
            'tests/files/sort_cyrillic_in/',
        ]
        s.output_location = 'tests/files/sort_cyrillic_out/'
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileExists('tests/files/sort_cyrillic_out/Vozrazhdenie 00 (1996-01-01)(Vozrazhdenie)(RU)[Omsk].udi')

    def test_deleting(self):
        s = Sorter(cache=False,
                   delete_source_files=True,
                   include_alternate=True,
                   )
        s.input_locations = [
            'tests/files/sort_deleting_in/',
        ]
        s.output_location = 'tests/files/sort_deleting_out/'
        backup_location = 'tests/files/sort_deleting_in_backup'
        if os.path.exists(s.input_locations[0]):
            shutil.rmtree(s.input_locations[0], ignore_errors=True)
        shutil.copytree(backup_location, s.input_locations[0])
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()
        self.assertFileNotExists(os.path.join(s.input_locations[0], '2 ExtendedBASIC.tzx.zip'))
        self.assertFileNotExists(os.path.join(s.input_locations[0], 'Dizzy VII - Crystal Kindom Dizzy (2017).7z'))
        self.assertFileNotExists(os.path.join(s.input_locations[0], '0004295 - Saboteur II.z80'))
        self.assertFileNotExists(os.path.join(s.input_locations[0], 'arkos.zip'))
        self.assertFileNotExists(os.path.join(s.input_locations[0], '3D Lunattack (1984)(Hewson Consultants)(48K)(GB)(en)en_4.pok'))
        self.assertFileNotExists(os.path.join(s.input_locations[0], 'POKES/3D Lunattack (1984)(Hewson Consultants)(48K)(GB)(en)en_4.pok'))
        self.assertFileNotExists(os.path.join(s.input_locations[0], 'POKES'))
        self.assertFileExists(os.path.join(s.input_locations[0], 'non speccy related stuff'))
        self.assertFileNotExists(os.path.join(s.input_locations[0], 'subdir'))

    def test_one_pok_file_per_game_per_folder(self):
        s = Sorter(cache=False,
                   include_alternate=True,
                   output_folder_structure='{GameName}/{Format}',
                   place_pok_files_in_pokes_subfolders=False,
                   )
        s.input_locations = [
            'tests/files/sort_one_pok_file_per_folder_in/',
        ]
        s.output_location = 'tests/files/sort_one_pok_file_per_folder_out/'
        if os.path.exists(s.output_location):
            shutil.rmtree(s.output_location)
        s.sortFiles()


    # def test_sort_alternate_files(self):
    #     '''
    #     The [a] parameter is assigned randomly in ZX Pokemaster sorting. It is really only important for TOSEC.
    #     '''
    #     s = Sorter(cache=False,
    #                include_alternate=True)
    #     s.input_locations = [
    #         'tests/files/sort_alternate_files_in/',
    #         ]
    #     s.output_location = 'tests/files/sort_alternate_files_out/'
    #     s.sortFiles()
    #     self.assertFileExists('tests/files/sort_alternate_files_out/Licence to Kill (1989)(Domark)(48K-128K).tap')
    #     self.assertFileExists('tests/files/sort_alternate_files_out/Licence to Kill (1989)(Domark)(48K-128K)[a].tap')
    #     for root, dirs, files in os.walk(s.output_location):
    #         for file in files:
    #             if file.endswith('.pok'):
    #                 continue
    #             gf = GameFile(os.path.join(root, file))
    #             if '[a]' in file:
    #                 expected_crc = 'bfe04de9'
    #             else:
    #                 expected_crc = '8b0de117'
    #             self.assertEqual(gf.getCRC32(), expected_crc)

    # def test_sorting_withing_same_folder(self):
    #     s = Sorter(cache=False,
    #                delete_source_files=True,
    #                include_alternate=True,
    #                )
    #     s.input_locations = [
    #         'tests/files/sort_deleting_in/',
    #     ]
    #     s.output_location = 'tests/files/sort_deleting_in/'
    #     backup_location = 'tests/files/sort_deleting_in_backup'
    #     if os.path.exists(s.input_locations[0]):
    #         shutil.rmtree(s.input_locations[0], ignore_errors=True)
    #     shutil.copytree(backup_location, s.input_locations[0])
    #     s.sortFiles()
    #     self.assertFileNotExists(s.input_locations[0]+'_old')
    #     self.assertFileNotExists(s.input_locations[0])

    def assertFilesWithCRCsExist(self, expected_crc, output_location):
        expected_crc_count = len(expected_crc)
        expected_crc_found = 0
        for root, dirs, files in os.walk(output_location):
            for file in files:
                gf = GameFile(os.path.join(root, file))
                if gf.getCRC32() in expected_crc:
                    # print(gf.getCRC32())
                    expected_crc_found += 1
                    expected_crc.pop(expected_crc.index(gf.getCRC32()))
        if expected_crc:
            print(expected_crc)
        self.assertEqual(expected_crc_found, expected_crc_count)

    def assertFileExists(self, file_path):
        self.assertTrue(os.path.exists(file_path))

    def assertFileNotExists(self, file_path):
        self.assertFalse(os.path.exists(file_path))

if __name__=='__main__':
    os.rename('pokemaster.db', '_pokemaster.db')
    unittest.main()
    if os.path.exists('_pokemaster.db'):
        os.rename('_pokemaster.db', 'pokemaster.db')
    # t = TestSorter()
    # t.test_alt_files()
    # t.test_same_name()
    # t.test_sort_false_alt()
    # t.test_8letter_paths()
    # t.test_all_subfolder_kwargs()
    # t.test_alt_files()
    # t.test_camel_case()
    # t.test_not_traversing_subfolders()
    # t.test_files_per_folder()
    # t.test_folders_per_folder()
    # t.test_multilang_games()
    # t.test_multipart_games()