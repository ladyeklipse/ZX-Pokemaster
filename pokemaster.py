import sys

import os

if hasattr(sys, 'frozen'):
    os.chdir(os.path.dirname(sys.executable))

from settings import *
import itertools
import stat
import shutil
import zipfile
import hashlib
import json
import traceback
from functions.game_name_functions import *
from functions.is_pathname_valid import *
from classes.database import *
# db = Database()
from classes.sorter import *

sys.path.append("ui")
from PyQt4.QtCore import *
from PyQt4.QtGui import *
from ui.SorterLauncher import *
import traceback
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
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.btnAddPath.clicked.connect(self.addInputPath)
        self.ui.btnRemovePaths.clicked.connect(self.removeSelectedInputPaths)
        self.ui.btnBrowseOutputPath.clicked.connect(self.browseOutputPath)
        self.ui.btnAddPattern.clicked.connect(self.addPattern)
        self.ui.btnEditPattern.clicked.connect(self.editPattern)
        self.ui.btnRemovePattern.clicked.connect(self.removePattern)
        self.ui.btnSortFiles.clicked.connect(self.sortFiles)
        self.ui.chkMaxFilesPerFolder.toggled['bool'].connect(lambda state:
             self.enableMaxFilesPerFolder(state))
        self.loadSettings()
        self.exec()

    def enableMaxFilesPerFolder(self, state):
        self.ui.txtMaxFilesPerFolder.setEnabled(state)

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
        pattern = self.getPatternFromDialog()
        if pattern:
            display_item = self.getDisplayItemFromOutputPattern(pattern)
            self.ui.cmbOutputPathStructure.insertItem(0, *display_item)
            self.ui.cmbOutputPathStructure.setCurrentIndex(0)

    def editPattern(self):
        folder_structure, file_structure = self.getOutputPathStructure()
        pattern = self.getPatternFromDialog(folder_structure, file_structure)
        if pattern:
            index = self.ui.cmbOutputPathStructure.currentIndex()
            # self.ui.cmbOutputPathStructure.setItemText(index, pattern)
            display_item = self.getDisplayItemFromOutputPattern(pattern)
            self.ui.cmbOutputPathStructure.setItemText(index, display_item[0])
            self.ui.cmbOutputPathStructure.setItemData(index, display_item[1])

    def getPatternFromDialog(self, folder_structure=None,
                                   file_structure=None):
        dialog = PatternCreatorDialog(parent=self,
                                      folder_structure=folder_structure,
                                      file_structure=file_structure)
        if dialog.result!=QDialog.Accepted:
            return
        pattern = dialog.getJoinedPattern()
        if pattern:
            for i in range(self.ui.cmbOutputPathStructure.count()):
                old_pattern = self.ui.cmbOutputPathStructure.itemText(i)
                if pattern == old_pattern:
                    self.ui.cmbOutputPathStructure.setCurrentIndex(i)
                    return None
        return pattern

    def removePattern(self):
        self.ui.cmbOutputPathStructure.removeItem(self.ui.cmbOutputPathStructure.currentIndex())

    def sortFiles(self):
        output_folder_structure, output_filename_structure = self.getOutputPathStructure()
        kwargs = {
            'input_locations':self.getInputLocations(),
            'traverse_subdirectories':self.ui.chkTraverseSubdirectories.isChecked(),
            'output_location':self.ui.txtOutputPath.text(),
            'formats_preference':self.getFormatsPreference(),
            'languages':self.getLanguages(),
            'output_folder_structure':output_folder_structure,
            'output_filename_structure':output_filename_structure,
            'max_files_per_folder':self.getMaxFilesPerFolder(),
            'ignore_alternate':not self.ui.chkIncludeAlternate.isChecked(),
            'ignore_alternate_formats':not self.ui.chkIncludeAlternateFileFormats.isChecked(),
            'ignore_rereleases':not self.ui.chkIncludeRereleases.isChecked(),
            'ignore_hacks':not self.ui.chkIncludeHacked.isChecked(),
            'ignore_xrated':not self.ui.chkIncludeXRated.isChecked(),
            'use_camel_case':self.ui.chkCamelCase.isChecked(),
            'short_filenames':self.ui.chkShortFilenames.isChecked(),
            'place_pok_files_in_pokes_subfolders':self.ui.chkPlacePokFilesIntoPOKESSubfolders.isChecked(),
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
        if s.error:
            self.bar.close()
            QMessageBox.information(self, MESSAGE_BOX_TITLE, self.tr(s.error))
            return
        self.bar.canceled.connect(s.cancel)
        self.bar.raise_()
        self.bar.activateWindow()
        s.sortFiles()
        self.bar.hide()
        if s.should_cancel:
            QMessageBox.information(self, MESSAGE_BOX_TITLE, self.tr('Operation was canceled.'))
        elif s.too_long_path:
            QMessageBox.information(self, MESSAGE_BOX_TITLE,
                                    self.tr('Path %s is too long. Please try another output location.' % s.too_long_path))
        else:
            message = self.tr('Sorting successfully finished.')
            if s.fails:
                message += self.tr('\nFailed files: {}. Please see failed_files.log')\
                    .format(len(s.fails))
                with open('failed_files.log', 'w+', encoding='utf-8') as f:
                    f.write('\n'.join(s.fails))
            QMessageBox.information(self, MESSAGE_BOX_TITLE, message)
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

    def getLanguages(self):
        languages = self.ui.txtLanguages.text()
        languages = languages.replace(';', ',').lower()
        languages = [x.strip()[:2] for x in languages.split(',') if x]
        return languages

    def getOutputPathStructure(self):
        index = self.ui.cmbOutputPathStructure.currentIndex()
        item = self.ui.cmbOutputPathStructure.itemData(index)
        folder_structure = os.path.dirname(item)
        filename_structure = os.path.basename(item)
        return folder_structure, filename_structure

    def getMaxFilesPerFolder(self):
        if not self.ui.chkMaxFilesPerFolder.isChecked():
            return None
        return self.ui.txtMaxFilesPerFolder.value()

    def updateProgressBar(self, current_value=0, max_value=None, label=None):
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
                self.loadOutputPathStructures(settings)
                self.ui.lstInputPaths.addItems(settings.get('input_locations', []))
                self.ui.chkTraverseSubdirectories.setChecked(settings.get('traverse_subridrectories', True))
                self.ui.txtOutputPath.setText(settings.get('output_location', ''))
                self.ui.txtFormatPreference.setText(','.join(settings.get('formats_preference',
                  self.getDefaultFormatPreference())))
                self.ui.txtFormatPreference.setText(','.join(settings.get('languages',
                  self.getDefaultLanguages())))
                self.ui.chkCamelCase.setChecked(settings.get('use_camel_case', False))
                self.ui.chkShortFilenames.setChecked(settings.get('short_filenames', False))
                self.ui.chkIncludeAlternate.setChecked(not settings.get('ignore_alternate', True))
                self.ui.chkIncludeAlternateFileFormats.setChecked(not settings.get('ignore_alternate_formats', False))
                self.ui.chkIncludeRereleases.setChecked(not settings.get('ignore_rereleases', False))
                self.ui.chkIncludeHacked.setChecked(not settings.get('ignore_hacks', False))
                self.ui.chkIncludeXRated.setChecked(not settings.get('ignore_xrated', False))
                self.ui.chkPlacePokFilesIntoPOKESSubfolders.setChecked(settings.get('place_pok_files_in_pokes_subfolders', True))
                if settings.get('max_files_per_folder') and \
                   type(settings['max_files_per_folder'])==int:
                    self.ui.chkMaxFilesPerFolder.toggle()
                    self.ui.txtMaxFilesPerFolder.setValue(settings['max_files_per_folder'])
        except:
            print(traceback.format_exc())
            # patterns = PREDEFINED_OUTPUT_FOLDER_STRUCTURES
            # if os.name == 'nt':
                # patterns = [pattern.replace('/', '\\') for pattern in patterns]
            display_items = [self.getDisplayItemFromOutputPattern(pattern) for pattern in PREDEFINED_OUTPUT_PATH_STRUCTURES]
            for item in display_items:
                self.ui.cmbOutputPathStructure.addItem(*item)
            # self.ui.cmbOutputPathStructure.addItems(display_items)
            self.ui.cmbOutputPathStructure.setCurrentIndex(0)
            self.ui.txtOutputPath.setText(os.getcwd())
            self.ui.txtFormatPreference.setText(self.getDefaultFormatPreference())

    def loadOutputPathStructures(self, settings):
        patterns = settings.get('patterns', PREDEFINED_OUTPUT_PATH_STRUCTURES)
        patterns = [pattern.replace('{Name}', '{GameName}') for pattern in patterns]
        display_items = [self.getDisplayItemFromOutputPattern(pattern) for pattern in
                         PREDEFINED_OUTPUT_PATH_STRUCTURES]
        # if os.name == 'nt':
        #     patterns = [pattern.replace('/', '\\') for pattern in patterns]
        for i, display_item in enumerate(display_items):
            self.ui.cmbOutputPathStructure.addItem(*display_item)
            if display_item[1] == settings.get('output_folder_structure'):
                self.ui.cmbOutputPathStructure.setCurrentIndex(i)

    def getDisplayItemFromOutputPattern(self, pattern):
        pattern = pattern.replace('/', os.sep)
        dirpath = os.path.dirname(pattern)
        filename = os.path.basename(pattern)
        display_text = 'Dir: {} File: {}'.format(dirpath, filename)
        return (display_text, pattern)

    def getDefaultFormatPreference(self):
        return ','.join(GAME_EXTENSIONS)

    def getDefaultLanguages(self):
        return ','.join([x[0] for x in INCLUDED_LANGUAGES_LIST])

    def saveSettings(self, kwargs):
        kwargs['patterns'] = self.getOutputFolderStructurePatterns()
        with open('settings.json', 'w+', encoding='utf-8') as f:
            json.dump(kwargs, f, indent=4)

    def getOutputFolderStructurePatterns(self):
        return [self.ui.cmbOutputPathStructure.itemData(i) \
         for i in range(self.ui.cmbOutputPathStructure.count())]

if __name__=='__main__':
    sys.excepthook = PyQtExceptHook
    app = QApplication(sys.argv)
    pokemaster = MainDialog()
