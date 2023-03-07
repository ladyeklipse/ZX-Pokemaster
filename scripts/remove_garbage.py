import glob

for file in glob.glob("../AllTipshopPokes/*/*.pok"):
    # print(file)
    with open(file, 'r') as f:
        contents = f.read()
        if 'Р В РІР‚в„ў ' in contents:
            contents = contents.replace(' Р В РІР‚в„ў ', ' ')
            print(contents)
    with open(file, 'w') as f:
        f.write(contents)