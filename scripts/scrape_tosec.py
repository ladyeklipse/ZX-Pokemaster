from scripts.restore_db import *
from classes.tosec_scraper import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
if __name__=='__main__':
    restoreDB()
print(os.getcwd())
ts = TOSECScraper(cache=False)
ts.paths = ts.generateTOSECPathsArrayFromDatFiles()
ts.db.loadCache()
ts.scrapeTOSEC()
ts.updateTOSECAliasesCSV()
ts.addUnscraped()
ts.db.commit()
ts.db.loadCache(True)
# for i in range(3):
#     print('checking have miss, iteration', i)
#     ts.paths = ts.checkHaveMissRatio()
#     if not ts.paths:
#         break
#     ts.scrapeTOSEC()
#     ts.updateTOSECAliasesCSV()
#     ts.addUnscraped()
#     ts.db.commit()
ts.db.loadCache(True)
print('will load real files')
ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\lost_and_found')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\mia')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\fikus-pikus\\renamed')
ts.scrapeTOSEC()
ts.updateTOSECAliasesCSV()
ts.addUnscraped()
ts.db.commit()
import scripts.check_zxdb_tosec_inconsistencies