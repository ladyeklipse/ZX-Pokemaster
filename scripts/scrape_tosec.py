from scripts.restore_db import *
from classes.tosec_scraper import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
if __name__=='__main__':
    restoreDB()
print(os.getcwd())
ts = TOSECScraper(cache=False)
ts.paths = ts.generateTOSECPathsArrayFromDatFiles()
ts.paths = [x for x in ts.paths if '(CSSCGC)' not in x['path']]
ts.db.loadCache()
ts.scrapeTOSEC()
ts.updateTOSECAliasesCSV()
ts.addUnscraped()
ts.db.commit()
ts.db.loadCache(True)
print('will load real files')
ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\lost_and_found')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\mia')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\ZXAAA Compilations')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\ZXAAA Releases')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\itch.io')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\indieretronews.com')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\CSSCGC Games Reviewed')
ts.scrapeTOSEC()
ts.updateTOSECAliasesCSV()
ts.addUnscraped()
ts.db.commit()
import scripts.check_zxdb_tosec_inconsistencies