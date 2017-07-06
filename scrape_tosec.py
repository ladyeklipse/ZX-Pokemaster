from classes.tosec_scraper import *

if __name__=='__main__':
    ts = TOSECScraper()
    paths = ts.generateTOSECPathsArray()
    # for path in paths[:10]:
    #     print(path)
    paths = [
        "tosec\Games\[TZX]\Aknadach (1990)(Proxima Software)(cs)[a].zip",
        "tosec\Games\[DSK]\Abadia del Crimen, La (1988)(Opera Soft)(es).zip",
        "tosec\Games\[DSK]\Xybots (1989)(Domark).zip",
        "tosec\Games\[TAP]\Zenji (1984)(Activision).zip",
        #
        "tosec\Games\[TZX]\Gilbert - Escape from Drill (1989)(Alternative Software)[128K][re-release].zip",
        "tosec\Games\[TZX]\Gilbert - Escape from Drill (1989)(Alternative Software)[re-release].zip",
        "tosec\Compilations\Games\[TZX]\Fists 'n' Throttles - Buggy Boy + Thundercats (1989)(Elite Systems)[48-128K].zip",
        "tosec\Games\[TZX]\Fists 'n' Throttles - Dragon's Lair (1989)(Elite Systems)(Side A).zip",
        "tosec\Games\[TZX]\Fists 'n' Throttles - Dragon's Lair (1989)(Elite Systems)(Side B).zip",
        'tosec\Games\[TAP]\Q-Bertus (19xx)(-)(de).zip',
        "tosec\Games\[TZX]\Indoor Soccer (1986)(Magnificent 7 Software).zip", #Error in ZXDB!!!
        "tosec\Games\[TZX]\Falcon - The Renegade Lord (1987)(Virgin Games)[h].zip", #":" symbol!d
        "tosec\Games\[TAP]\\3D Starfighter (1988)(Codemasters).zip",
        "tosec\Games\[TZX]\\3D Starfighter (1988)(Codemasters).zip",
        "tosec\Games\[Z80]\\3D Starfighter (1988)(Codemasters).zip",
        "tosec\Games\[SCL]\\3D Starfighter (1988)(Codemasters)[h Flash][t].zip",
        "tosec\Games\[TZX]\Indoor Soccer (1986)(Alternative Software)[re-release].zip",
        "tosec\Games\[TAP]\Indoor Soccer (1986)(Magnificent 7 Software).zip",
        "tosec\Games\[Z80]\Indoor Soccer (1986)(Magnificent 7 Software).zip",
        "tosec\Games\[Z80]\9-Hole Golf (1986)(Galileo).zip",
        "tosec\Covertapes\[TZX]\Ajedrez (1985)(Load 'n' Run)(es)[aka Cyrus IS Chess].zip",
        'tosec\Games\[TAP]\Zzzz (1986)(Mastertronic).zip',
        'tosec\Games\[TZX]\Zzzz (1986)(Mastertronic).zip',
        'tosec\Games\[Z80]\Zzzz (1986)(Mastertronic).zip',
        'tosec\Games\[TZX]\Zzzz (1986)(Mastertronic)[a].zip',
        'tosec\Games\[Z80]\Zzzz (1986)(Mastertronic)[a].zip',
        'tosec\Games\[TZX]\Zzzz (1986)(Zenobi Software)[re-release].zip',
        'tosec\Games\[Z80]\Zzzz (1986)(Zenobi Software)[re-release].zip',
        'tosec\Games\[DSK]\Zzzz (1986)(Zenobi Software)[re-release].zip'
        ]
    # paths = ts.showUnscraped()
    # ts.paths = paths
    ts.scrapeTOSEC()
    # ts.showUnscraped()