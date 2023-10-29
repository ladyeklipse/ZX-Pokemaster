import os
os.chdir('..')
for root, dirs, files in os.walk('alltipshoppokes'):
    for file in files:
        if not file.endswith('.pok'):
            continue
        path = os.path.join(root, file)
        # print(path)
        with open(path, 'r') as f:
            contents = f.readlines()
            for line in contents:
                try:
                    line.encode('ascii')
                except UnicodeEncodeError as e:
                    print("file", path, "has errors:", e)
                    print("line=", line)