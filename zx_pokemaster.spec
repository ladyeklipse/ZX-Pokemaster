# -*- mode: python -*-

block_cipher = None

a = Analysis(['pokemaster.py'],
             pathex=['C:\\ZX Pokemaster'],
             binaries=[],
             hiddenimports=[
                    'sip',
                    'PyQt5.QtCore',
                    'PyQt5.QtGui',
                    'PyQt5.QtWidgets',
                    'PIL',
                    'ui',
             ],
             datas=[
                ('ui/res_rc.py', 'ui'),
                ('default_settings/settings.json', 'default_settings'),
                ('minified_database/pokemaster.db', '.'),
                ('README.txt', '.'),
                ('assets/pokemaster.png', 'assets'),
                ('assets/pokemaster.ico', 'assets'),
            ],
             hookspath=None,
             runtime_hooks=[],
             excludes=[
             'PyQt4',
             'PyQt4.QtCore',
             'PyQt4.QtGui',
             'tk',
             'tkinter',
             'matplotlib',
             'gfortran',
             'libopenblas',
             ],
             win_no_prefer_redirects=False,
             win_private_assemblies=False,
             cipher=block_cipher)
pyz = PYZ(a.pure, a.zipped_data,
             cipher=block_cipher)
exe = EXE(pyz,
          a.scripts,
          exclude_binaries=True,
          name='ZX Pokemaster',
          debug=False,
          strip=False,
          icon='assets/pokemaster.ico',
          bootloader_ignore_signals=False,
          upx=True,
          console=False)
coll = COLLECT(exe,
               a.binaries,
               a.zipfiles,
               a.datas,
               strip=False,
               upx=True,
               name='ZX Pokemaster')