from classes.zxdb_scraper import *
from classes.scraper import *
if (os.getcwd().endswith('scripts')):
    os.chdir('..')
def scrapeGameFilesFromWosMirrors(games):
    s = Scraper()
    for game in games:
        for file in game.getFiles():
            local_path = file.getLocalPath()
            if os.path.exists(local_path) and \
                    os.path.getsize(local_path):
                continue
            elif os.path.exists(local_path) and \
                os.path.getsize(local_path)!=file.size:
                print('wrong file size:', local_path)
            else:
                for mirror in WOS_MIRRORS:
                    try:
                        status = s.downloadFile(file.getWosPath(wos_mirror_root=mirror), local_path)
                    except:
                        print(traceback.format_exc())
                    if status == 200:
                        break

        for release in game.releases:
            if release.ingame_screen_gif_filesize:
                path = release.getIngameScreenFilePath('gif')
                local_path = LOCAL_FTP_ROOT+path
                if not os.path.exists(local_path) or \
                                os.path.getsize(local_path)==0:# != release.ingame_screen_gif_filesize:
                    for mirror in WOS_MIRRORS:
                        status = s.downloadFile(mirror+path, local_path)
                        if status==200:
                            break

            if release.loading_screen_scr_filesize:
                path = release.getLoadingScreenFilePath('scr')
                local_path = LOCAL_FTP_ROOT+path
                if not os.path.exists(local_path) or \
                                os.path.getsize(local_path)==0:# != release.loading_screen_scr_filesize:
                    for mirror in WOS_MIRRORS:
                        status = s.downloadFile(mirror+path, local_path)
                        if status==200:
                            break

            if release.loading_screen_gif_filesize:
                path = release.getLoadingScreenFilePath('gif')
                local_path = LOCAL_FTP_ROOT+path
                if not os.path.exists(local_path) or \
                                os.path.getsize(local_path)==0:# != release.loading_screen_gif_filesize:
                    for mirror in WOS_MIRRORS:
                        status = s.downloadFile(mirror+path, local_path)
                        if status==200:
                            break

            if release.manual_filesize:
                path = release.manual_filepath
                local_path = LOCAL_FTP_ROOT+path
                if not os.path.exists(local_path) or \
                        not os.path.getsize(local_path):
                        #os.path.getsize(local_path) != release.manual_filesize:
                    for mirror in WOS_MIRRORS:
                        status = s.downloadFile(mirror + path, local_path)
                        if status == 200:
                            break
                # else:
                #     print('File', local_path, 'OK')

if __name__=='__main__':
    zxdb = ZXDBScraper()
    start_time = time.clock()
    games = zxdb.getAllGames()
    end_time = time.clock()
    print('got in:', end_time - start_time)
    db = Database()
    for game in games:
        for release in game.releases:
            try:
                release.getInfoFromLocalFiles()
            except:
                print(traceback.format_exc())
        db.addGame(game)
    db.commit()
    print(len(games))
    print(len(set([game.wos_id for game in games])))
