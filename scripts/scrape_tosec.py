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
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\')
ts.sortPaths()
ts.scrapeTOSEC()
ts.addUnscraped()
ts.updateContentDescAndNotesLookupTable() #doesn't work well
ts.db.commit()
import scripts.check_zxdb_tosec_inconsistencies
import scripts.create_tosec_dats
import scripts.minify_database