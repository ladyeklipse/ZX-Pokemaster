from classes.database import *
from mysql import connector
import time
zxdb_con = connector.connect(
                        user='root',
                        password='',
                        host='localhost',
                        database='zxdb',
                        charset='utf8',
                        )
zxdb_cur = zxdb_con.cursor(dictionary=True, buffered=True)
sql = 'SELECT ' \
      'entries.*, ' + \
      'publishers.*, ' \
      'labels.*, ' \
      'aliases.* ' \
      'FROM entries ' + \
      'LEFT JOIN publishers ON publishers.entry_id=entries.id AND publishers.release_seq=releases.' + \
      'LEFT JOIN labels ON labels.id=publishers.label_id ' + \
      'LEFT JOIN aliases ON aliases.entry_id=entries.id ' \
      'LEFT JOIN downloads ON downloads.entry_id=entries.id ' \
      'LEFT JOIN filetypes ON downloads.filetype_id=filetypes.id ' \
      'LEFT JOIN genretypes ON genretypes.id=entries.genretype_id ' \
      'WHERE downloads.filetype_id IN (0, 1, 2, 8, 10, 11, 17, 20, 21, 28) ' \
      'LIMIT 5000'
print(sql)
start_time = time.clock()
zxdb_cur.execute(sql)
raw_data = []
for row in zxdb_cur:
    raw_data.append(row)
end_time = time.clock()
print(sorted(raw_data[0].keys()))
print(raw_data[:10])
print(len(raw_data))
print('got in:', end_time-start_time)
