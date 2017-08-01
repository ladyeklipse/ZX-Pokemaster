# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.OutputFolderStructureEditor import *
from classes.game_file import GameFile
from classes.game import Game
from settings import *
import os
import re
from settings import MESSAGE_BOX_TITLE
from scripts.is_pathname_valid import *

class PatternCreatorDialog(QDialog):

    example_is_valid = False

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.buttons = [
            self.ui.btnGenre, self.ui.btnMachineType, self.ui.btnYear, self.ui.btnPart,
            self.ui.btnPublisher, self.ui.btnGameName, self.ui.btnLanguage, self.ui.btnSide,
            self.ui.btnLetter, self.ui.btnNumberOfPlayers, self.ui.btnSlash, self.ui.btnModFlags,
            self.ui.btnFormat, self.ui.btnZXDB_ID, self.ui.btnHyphen, self.ui.btnUnderscore
        ]
        for button in self.buttons:
            button.clicked.connect(self.addPatternComponent)
        self.ui.txtOutputFolderStructure.textChanged.connect(self.setExample)
        self.ui.txtOutputFileNameStructure.textChanged.connect(self.setExample)
        self.initGameFile()
        self.setExample()
        self.ui.txtOutputFolderStructure.setFocus()
        self.exec()

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

    def initGameFile(self):
        self.example_game_file = GameFile('Tujad (1986)(Ariolasoft UK)[48K].tap')
        self.example_game_file.game.setGenre('Arcade - Maze')
        self.example_game_file.game.wos_id = 5448

    def setExample(self):
        folder_structure, filename_structure = self.getPattern()
        kwargs = self.example_game_file.getOutputPathFormatKwargs()
        try:
            filename = self.example_game_file.getOutputName(filename_structure)
            example_path = os.path.join(folder_structure.format(**kwargs), filename)
            if not is_pathname_valid(example_path):
                raise Exception('Invalid path')
            self.ui.lblExample.setText(example_path)
            self.example_is_valid = True
        except Exception as e:
            self.ui.lblExample.setText(str(e))
            self.example_is_valid = False

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