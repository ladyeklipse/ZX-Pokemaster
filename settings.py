ZX_POKEMASTER_VERSION = '1.51'
POKEMASTER_DB_PATH = 'pokemaster.db'
POKEMASTER_MIN_DB_PATH = 'minified_database/pokemaster.db'
DB_DISK_CACHE_FILE = 'hashes.dat'
LOCAL_FTP_ROOT = 'ftp'
WOS_SITE_ROOT = 'http://www.worldofspectrum.org'
WOS_MIRRORS = [
    'https://archive.org/download/World_of_Spectrum_June_2017_Mirror/World%20of%20Spectrum%20June%202017%20Mirror.zip/World%20of%20Spectrum%20June%202017%20Mirror',
    'http://spectrumcomputing.co.uk',
]
WOS_GAME_FILES_DIRECTORY = 'pub/sinclair/games'
WOS_TRDOS_GAME_FILES_DIRECTORY = 'pub/sinclair/trdos/games'
WOS_INGAME_SCREENS_DIRECTORY = 'pub/sinclair/screens/in-game'
WOS_LOADING_SCREENS_DIRECTORY = 'pub/sinclair/screens/load'
WOS_MANUALS_DIRECTORY = 'pub/sinclair/games-info'
TIPSHOP_SITE_ROOT = 'http://www.the-tipshop.co.uk'
GAME_EXTENSIONS = ['tap', 'dsk', 'z80', 'sna', 'dsk',
                   'trd', 'tzx', 'img', 'mgt', 'rom',
                   'scl', 'slt', 'szx', 'fdi', 'opd',
                   'mdr', 'wdr', 'd80', 'd40', 'sp',
                   'dck', 'ipf', 'csw', 'udi', 'spg',
                   'wmf']
ARCHIVE_EXTENSIONS =   ['zip', 'rar', '7z', 'gz', 'iso', 'tar',
                        'bz2', 'bzip2', 'tbz2', 'tbz',
                        'gz', 'gzip', 'tgz', 'tar',
                        'xz', 'txz', 'arj', 'dmg', 'iso',
                        'lzh', 'lha', 'lzma', 'r00', 'z', 'taz']
DISALLOWED_SUPPLEMENTARY_FILES = GAME_EXTENSIONS + ARCHIVE_EXTENSIONS + \
    ['pok', '$b', '$c', '$m', '$t', '$u', '$w', '$x', '$z']
DISK_FORMATS = ('dsk', 'trd', 'scl')
TAPE_FORMATS = ('tzx', 'tap')
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
GAME_PREFIXES = ['A', 'An', 'The',
                 'La', 'Le', 'De', "L'", "D'"
                 'Les', 'Los', 'Las', 'El',
                 'Une', 'Una', 'Uno',
                 'Het',
                 'Der', 'Die', 'Das']
SIDE_A = 1
SIDE_B = 2
PREDEFINED_OUTPUT_PATH_STRUCTURES = [
    '/{TOSECName}',
    '{Letter}/{TOSECName}',
    '{Letter}/{Name}/{TOSECName}',
    '{Genre}/{Year}/{TOSECName}',
    '{Publisher}/{Year}/{GameName}/{TOSECName}',
    '{Genre}/{Publisher}/{TOSECName}',
    '{MachineType}/{MaxPlayers}/{Genre}/{TOSECName}',
    '{Genre}/{MaxPlayers}/{Letter}/{TOSECName}'
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
    ('it', 'Italian'),
    ('hu', 'Hungarian'),
    ('no', 'Norwegian'),
    ('pl', 'Polish'),
    ('pt', 'Portuguese'),
    ('sh', 'Serbo-Croatian'),
    ('sr', 'Serbian'),
    ('sk', 'Slovak'),
    ('sl', 'Slovenian'),
    ('sv', 'Swedish')
]
COUNTRY_LANGUAGE_DICT = {
    'GB':'en',
    'AU':'en',
    'US':'en',
    'AR':'es',
    'BR':'pt',
    'CZ':'cs',
    'SI':'sl',
    '':'en',
}
TOSEC_COMPLIANT_FILENAME_STRUCTURE = \
    '{GameName} ({Year})({Publisher})({MachineType})({Country})({Language})({Media}){ModFlags}{Notes}'
DEFAULT_MACHINE_TYPE = '48K'
DEFAULT_GAME_LANGUAGE = 'en'
OUTPUT_PATH_STRUCTURE_KEYS = [
    'Type',
    'Genre',
    'Type',
    'Year',
    'Letter',
    'MachineType',
    'Publisher',
    'MaxPlayers',
    'GameName',
    'Language',
    'Format',
    'Side',
    'Part',
    'ModFlags'
    'ZXDB_ID',
    'Notes',
    'TOSECName'
]
MOD_FLAGS_ORDER = ['cr', 'f', 'h', 'm', 'p', 't', 'tr', 'o', 'u', 'v', 'b']
X_RATED_FLAG = '[adult]'
COVERTAPE_PUBLISHERS = ['Your Sinclair', 'Crash', 'Sinclair User', 'Run Magazine']