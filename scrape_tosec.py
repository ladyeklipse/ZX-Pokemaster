from classes.tosec_scraper import *
import sys
if __name__=='__main__':
    import restore_db
    ts = TOSECScraper(cache=False)
    ts.paths = ts.generateTOSECPathsArrayFromDatFiles()
    # ts.paths = ts.showUnscraped()
    ts.db.loadCache()
    ts.scrapeTOSEC()
    ts.addUnscraped()
    # ts.paths = ts.showUnscraped()
    # for path in ts.paths:
    #     game = ts.db.getGameByFileMD5(path['md5'])
    #     if game:
    #         file = game.findFileByMD5(path['md5'])
    #         file.getParamsFromTOSECPath(path['path'])
    #         ts.inconsistencies.append((path['path'], file.wos_path, game.getWosID(), file.getTOSECName()))
    #         ts.db.addGame(game)
    ts.db.commit()
    with open('tosec_inconsistencies.csv', 'w', encoding='utf-8') as f:
        for array in ts.wrong_releases:
            f.write(';'.join(array)+'\n')
        for array in ts.inconsistencies:
            f.write(';'.join(array)+'\n')

    sys.exit()
