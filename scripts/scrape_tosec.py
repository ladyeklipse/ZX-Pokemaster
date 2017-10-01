from scripts.restore_db import *
from classes.tosec_scraper import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
if __name__=='__main__':
    restoreDB()
print(os.getcwd())
ts = TOSECScraper(cache=False)
ts.db.loadCache()
ts.paths = ts.generateTOSECPathsArrayFromDatFiles()
# ts.paths = [x for x in ts.paths if 'SCGC)' not in x['path'] and x['md5']!='e27911f6828ca9249ab9755a9ff10d17']
for path in ts.paths:
    if 'SCGC' in path['path']:
        path['path'] = path['path'].replace('(CSSCGC)', '(-)[CSSCGC]').replace('(CCSCGC)', '(-)[CSSCGC]')
        print(path['path'], path['md5'])
ts.sortPaths()
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\lost_and_found')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\mia')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\ZXAAA Compilations')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\ZXAAA Releases\\Games')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\itch.io')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\indieretronews.com Games')
# ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\CSSCGC Games Reviewed')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\spectrum4ever.org\\reviewed')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\reviewed files\\')
ts.sortPaths()
ts.scrapeTOSEC()
ts.addUnscraped()
ts.updateContentDescAndNotesLookupTable()
ts.db.commit()
# ts.db.loadCache(True)
# print('will load real files')
# ts.paths = []
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\lost_and_found')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\mia')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\ZXAAA Compilations')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\ZXAAA Releases')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\itch.io')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\indieretronews.com')
# ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\CSSCGC Games Reviewed')
# ts.scrapeTOSEC()
# ts.addUnscraped()
# ts.db.commit()
import scripts.check_zxdb_tosec_inconsistencies