# from PyQt5.QtCore import *
# from PyQt5.QtGui import *
# from PyQt5.QtWidgets import *
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.OutputFolderStructureEditor import *
from classes.game_file import GameFile
from classes.game import Game
import os

class PatternCreatorDialog(QDialog):

    def __init__(self):
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.buttons = [
            self.ui.btnGenre, self.ui.btnMachineType, self.ui.btnYear,
            self.ui.btnPublisher, self.ui.btnGameName, self.ui.btnLanguage,
            self.ui.btnLetter, self.ui.btnNumberOfPlayers, self.ui.btnSlash
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
            self.ui.lblExample.setText(example_path.format(**kwargs))
        except Exception as e:
            self.ui.lblExample.setText(str(e))

    def getPattern(self):
        pattern = self.ui.txtOutputPath.text()
        return pattern