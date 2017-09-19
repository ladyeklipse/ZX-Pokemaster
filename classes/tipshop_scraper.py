from classes.scraper import *
from classes.game import Game
from classes.poke import Poke
from classes.cheat import Cheat
from settings import *
from string import ascii_letters
import re

SANITIZE_DESC_CHARS = ['POKE', '->', ',', ':', '.',
                       'x=', 'x =', 'X=', 'X = ',
                       'n = ', 'n=', 'N=','N =',
                       '= x', '=x',
                       '=', '\t', '\r', '\n']
poke_regex = re.compile('([0-9]{5},(\s{0,})?[0-9xXnN]{1,})')


def find_range(array, a, b):
    try:
        start = array.index(a)
    except ValueError:
        return []
    end = len(array)
    for each in b:
        try:
            end_candidate = array.index(each)
        except ValueError:
            continue
        if end_candidate>-1 and end_candidate<end:
            end = end_candidate
    return array[start+1:end]

class TipshopScraper(Scraper):

    def __init__(self):
        self.name_replace_dict = {}
        with open('tipshop_aliases.csv', 'r', encoding='utf-8') as f:
            for line in f.readlines():
                line = line.split(';')
                if len(line)==1:
                    continue
                else:
                    self.name_replace_dict[line[0].strip()] = line[1].strip()

    def getList(self, letter):
        url = TIPSHOP_SITE_ROOT+'/getlist/'+letter+'.htm'
        selector = self.loadUrl(url)
        links = selector.xpath('//table//a/@href').extract_all()
        return links

    def getWosIdFromUrl(self, url):
        selector = self.loadUrl(url)
        wos_id_container = selector.xpath('//font[@size="3"]//a/@href').extract_first()
        if not wos_id_container:
            print(url, 'has no wos_id')
        else:
            wos_id = wos_id_container[-7:]
            if wos_id.isdigit():
                return int(wos_id)
        wos_name = selector.xpath('//font[@size="7"]//text()').extract_first()
        if self.name_replace_dict.get(wos_name):
            wos_name = self.name_replace_dict[wos_name]
            if wos_name.isdigit():
                return int(wos_name)
        return wos_name

    def scrapePokes(self, game=Game()):
        if not game.wos_id:
            return
        url = game.getTipshopUrl()
        print(url)
        try:
            selector = self.loadUrl(url)
            pure_text = selector.xpath('//text()').extract_all()
            strings = find_range(pure_text, 'Download full POKE database', ['Complete solutions', 'Type-in hacks'])
            self.getPokesFromStrings(game, strings)
        except:
            print(traceback.format_exc())

    def getPokesFromStrings(self, game, strings):
        strings = [x.strip() for x in strings if x.strip()]
        game.tipshop_multiface_pokes_section = '\n'.join(strings)
        i = 0
        while i<len(strings):
            string = strings[i]
            possible_pokes = self.getPossiblePokesFromString(string)
            # print('string=', string)
            # print('possible pokes = ',possible_pokes)
            if not possible_pokes:
                i += 1
                continue
            possible_desc = self.getPossibleDescriptionFromString(string)
            for poke in possible_pokes:
                possible_desc = possible_desc.replace(poke,'').strip()
            possible_desc = possible_desc.replace(':', '').replace('POKE', '').strip()

            for char in SANITIZE_DESC_CHARS:
                possible_desc = possible_desc.replace(char, '')
            if not possible_desc or len(possible_desc)<4 or \
                    not any([x for x in ascii_letters if x in possible_desc]):
                desc = strings[i-1].strip()
            else:
                desc = possible_desc.strip()
            for char in SANITIZE_DESC_CHARS:
                desc = desc.replace(char, '')
            if not desc and i+1!=len(strings):
                possible_pokes_on_next_string = self.getPossiblePokesFromString(strings[i+1])
                if not possible_pokes_on_next_string:
                    desc = strings[i+1]
                    i += 1
            desc = ' '.join([x for x in desc.split(' ') if x.strip()])
            while desc.startswith('-'):
                desc = desc[1:].lstrip()
            while desc.endswith('-'):
                desc = desc[:-1].rstrip()
            while desc.startswith(';'):
                desc = desc[1:].lstrip()
            if desc.startswith('(') and desc.endswith(')'):
                desc = desc[1:-1].lstrip()
            # if desc:
            #     desc = desc[0].upper() + desc[1:]
            j = i
            while True:
                j += 1
                if j>=len(strings):
                    break
                possible_pokes_continued = self.getPossiblePokesFromString(strings[j])
                # possible_next_description = self.getPossibleDescriptionFromString(string)
                possible_next_description = self.getPossibleDescriptionFromString(strings[j])
                for char in SANITIZE_DESC_CHARS+[x for x in ' 0123456789nxNX,']:
                    possible_next_description = possible_next_description.replace(char, '')

                if not possible_pokes_continued:
                    break
                elif possible_next_description:
                    break
                else:
                    possible_pokes += possible_pokes_continued
                    # i+=1
                    # j+=1
            self.addCheatToGame(desc, possible_pokes, game)
            i += 1

    def getPossiblePokesFromString(self, string):
        return [x[0] for x in re.findall(poke_regex, string) if x]

    def getPossibleDescriptionFromString(self, string):
        return string.strip()
        # text_outside_brackets =  re.sub(r'\([^)]*\)', '', string).strip()
        # text_inside_brackets = re.findall(r'\([^)]*\)'
        # string_without_brackets = re.sub(r'\([^)]*\)', '', string.strip())
        # return string_without_brackets

    def addCheatToGame(self, desc, possible_pokes, game):
        print('"' + desc + '"')
        print(possible_pokes)
        if desc and possible_pokes and \
                                3 < len(desc) < 100 and not desc.isdigit():
            c = Cheat(desc)
            try:
                for poke in possible_pokes:
                    poke = poke.split(',')
                    c.addPoke(poke[0], poke[1])
            except ValueError:
                pass
            finally:
                game.addCheat(c)
