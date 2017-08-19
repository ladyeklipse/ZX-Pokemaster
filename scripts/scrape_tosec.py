
from classes.tosec_scraper import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
if __name__=='__main__':
    import restore_db
print(os.getcwd())
ts = TOSECScraper(cache=False)
ts.paths = ts.generateTOSECPathsArrayFromDatFiles()
ts.db.loadCache()
ts.scrapeTOSEC()
ts.updateTOSECAliasesCSV()
ts.addUnscraped()
ts.db.commit()
ts.db.loadCache(True)
ts.paths = ts.generateTOSECPathsArrayFromFolder('tosec\\lost_and_found')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\mia')
ts.paths += ts.generateTOSECPathsArrayFromFolder('tosec\\fikus-pikus\\renamed')
ts.scrapeTOSEC()
ts.updateTOSECAliasesCSV()
ts.addUnscraped()
ts.db.commit()
for i in range(3):
    ts.paths = ts.checkHaveMissRatio()
    ts.scrapeTOSEC()
    ts.updateTOSECAliasesCSV()
    ts.addUnscraped()
    ts.db.commit()
import scripts.check_zxdb_tosec_inconsistencies