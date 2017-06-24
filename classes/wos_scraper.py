#
#   DEPRECATED
#

from classes.scraper import Scraper
from classes.game import Game
from classes.game_file import GameFile
from classes.selector import Selector
from settings import *
import urllib.parse
import os

ALPHABET = '1abcdefghijklmnopqrstuvwxyz'

class WosScraper(Scraper):

    def getGamesList(self):
        games_list = []
        for letter in ALPHABET:
            letter_games_list = self.loadGamesListForLetter(letter)
            games_list += letter_games_list
        return games_list

    def loadGamesListForLetter(self, letter, folder='games'):
        url = WOS_SITE_ROOT+'/'+folder+'/{}.html'.format(letter)
        selector = self.loadUrl(url)
        games_list = []
        game_links = selector.xpath('//body//pre//a').extract_all()
        for game_link in game_links:
            game_link = Selector(game_link)
            game_name = game_link.xpath('//text()').text()[0]
            game_url = game_link.xpath('//a/@href').extract_first()
            game_url_query_string = game_url.split('?')[1]
            game_wos_id = int(urllib.parse.parse_qs(game_url_query_string)['id'][0])
            game = Game(game_name, game_wos_id)
            games_list.append(game)
        return games_list

    def scrapeGameData(self, game=Game()):
        url = game.getWosUrl()
        selector = self.loadUrl(url)
        tables = selector.xpath('//table').extract_all()
        desc_table = Selector(text=tables[5])
        desc_rows = desc_table.xpath('//tr').extract_all()
        for row in desc_rows:
            row_text = self.getTextFromDescriptionRow(row)
            if not row_text:
                continue
            caption = row_text[0]
            value = row_text[1]
            if caption == 'Full title':
                if value.startswith('[MOD]'):
                    value = row_text[2]
                game.setTitle(value)
            elif caption == 'Year of release':
                game.setYear(value)
            elif caption == 'Publisher':
                game.setPublisher(value)
            elif caption == 'Machine type':
                game.setMachineType(value)
            elif caption == 'Number of players':
                game.setNumberOfPlayers(value)
            elif caption == 'Type':
                game.setGenre(value)
            elif caption == 'Availability':
                game.setAvailability(value)
        # if game.availability > AVAILABILITY_AVAILABLE:
        #     return
        has_tipshop_pokes = selector.xpath('//img[@title="Search The Tipshop"]/@title').extract_first()
        if has_tipshop_pokes=='Search The Tipshop':
            game.has_tipshop_pokes = True
        game_files, additional_materials = self.getFilesLists(tables[4:])
        self.scrapeGameFiles(game, game_files)
        self.scrapeAdditionalMaterials(game, additional_materials)

    def scrapeGameFiles(self, game, game_files):
        for i, game_file_info in enumerate(game_files[1:]):
            game_file_info = Selector(game_file_info)
            cells = game_file_info.xpath('//td').extract()
            java_link = Selector(cells[0]).xpath('//a/@title').extract_first()
            file_link = Selector(cells[2]).xpath('//a/@href').extract_first()
            # file_link = game.sanitizeWosUrl(file_link)
            file_size = Selector(cells[3]).xpath('//text()').extract_first()
            game_file = GameFile(file_link, file_size, game)
            if game_file.format not in GAME_EXTENSIONS:
                continue
            if java_link:
                if '128K' in java_link:
                    game.setMachineType('128K')
                    # game_file.machine_type = '128K'
                # elif '48K' in java_link:
                #     game_file.machine_type = '48K'
            game.addFile(game_file)

    def scrapeAdditionalMaterials(self, game, additional_materials):
        for i, row in enumerate(additional_materials[1:]):
            cells = Selector(row).xpath('//td').extract()
            if len(cells)<4:
                continue
            type = Selector(cells[3]).xpath('//text()').extract_first()
            if not type.startswith('('):
                continue
            elif type=='(Loading screen)':
                game.setLoadingScreenUrl(*self.fileInfoFromRow(cells))
            elif type=='(Loading screen dump)':
                game.setLoadingScreenUrl(*self.fileInfoFromRow(cells))
            elif type=='(In-game screen)':
                # url = Selector(cells[1]).xpath('//a/@href').extract_first()
                game.setIngameScreenUrl(*self.fileInfoFromRow(cells))
            elif 'instructions' in type:
                if 'English' in type or not game.getManualUrl():
                    # manual_url = Selector(cells[1]).xpath('//a/@href').extract_first()
                    url, size = self.fileInfoFromRow(cells)
                    if url.endswith('.txt'):
                        game.setManualUrl(url, size)

    def fileInfoFromRow(self, cells):
        url = Selector(cells[1]).xpath('//a/@href').extract_first()
        size = Selector(cells[2]).xpath('//text()').extract_first()
        return url, size

    def getTextFromDescriptionRow(self, desc_row):
        s = Selector(text=desc_row)
        text = s.xpath('//td//text()').extract_all()
        return text

    def getFilesLists(self, tables):
        game_files_table_selector, additional_materials_table_selector = None, None
        for table in tables:
            table_selector = Selector(table)
            table_cell_caption = table_selector.xpath('//tr[1]//td//text()').extract()
            if (table_cell_caption[:4]==['Filename', 'Size', 'Type', 'Origin']):
            # if len(table_caption)==7:
                game_files_table_selector = table_selector
            elif (table_cell_caption[:4]==['Filename', 'Size', 'Type', '\n']):
                additional_materials_table_selector = table_selector
        game_files = game_files_table_selector.xpath('//tr').extract_all() \
            if game_files_table_selector else []
        additional_materials = additional_materials_table_selector.xpath('//tr').extract_all() \
            if additional_materials_table_selector else []
        return game_files, additional_materials

    def downloadFiles(self, game=Game()):
        for file in game.files:
            local_path = file.getLocalPath(zipped=True)
            if os.path.exists(local_path) and \
                os.path.getsize(local_path):#==file.size:
                continue
            else:
                for mirror in WOS_MIRRORS:
                    status = self.downloadFile(file.getWosPath(wos_mirror_root=mirror), local_path)
                    if status==200:
                        break


        if game.ingame_screen_gif_size:
            if not os.path.exists(game.getLocalIngameScreenPath('gif')) or \
                    os.path.getsize(game.getLocalIngameScreenPath('gif'))!=game.ingame_screen_gif_size:
                self.downloadFile(game.getRemoteIngameScreenUrl('gif'), game.getLocalIngameScreenPath('gif'))

        if game.loading_screen_scr_size:
            if not os.path.exists(game.getLocalLoadingScreenPath('scr')) or \
                os.path.getsize(game.getLocalLoadingScreenPath('scr'))!=game.loading_screen_scr_size:
                self.downloadFile(game.getRemoteLoadingScreenUrl('scr'),
                                  game.getLocalLoadingScreenPath('scr'))

        if game.loading_screen_gif_size:
            if not os.path.exists(game.getLocalLoadingScreenPath(format='gif')) or \
                os.path.getsize(game.getLocalLoadingScreenPath('gif')) != game.loading_screen_gif_size:
                self.downloadFile(game.getRemoteLoadingScreenUrl('gif'), game.getLocalLoadingScreenPath('gif'))

        if game.manual_size:
            #No filesize check, because WoS shows wrong filesize for many manuals.
            if not os.path.exists(game.getLocalManualPath()):# or \
                    #os.path.getsize(game.getLocalManualPath())!=game.manual_size:
                self.downloadFile(game.getRemoteManualUrl(), game.getLocalManualPath())
