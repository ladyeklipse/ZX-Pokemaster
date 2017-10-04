import os
os.chdir('C:\ZX Pokemaster\\tosec\ROMVault_V2.6.2\ROMRoot\\')
aka_files = []
for root, dirs, files in os.walk('.'):
    for file in files:
        if '[aka ' in file:
            aka_files.append(file)
aka_files = sorted(set(aka_files))
print(len(aka_files))
with open('C:\ZX Pokemaster\\tosec\\aka_files.csv', 'w+') as f:
    f.write('\n'.join(aka_files))