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

