from settings import *
import re
import unicodedata

publisher_regex = re.compile(' Software| inc$|inc[ .]|ltd|plc|S\.A\.', re.IGNORECASE)
filepath_regex = re.compile('\*|\?|\:|\||\\|/|\"|<|>|\"')
remove_square_brackets_regex = re.compile('\[[^\]]*\]')

MEANINGLESS_WORDS = [
    'of', 'the', 'in',
    'an', 'at', 'for'
]

def getMeaningfulEightLetterName(game_name):
    if not game_name:
        return ''
    # if ',' in game_name and [x for x in GAME_PREFIXES if x in game_name.lower()]:
    game_name_split = game_name.split(',')[0]
    if len(game_name_split)>2:
        game_name = game_name_split
    game_name = ''.join([x for x in game_name if x.isalnum() or x==' '])
    game_name = ' '.join([x for x in game_name.split(' ') if \
                          x.lower() not in MEANINGLESS_WORDS])
    game_name = game_name.replace(' II', ' 2').replace(' III', ' 3').replace(' IV', ' 4')
    # words = [word for word in game_name.split(' ') if len(word)>1 or word.isdigit()]
    words = [word for word in game_name.split(' ') if word]
    if len(words)==1:
        name = words[0][:8]
    elif len(words)==2:
        first_word_length = len(words[0])
        if first_word_length>4:
            first_word_length = 8-len(words[1][:3])
            if first_word_length>7:
                first_word_length=4
            elif first_word_length<1:
                first_word_length = len(words[0][:3])
        name = words[0][:first_word_length] + words[1][:(8-first_word_length)]
    else:
        first_word_length = len(words[0])
        second_word_length = len(words[1])
        third_word_length = len(words[2])
        if first_word_length>3:
            first_word_length = 8-len(words[2][:2])-len(words[0][:3])
            if first_word_length>7:
                first_word_length=4
            elif first_word_length<1:
                first_word_length = len(words[0][:3])
        second_word_length = len(words[1])
        if second_word_length>3 and first_word_length+third_word_length>5:
            second_word_length = 3
        third_word_length = 8-second_word_length-first_word_length
        name = words[0][:first_word_length]+words[1][:second_word_length]+words[2][:third_word_length]
        if len(name)<8 and len(words)>3:
            name += words[3][:(8-len(name))]
    return name.upper()

def getWosSubfolder(filepath):
    return '123' if not filepath[0].isalpha() else filepath[0].lower()

def getFileSystemFriendlyName(name):
    if not name:
        return ''
    name = name.replace(':', ' -').replace('/','-')
    name = ' '.join([word[0].upper()+word[1:].rstrip()
                     if len(word)>3 and '.' not in word
                     else word.strip() for word in name.split(' ')])
    name = filepath_regex.sub('', name).strip()
    deunicoded_name = unicodedata.normalize('NFKD', name).encode('ascii', 'ignore').decode('ascii')
    if deunicoded_name:
        return deunicoded_name
    return name

def putPrefixToEnd(game_name):
    if not game_name:
        return ''
    components = re.split(' - | \+ ', game_name)
    for i, component in enumerate(components):
        if len(component)<5:
            continue
        if component.startswith('Die Hard'):
            continue
        if component.endswith(', 3D'):
            component = '3D '+component[:-4]
        for prefix in GAME_PREFIXES:
            if component.startswith(prefix + ' '):
                components[i] = ' '.join(component.split(' ')[1:]) + ', ' + prefix
                break
    game_name = ''.join(components)
    return game_name

def getSearchStringFromGameName(game_name):
    if not game_name:
        return ''
    for prefix in GAME_PREFIXES:
        if game_name.startswith(prefix + ' '):
            game_name = game_name[len(prefix)+1:]
            break
        elif game_name.endswith(', '+prefix):
            game_name = game_name[:len(game_name)-len(prefix)-2]
    return ''.join(filter(str.isalnum, game_name.lower()))
