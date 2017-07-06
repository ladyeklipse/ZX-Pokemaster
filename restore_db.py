import sqlite3
import traceback
import os
if os.path.exists('pokemaster.db'):
    os.unlink('pokemaster.db')
conn = sqlite3.connect('pokemaster.db')
cur = conn.cursor()
cur.execute('PRAGMA JOURNAL_MODE = OFF')
with open('pokemaster.db.sql', 'r', encoding='utf-8') as f:
    sql = f.read().split(';\n')
    print(len(sql))
    for query in sql:
        print(query)
        if not query or 'COMMIT' in query:
            continue
        try:
            cur.execute(query)
            # conn.commit()
        except Exception as e:
            print(traceback.format_exc())
    # cur.close()
    conn.commit()