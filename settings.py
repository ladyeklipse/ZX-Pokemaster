POKEMASTER_DB_PATH = 'C:\\ZX Pokemaster\\pokemaster.db'
LOCAL_FTP_ROOT = 'C:\\ZX Pokemaster\\ftp'
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
MAX_GAME_NAME_LENGTH = 100
MIN_GAME_NAME_LENGTH = 30
MAX_DESTINATION_PATH_LENGTH = 240
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
ALPHABETIC_DIRNAMES = ['123', 'a', 'b', 'c', 'd', 'e', 'f',
                       'g', 'h', 'i', 'j', 'k', 'l', 'm', 'n',
                       'o', 'p', 'q', 'r', 's', 't', 'u', 'v',
                       'w', 'x', 'y', 'z']
GAME_PREFIXES = ['A', 'The',
                 'La', 'Le', 'De', "L'", "D'"
                 'Les', 'Los', 'Las', 'El',
                 'Une', 'Una', 'Uno',
                 'Het',
                 'Der', 'Die', 'Das']
SIDE_A = 1
SIDE_B = 2
PREDEFINED_OUTPUT_FOLDER_STRUCTURES = [
    '/{TOSECName}',
    '{Letter}/{TOSECName}',
    '{Letter}/{Name}/{TOSECName}',
    '{Genre}/{Year}/{TOSECName}',
    '{Publisher}/{Year}/{GameName}/{TOSECName}',
    '{Genre}/{Publisher}/{TOSECName}',
    '{MachineType}/{NumberOfPlayers}/{Genre}/{TOSECName}',
    '{Genre}/{MultiplayerType}/{Letter}/{TOSECName}'
]
MESSAGE_BOX_TITLE = 'ZX Pokemaster'
INCLUDED_TYPES_LIST = [
    ''
]
INCLUDED_LANGUAGES_LIST = [
    ('en', 'English'),
    ('es', 'Spanish'),
    ('ru', 'Russian'),
    ('hr', 'Croatian'),
    ('cz', 'Czech'),
    ('nl', 'Dutch'),
    ('de', 'German'),
    ('fr', 'French'),
    ('hu', 'Hungarian'),
    ('no', 'Norwegian'),
    ('pl', 'Polish'),
    ('sr', 'Serbian'),
    ('sl', 'Slovak'),
    ('sv', 'Swedish')
]
TOSEC_COMPLIANT_FILENAME_STRUCTURE = \
    '{GameName} ({Year})({Publisher})({Language})({Part})({Side})[{MachineType}]{ModFlags}{Notes}.{Format}'
DEFAULT_MACHINE_TYPE = '48K'
DEFAULT_GAME_LANGUAGE = 'en'