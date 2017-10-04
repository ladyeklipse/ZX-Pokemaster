from scripts.restore_db import *
from classes.tosec_scraper import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
if __name__=='__main__':
    restoreDB()
ts = TOSECScraper(cache=False)
ts.db.loadCache()
ts.paths = ts.generateTOSECPathsArrayFromDatFiles()
for path in ts.paths:
    if 'SCGC' in path['path']:
        path['path'] = path['path'].replace('(CSSCGC)', '(-)[CSSCGC]').replace('(CCSCGC)', '(-)[CSSCGC]')
        print(path['path'], path['md5'])
# ts.sortPaths()
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\test')
# ts.paths = [path for path in ts.paths if 'Shadow of the Unicorn' in path['path']]
ts.sortPaths()
ts.scrapeTOSEC()
ts.addUnscraped()
# ts.updateContentDescAndNotesLookupTable() #doesn't work well
ts.db.commit()
import scripts.check_zxdb_tosec_inconsistencies
import scripts.create_tosec_dats