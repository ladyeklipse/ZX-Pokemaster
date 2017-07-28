import sqlite3
import traceback
import os
import sys
import shutil
if os.path.exists('pokemaster.db'):
    os.unlink('pokemaster.db')
shutil.copy('pokemaster_zxdb_only.db', 'pokemaster.db')
# conn = sqlite3.connect('pokemaster.db')
# cur = conn.cursor()
# cur.execute('PRAGMA JOURNAL_MODE = OFF')
# with open('pokemaster_zxdb_only.db.sql', 'r', encoding='utf-8') as f:
#     sql = f.read().split(';\n')
#     print(len(sql))
#     for query in sql:
#         print(query)
#         if not query or 'COMMIT' in query:
#             continue
#         try:
#             cur.execute(query)
#             conn.commit()
#             input()
        # except Exception as e:
        #     print(traceback.format_exc())
        #     sys.exit()
    # cur.close()
    # conn.commit()