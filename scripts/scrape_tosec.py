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
ts.paths = [x for x in ts.paths if '(CSSCGC)' not in x['path'] and x['md5']!='e27911f6828ca9249ab9755a9ff10d17']
ts.sortPaths()
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\lost_and_found')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\mia')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\ZXAAA Compilations')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\ZXAAA Releases')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\itch.io')
ts.paths += ts.generateTOSECPathsArrayFromFolder('toяsec\\indieretronews.com Games')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\CSSCGC Games Reviewed')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\spectrum4ever.org\\reviewed')
ts.sortPaths()
ts.scrapeTOSEC()
ts.addUnscraped()
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