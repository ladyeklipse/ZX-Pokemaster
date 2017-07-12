import sys

if __name__ == '__main__':
    sys.argv.append('build')

from cx_Freeze import setup, Executable

base = None
if sys.platform == "win32":
    base = "Win32GUI"

setup(
    name="ZX Pokemaster",
    version="1.0",
    description="File management utility for ZX Spectrum files.",
    options={"build_exe": {"includes": ["sip", "PyQt4.QtCore", "PyQt4.QtGui"],
                           'include_msvcr':True,
                           "optimize":2,
                           "include_files": ['pokemaster.db']}},
    executables=[Executable("pokemaster.py", base=base)])



