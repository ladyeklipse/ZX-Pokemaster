import os
os.chdir('..')
from classes.database import *
db = Database()
collisions_table = db.execute('SELECT * FROM files_with_same_md5')
md5_dict = {}
for row in collisions_table:
    key = row['md5']+';'+row['wos_path']
    row = list(row)
    row.insert(7, '')
    md5_dict[key] = list(row)
# print(md5_dict)
old_md5_dict = {}
with open('same_md5.csv', 'r', encoding='utf-8') as f:
    for line in f.readlines():
        line = line.split(';')
        if len(line)<10:
            continue
        md5 = line[3].strip()
        wos_path = line[8].strip()
        key =md5+';'+wos_path
        if key in md5_dict.keys():
            new_row = md5_dict[key]
            decision = line[6].strip()
            if decision:
                print(decision)
                md5_dict[key][7] = decision
        # old_md5_dict[md5] = decision
with open('same_md5_new.csv', 'w', encoding='utf-8') as f_new:
    for row in md5_dict.values():
        # print(row)
        f_new.write(';'.join([str(x) for x in row])+'\n')
new_exc_list = []
with open('exclusion_list.csv', 'r', encoding='utf-8') as f:
    with open('exclusion_list_new.csv', 'w', encoding='utf-8') as f_new:
        for line in f.readlines():
            line = line.strip()
            for row in md5_dict.values():
                if line == row[8] or line == row[9]:
                    if line not in new_exc_list:
                        new_exc_list.append(line)
                        f_new.write(line+'\n')
