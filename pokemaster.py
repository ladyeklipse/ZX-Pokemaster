import sys
sys.path.append("ui")
from PyQt4.QtCore import *
from PyQt4.QtGui import *
# from PyQt4.QtWidgets import *
from ui.SorterLauncher import *
from classes.sorter import *
from scripts.is_pathname_valid import *
import traceback
import threading
from pattern_creator import PatternCreatorDialog
import json
from settings import MESSAGE_BOX_TITLE

def PyQtExceptHook(exc_cls, ex, tb):
    MESSAGE = str(ex)+'\n'
    MESSAGE += ''.join(traceback.format_tb(tb))
    QMessageBox.critical(None, exc_cls.__name__, MESSAGE)

class MainDialog(QDialog):

    last_added_dir = None

    def __init__(self, parent=None):
        super(QDialog, self).__init__()
        self.ui = Ui_Dialog()
        self.ui.setupUi(self)
        self.ui.btnAddPath.clicked.connect(self.addInputPath)
        self.ui.btnRemovePaths.clicked.connect(self.removeSelectedInputPaths)
        self.ui.btnBrowseOutputPath.clicked.connect(self.browseOutputPath)
        self.ui.btnAddPattern.clicked.connect(self.addPattern)
        self.ui.btnRemovePattern.clicked.connect(self.removePattern)
        self.ui.btnSortFiles.clicked.connect(self.sortFiles)
        self.loadSettings()
        self.exec()

    def addInputPath(self):
        dir_path = self.getDirectoryFromFileDialog()
        if dir_path:
            self.ui.lstInputPaths.addItem(dir_path)
            self.last_addded_dir = dir_path

    def removeSelectedInputPaths(self):
        for item in self.ui.lstInputPaths.selectedItems():
            self.ui.lstInputPaths.takeItem(self.ui.lstInputPaths.row(item))

    def browseOutputPath(self):
        dir_path = self.getDirectoryFromFileDialog()
        if dir_path:
            self.ui.txtOutputPath.setText(dir_path)

    def getDirectoryFromFileDialog(self):
        dir_path = QFileDialog.getExistingDirectory(self, self.tr('Add folder'),
                      self.last_added_dir,
                      QFileDialog.ShowDirsOnly | QFileDialog.DontResolveSymlinks)
        if os.name=='nt':
            dir_path = dir_path.replace('/', '\\')
        return dir_path

    def addPattern(self):
        dialog = PatternCreatorDialog(parent=self)
        pattern = dialog.getPattern()
        if pattern:
            for i in range(self.ui.cmbOutputFolderStructure.count()):
                old_pattern = self.ui.cmbOutputFolderStructure.itemText(i)
                if pattern == old_pattern:
                    self.ui.cmbOutputFolderStructure.setCurrentIndex(i)
                    return
            self.ui.cmbOutputFolderStructure.insertItem(0, dialog.getPattern())
            self.ui.cmbOutputFolderStructure.setCurrentIndex(0)

    def removePattern(self):
        self.ui.cmbOutputFolderStructure.removeItem(self.ui.cmbOutputFolderStructure.currentIndex())

    def sortFiles(self):
        kwargs = {
            'input_locations':self.getInputLocations(),
            'traverse_subdirectories':self.ui.chkTraverseSubdirectories.isChecked(),
            'output_location':self.ui.txtOutputPath.text(),
            'formats_preference':self.getFormatsPreference(),
            'output_folder_structure':self.getOutputFolderStructure(),
            'ignore_alternate':not self.ui.chkIncludeAlternate.isChecked(),
            'ignore_alternate_formats':not self.ui.chkIncludeAlternateFileFormats.isChecked(),
            'ignore_rereleases':not self.ui.chkIncludeRereleases.isChecked(),
            'ignore_hacks':not self.ui.chkIncludeHacked.isChecked(),
            'place_pok_files_in_pokes_subfolders':self.ui.chkPlacePokFilesIntoPOKESSubfolder.isChecked(),
        }
        if not is_pathname_valid(kwargs['output_location']):
            QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr('Invalid output path'))
            return
        for format in kwargs['formats_preference']:
            if format not in GAME_EXTENSIONS:
                QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr('Format %s is not recognized') % format)
                return
        self.saveSettings(kwargs)
        if not kwargs['input_locations']:
            QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr('Please add one or more input path(s).'))
            return

        kwargs['gui'] = self
        self.bar = QProgressDialog(self.tr("Sorting..."),
                              self.tr("Cancel"), 0, 0, self)
        self.bar.setWindowTitle('Sorting')
        self.bar.setLabelText(self.tr("Please wait"))
        self.bar.setFixedWidth(400)
        self.bar.setAutoClose(True)
        self.bar.show()
        s = Sorter(**kwargs)
        self.bar.canceled.connect(s.cancel)
        s.sortFiles()
        self.bar.hide()
        if s.should_cancel:
            QMessageBox.information(self, MESSAGE_BOX_TITLE, self.tr('Operation was canceled.'))
        elif s.too_long_path:
            QMessageBox.information(self, MESSAGE_BOX_TITLE,
                                    self.tr('Path %s is too long. Please try another output location.' % s.too_long_path))
        else:
            QMessageBox.information(self, MESSAGE_BOX_TITLE, self.tr('Sorting successfully finished.'))
        self.bar.close()

    def getInputLocations(self):
        input_locations = []
        for i in range(self.ui.lstInputPaths.count()):
            input_locations.append(self.ui.lstInputPaths.item(i).text())
        return input_locations

    def getFormatsPreference(self):
        formats = self.ui.txtFormatPreference.text()
        formats = formats.replace(';', ',').lower()
        formats = [x.strip() for x in formats.split(',') if x]
        return formats

    def getOutputFolderStructure(self):
        index = self.ui.cmbOutputFolderStructure.currentIndex()
        item = self.ui.cmbOutputFolderStructure.itemText(index)
        return item

    def updateProgressBar(self, current_value=0, max_value=None, label=None):
        print('updating progress bar')
        self.bar.setValue(current_value)
        if max_value:
            self.bar.setMaximum(max_value)
        if label:
            self.bar.setLabelText(self.tr(label))
        QCoreApplication.instance().processEvents()

    def loadSettings(self):
        try:
            with open('settings.json', 'r', encoding='utf-8') as f:
                settings = json.load(f)
                patterns = settings.get('patterns', PREDEFINED_OUTPUT_FOLDER_STRUCTURES)
                if os.name=='nt':
                    patterns = [pattern.replace('/', '\\') for pattern in patterns]
                for i, pattern in enumerate(patterns):
                    self.ui.cmbOutputFolderStructure.addItem(pattern)
                    if pattern == settings.get('output_folder_structure'):
                        self.ui.cmbOutputFolderStructure.setCurrentIndex(i)
                self.ui.lstInputPaths.addItems(settings.get('input_locations', []))
                self.ui.chkTraverseSubdirectories.setChecked(settings.get('traverse_subridrectories', True))
                self.ui.txtOutputPath.setText(settings.get('output_location', ''))
                self.ui.txtFormatPreference.setText(','.join(settings.get('formats_preference', [','.join(GAME_EXTENSIONS)])))
                self.ui.chkIncludeAlternate.setChecked(not settings.get('ignore_alternate', True))
                self.ui.chkIncludeAlternateFileFormats.setChecked(not settings.get('ignore_alternate_formats', False))
                self.ui.chkIncludeRereleases.setChecked(not settings.get('ignore_rereleases', False))
                self.ui.chkIncludeHacked.setChecked(not settings.get('ignore_hacks', False))
                self.ui.chkPlacePokFilesIntoPOKESSubfolder.setChecked(settings.get('place_pok_files_in_pokes_subfolders', True))
        except:
            print(traceback.format_exc())
            patterns = PREDEFINED_OUTPUT_FOLDER_STRUCTURES
            if os.name == 'nt':
                patterns = [pattern.replace('/', '\\') for pattern in patterns]
            self.ui.cmbOutputFolderStructure.addItems(patterns)
            self.ui.cmbOutputFolderStructure.setCurrentIndex(0)
            self.ui.txtOutputPath.setText(os.getcwd())
            self.ui.txtFormatPreference.setText(','.join(GAME_EXTENSIONS))

    def saveSettings(self, kwargs):
        kwargs['patterns'] = self.getOutputFolderStructurePatterns()
        with open('settings.json', 'w+', encoding='utf-8') as f:
            json.dump(kwargs, f, indent=4)

    def getOutputFolderStructurePatterns(self):
        return [self.ui.cmbOutputFolderStructure.itemText(i) \
         for i in range(self.ui.cmbOutputFolderStructure.count())]

if __name__=='__main__':
    sys.excepthook = PyQtExceptHook
    app = QApplication(sys.argv)
    pokemaster = MainDialog()
