from classes.database import *
import shutil
import os
if (os.getcwd().endswith('functions')):
    os.chdir('..')

def move_known(src, dest=None):
    src = src.replace('//', '/')
    if not dest:
        dest = src+'known/'
    db = Database()
    # db.loadCache()
    for root, dirs, files in os.walk(src):
        for file_name in files:
            file_path = os.path.join(root, file_name).replace('\\', '/')
            file = GameFile(file_path)
            game = db.getGameByFileMD5(file.getMD5())
            # print(src+file_name, dest+file_name)
            if game:
                print(file, 'known as', game.findFileByMD5(file.md5).getTOSECName())
                dest_path = dest+file_path.replace(src, '')
                print(file_path, os.path.dirname(dest_path))
                print(dest_path)
                # continue
                os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                if os.path.exists(dest_path):
                    os.unlink(dest_path)
                shutil.move(file_path, os.path.dirname(dest_path))

if __name__=='__main__':
    move_known('tosec/unsorted files/vtrdos.ru/demos/dest/')
    pass