import os
import sys
import shutil
# import version
import glob
import zipfile
from settings import ZX_POKEMASTER_VERSION
PROJECT_NAME = 'ZX Pokemaster'
INNOSETUP_APP_ID = '9D553812-52CF-4FAF-8C56-AD2F573F5EB5'

DIST_PATH = 'dist-win32' if sys.platform == 'win32' else '/tmp/dist-darwin'
original_folder = os.getcwd()

def createInstaller(project_name, python_ver="37"):
    # version.setVersion()
    executable = ""
    if 'darwin' in sys.platform:
        # executable = "python3 pyinstaller-dev-2020-01-15/pyinstaller.py"
        executable = "pyinstaller"
    else:
        executable = "C:/python{}/scripts/pyinstaller.exe".format(python_ver)
    launch_string = executable + ' {}.spec --log-level INFO --windowed -y'.format(getExecutableName(project_name))
    print(os.getcwd(), os.path.exists(getExecutableName(project_name)+'.spec'))
    launch_string += ' --distpath {}'.format(DIST_PATH)
    launch_string += " --key=fWexFwr9PwelDsgn"
    print(launch_string)
    os.system(launch_string)

def cleanup(project_name):
    if sys.platform == 'win32':
        os.chdir('dist-win32/{}'.format(project_name))
        for file in glob.glob('api-ms-win-*.dll'):
            os.remove(file)
        for file in [
            'PyQt5/Qt/plugins/platforms/qwebgl.dll',
            'PyQt5/Qt/plugins/platforms/qoffscreen.dll',
            'PyQt5/Qt/plugins/platforms/qminimal.dll'
                ]:
            if os.path.exists(file):
                os.remove(file)
        for path in ['PyQt5/Qt/bin',
                     'PyQt5/Qt/translations',
                     'PyQt5/QtBluetooth.pyd',
                     'Qt5Qml.dll',
                     'Qt5Quick.dll',
                     'Qt5WebSockets.dll',
                     'Qt5Designer.dll',
                     'Qt5WebEngineCore.dll'
                     ]:
            if os.path.exists(path):
                if os.path.isdir(path):
                    shutil.rmtree(path)
                else:
                    os.unlink(path)
    elif sys.platform == 'darwin':
        os.chdir('dist-darwin/'.format(project_name))
        for file in [
            'QtWebEngineCore'
        ]:
            if os.path.exists(file):
                os.remove(file)
    os.chdir('../..')

def createWin32Portable(project_name, project_version):
    print("Zipping...")
    zfname = '{}-{}-{}-portable'.format(getExecutableName(project_name), sys.platform, project_version)
    zfpath = '../../Output/'+zfname + '.zip'
    print(zfpath)
    os.chdir('dist-{}/{}'.format(sys.platform, project_name))
    with zipfile.ZipFile(zfpath, 'w', zipfile.ZIP_DEFLATED) as zf:
        for root, dirs, files in os.walk('.'):
            for file in files:
                if file.endswith('.log'):
                    continue
                else:
                    zf.write(os.path.join(root, file), os.path.join(root, file))
    os.chdir('../..')

def createInnoSetup(app_id, project_name, project_version):
    iss_name = "zx_pokemaster_stub.iss"
    with open(iss_name, 'r', encoding='utf-8') as temp:
        iss_template = temp.read()
        iss = iss_template.format(app_id=app_id,
                                  project_name=project_name,
                                  project_executable_name=getExecutableName(project_name),
                                  project_version=project_version)
    with open(getExecutableName(project_name)+'.iss', 'w', encoding='utf-8') as f:
        f.write(iss)
    executable = '"C:\\Program Files (x86)\\Inno Setup 6\\iscc.exe" {}.iss'.format(getExecutableName(project_name))
    print(executable)
    os.system(executable)
    installer_path = "Output//"+getDatedName(project_name, project_version)+"-installer.exe"
    if os.path.exists(installer_path):
        os.unlink(installer_path)
    os.rename("Output//{}-{}.exe".format(
        getExecutableName(project_name), project_version), installer_path)

def getDatedName(project_name, project_version):
    return '{}-{}-{}'.format(getExecutableName(project_name), project_version, sys.platform)

def getExecutableName(project_name):
    return project_name.replace(' ', '_')

def generatePlist(project_name, project_version, project_icon):
    plist_path = "{}/Bundle/{}.app/Contents/info.plist".format(DIST_PATH, project_name)
    exec_name = getExecutableName(project_name)
    plist_stub_path = "assets/info.plist.stub".format(exec_name)
    if os.path.exists(plist_path):
        os.unlink(plist_path)
    with open(plist_stub_path, 'r', encoding='utf-8') as f:
        plist_contents = f.read().format(PROJECT_NAME=project_name,
                                         PROJECT_VERSION=project_version,
                                         PROJECT_ICON=project_icon)
    with open(plist_path, 'w', encoding='utf-8') as f:
        f.write(plist_contents)

def createBundle(project_name, project_version, project_icon):
    os.chdir(original_folder)
    print(os.getcwd())
    exec_name = getExecutableName(project_name)
    print('exec_name =', exec_name)
    if os.path.exists("{}/Bundle/{}.app".format(DIST_PATH, project_name)):
        shutil.rmtree("{}/Bundle/{}.app".format(DIST_PATH, project_name))
    os.makedirs("{}/Bundle/{}.app".format(DIST_PATH, project_name), exist_ok=True)
    os.makedirs("{}/Bundle/{}.app/Contents/Resources".format(DIST_PATH, project_name), exist_ok=True)
    icon_path = os.path.join('assets', project_icon)
    shutil.copy(icon_path,
                "{}/Bundle/{}.app/Contents/Resources/{}".format(DIST_PATH, project_name, icon_name))
    generatePlist(project_name, project_version, project_icon)
    shutil.copytree('{}/{}'.format(DIST_PATH, project_name),
                "{}/Bundle/{}.app/Contents/MacOS".format(DIST_PATH, project_name))

def createDmg(project_name, project_version):
    exec_name = getExecutableName(project_name)
    executable = "appdmg {}_dmg.json {}.dmg".format(exec_name, exec_name)
    os.system("hdiutil detach /dev/disk2")
    os.system("rm {}.dmg".format(exec_name))
    os.system(executable)
    os.rename("{}-installer.dmg".format(exec_name), "Output/{}.dmg".format(getDatedName(project_name, project_version)))

if __name__=='__main__':
    createInstaller(PROJECT_NAME)
    cleanup(PROJECT_NAME)
    if sys.platform == 'darwin':
        createBundle(PROJECT_NAME, ZX_POKEMASTER_VERSION)
        createDmg(PROJECT_NAME, ZX_POKEMASTER_VERSION)
    if sys.platform == 'win32':
        createWin32Portable(PROJECT_NAME, ZX_POKEMASTER_VERSION)
        createInnoSetup(INNOSETUP_APP_ID, PROJECT_NAME, ZX_POKEMASTER_VERSION)