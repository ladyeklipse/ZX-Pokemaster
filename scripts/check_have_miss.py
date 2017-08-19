from classes.tosec_scraper import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
ts = TOSECScraper(cache=False)
ts.paths = ts.generateTOSECPathsArrayFromDatFiles()
missed_paths = ts.getUnscraped()

