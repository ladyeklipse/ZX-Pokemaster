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

# ts.showSameMD5WarningsForFolder('tosec\\reviewed files\\spectrum4ever')

reviewed_files = ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\')
ts.paths += reviewed_files
ts.sortPaths()
# ts.paths = [path for path in ts.paths if path['name'].startswith('Robin of')]
ts.scrapeTOSEC()
ts.addUnscraped()
# ts.updateContentDescAndNotesLookupTable() #doesn't work well, need to back up the CSV
ts.db.commit()
# import scripts.check_zxdb_tosec_inconsistencies
