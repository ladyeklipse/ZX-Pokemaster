import os
import re
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from classes.database import *

from classes.game_file import GameFile
from functions.is_pathname_valid import *
from settings import MESSAGE_BOX_TITLE
from ui.OutputFolderStructureEditor import *

class PatternCreatorDialog(QDialog):

    example_is_valid = False

    def __init__(self, parent=None,
                 folder_structure=None,
                 file_structure=None):
        super(QDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)

        self.buttons = [
            self.ui.btnGenre, self.ui.btnMachineType, self.ui.btnYear, self.ui.btnMedia,
            self.ui.btnPublisher, self.ui.btnGameName, self.ui.btnLanguage, self.ui.btnAuthor,
            self.ui.btnLetter, self.ui.btnNumberOfPlayers, self.ui.btnSlash, self.ui.btnModFlags,
            self.ui.btnFormat, self.ui.btnZXDB_ID, self.ui.btnHyphen, self.ui.btnUnderscore,
            self.ui.btnType, self.ui.btnNotes, self.ui.btnCountry, self.ui.btnOriginalName
        ]
        for button in self.buttons:
            button.clicked.connect(self.addPatternComponent)
        self.ui.txtOutputFolderStructure.textChanged.connect(self.setExamples)
        self.ui.txtOutputFileNameStructure.textChanged.connect(self.setExamples)
        self.initGameFiles()
        self.setExamples()
        if folder_structure:
            self.ui.txtOutputFolderStructure.setText(folder_structure)
        if file_structure:
            self.ui.txtOutputFileNameStructure.setText(file_structure)
        self.ui.txtOutputFolderStructure.setFocus()
        self.result = self.exec()

    def addPatternComponent(self):
        text = self.sender().text()
        if not text.startswith('{'):
            text = re.findall('[\(](.*?)[\)]', text)[0]
        if self.ui.txtOutputFolderStructure.hasFocus():
            elem = self.ui.txtOutputFolderStructure
            if elem.cursorPosition()==len(elem.text()) and \
                not elem.text().endswith('\\') and \
                len(elem.text())>0:
                elem.insert('\\')
            elem.insert(text)
        elif self.ui.txtOutputFileNameStructure.hasFocus():
            elem = self.ui.txtOutputFileNameStructure
            elem.insert(text)

    def initGameFiles(self):
        self.examples = []
        database = Database()
        game = database.getGameByFileMD5('200c35cb8984a40257dd8b317263d752')
        game_file = game.findFileByMD5('200c35cb8984a40257dd8b317263d752')
        game_file.src = "/pub/sinclair/games/Tujad"
        self.examples.append(game_file)
        game = database.getGameByFileMD5('93dfecdd9c7db7c39d0c10f2f155f938')
        game_file = game.findFileByMD5('93dfecdd9c7db7c39d0c10f2f155f938')
        game_file.src = "Sinclair ZX Spectrum\Compilations\Games\[TZX]\Coin-Op Hits (1990)(US Gold)(Tape 1 of 2 Side A)[Spy Hunter]"
        self.examples.append(game_file)
        game = database.getGameByFileMD5('a951bc3a62f00454eaeb6373395de185')
        # game.author = "Unknown Author"
        game_file = game.findFileByMD5('a951bc3a62f00454eaeb6373395de185')
        game_file.src = "Sinclair ZX Spectrum\Covertapes\[TZX]\Snare (demo) (1992)(Beyond Belief - Sinclair User)[cr][48-128K]"
        self.examples.append(game_file)

    def setExamples(self):
        examples = []
        for game_file in self.examples:
            folder_structure, filename_structure = self.getPattern()
            kwargs = game_file.getOutputPathFormatKwargs()
            try:
                filename = game_file.getOutputName(filename_structure)
                example_path = os.path.join(folder_structure.format(**kwargs), filename)
                if not is_pathname_valid(example_path):
                    raise Exception('Invalid path')
                # self.ui.lblExample.setText(example_path)
                examples.append(example_path)
                self.example_is_valid = True
            except Exception as e:
                self.ui.lblExample.setText(str(e))
                self.example_is_valid = False
                break
        self.ui.lblExample.setText('\r\n'.join(examples))

    def getPattern(self):
        folder_structure = self.ui.txtOutputFolderStructure.text()
        filename_structure = self.ui.txtOutputFileNameStructure.text()
        return folder_structure, filename_structure

    def getJoinedPattern(self):
        folder, filename = self.getPattern()
        if not filename:
            filename = '{TOSECName}'
        pattern = os.path.join(folder, filename)
        return pattern

    def accept(self):
        if not self.example_is_valid:
            QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr('Pattern is invalid.'))
        else:
            QDialog.accept(self)