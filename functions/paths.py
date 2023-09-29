import os
import sys
if sys.platform=='win32':
    import winreg

def getAppDataFolder():
    if sys.platform == 'win32':
            app_data_folder = winreg.ExpandEnvironmentStrings("%appdata%")
    else:  # mac
        app_data_folder = os.path.join(os.path.expanduser("~"),
                                           "Library", "Application Support")
    return app_data_folder

def getDefaultSettingsPath():
    return os.path.join(getAppDataFolder(), 'ZX Pokemaster', 'settings.json')