# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.OutputFolderStructureEditor import *
from classes.game_file import GameFile
from classes.game import Game
import os
from settings import MESSAGE_BOX_TITLE
from scripts.is_pathname_valid import *

class PatternCreatorDialog(QDialog):

    example_is_valid = False

    def __init__(self, parent=None):
        super(QDialog, self).__init__(parent)
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.buttons = [
            self.ui.btnGenre, self.ui.btnMachineType, self.ui.btnYear,
            self.ui.btnPublisher, self.ui.btnGameName, self.ui.btnLanguage,
            self.ui.btnLetter, self.ui.btnNumberOfPlayers, self.ui.btnSlash,
            self.ui.btnFormat
        ]
        for button in self.buttons:
            button.clicked.connect(self.addPatternComponent)
        self.ui.txtOutputPath.textChanged.connect(self.setExample)
        self.initGameFile()
        self.exec()

    def addPatternComponent(self):
        if self.ui.txtOutputPath.cursorPosition()==len(self.ui.txtOutputPath.text()) and \
            not self.ui.txtOutputPath.text().endswith('\\') and \
            len(self.ui.txtOutputPath.text())>0:
            self.ui.txtOutputPath.insert('\\')
        self.ui.txtOutputPath.insert(self.sender().text())

    def initGameFile(self):
        self.example_game_file = GameFile('Tujad (1986)(Ariolasoft UK).tap')
        self.example_game_file.game.setGenre('Arcade - Maze')

    def setExample(self):
        kwargs = self.example_game_file.getOutputPathFormatKwargs()
        pattern = self.ui.txtOutputPath.text()
        example_path = os.path.join(pattern, self.example_game_file.getTOSECName())
        try:
            if not is_pathname_valid(example_path):
                raise Exception('Invalid path')
            self.ui.lblExample.setText(example_path.format(**kwargs))
            self.example_is_valid = True
        except Exception as e:
            self.ui.lblExample.setText(str(e))
            self.example_is_valid = False

    def getPattern(self):
        pattern = self.ui.txtOutputPath.text()
        return pattern

    def accept(self):
        if not self.example_is_valid:
            QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr('Pattern is invalid.'))
        else:
            QDialog.accept(self)