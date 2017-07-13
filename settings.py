LOCAL_GAME_FILES_DIRECTORY = 'wos_games'
LOCAL_FTP_ROOT = 'ftp'
WOS_SITE_ROOT = 'http://www.worldofspectrum.org'
WOS_MIRRORS = [
    'http://spectrumcomputing.co.uk',
    'https://wos.meulie.net',
    WOS_SITE_ROOT,
]
WOS_GAME_FILES_DIRECTORY = 'pub/sinclair/games'
WOS_TRDOS_GAME_FILES_DIRECTORY = 'pub/sinclair/trdos/games'
WOS_INGAME_SCREENS_DIRECTORY = 'pub/sinclair/screens/in-game'
WOS_LOADING_SCREENS_DIRECTORY = 'pub/sinclair/screens/load'
WOS_MANUALS_DIRECTORY = 'pub/sinclair/games-info'
TIPSHOP_SITE_ROOT = 'http://www.the-tipshop.co.uk'
GAME_EXTENSIONS = ['tap', 'dsk', 'z80', 'sna', 'dsk', 'trd', 'tzx', 'img', 'mgt', 'rom', 'scl', 'slt', 'szx']
MAX_ZIP_FILE_SIZE = 8858353
# AVAILABILITY_AVAILABLE = 'A'
# AVAILABILITY_DISTRIBUTION_DENIED = 'D'
# AVAILABILITY_DISTRIBUTION_DENIED_STILL_FOR_SALE = 'd'
# AVAILABILITY_MISSING_IN_ACTION = '?'
# AVAILABILITY_NEVER_RELEASED = 'N'
# AVAILABILITY_RECOVERED = 'R'
# MULTIPLAYER_TYPE_COOP = 'c'
# MULTIPLAYER_TYPE_VS_COOP = 'm'
# MULTIPLAYER_TYPE_VS_TEAM = 'n'
# MULTIPLAYER_TYPE_TEAM = 't'
# MULTIPLAYER_TYPE_VS = 'v'
AVAILABILITY_TYPES = {
    'A':'Available',
    'D':'Distribution denied',
    'd':'Distribution denied (still for sale)',
    '?':'Missing in action',
    'N':'Never released',
    'R':'Recovered'
}
MULTIPLAYER_TYPES = {
    'c':'Coop',
    'm':'Vs+Coop',
    'n':'Vs+Team',
    't':'Team',
    'v':'Vs'
}
CHEAT_SOURCE_SCRAPE = 0
CHEAT_SOURCE_OLD_DB = 1
CHEAT_SOURCE_WOS_FILE = 2
CHEAT_SOURCE_NEW_DB = 99
ALPHABETIC_DIRNAMES = ['123', 'A', 'B', 'C', 'D', 'E', 'F',
                       'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                       'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                       'W', 'X', 'Y', 'Z']
GAME_PREFIXES = ['A', 'The',
                 'La', 'Le', 'De', "L'", "D'"
                 'Les', 'Los', 'Las', 'El',
                 'Une', 'Una', 'Uno',
                 'Het',
                 'Der', 'Die', 'Das']
SIDE_A = 1
SIDE_B = 2
PREDEFINED_OUTPUT_FOLDER_STRUCTURES = [
    '{Letter}',
    '{Letter}/{Name}',
    '{Genre}/{Year}',
    '{Publisher}/{Year}/{Name}',
    '{Genre}/{Publisher}',
    '{MachineType}/{NumberOfPlayers}/{Genre}',
    '{Genre}/{MultiplayerType}/{Letter}'
]
