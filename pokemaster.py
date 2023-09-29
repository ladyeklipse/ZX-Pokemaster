import sys

import os

if hasattr(sys, 'frozen'):
    os.chdir(os.path.dirname(sys.executable))
import settings
from settings import *
import itertools
import stat
import shutil
import zipfile
import zlib
import hashlib
import json
import traceback
from functions.game_name_functions import *
from functions.is_pathname_valid import *
from functions.paths import getDefaultSettingsPath
from classes.database import *
from classes.sorter import *
import webbrowser
import subprocess

sys.path.append("ui")
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from ui.SorterLauncher import *
from pattern_creator import PatternCreatorDialog

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
        self.setWindowTitle(self.windowTitle()+' v'+ZX_POKEMASTER_VERSION)
        self.setWindowFlags(Qt.WindowCloseButtonHint | Qt.WindowMinimizeButtonHint)
        self.ui.tabWidget.setCurrentIndex(0)
        self.ui.btnAddPath.clicked.connect(self.addInputPath)
        self.ui.btnRemovePaths.clicked.connect(self.removeSelectedInputPaths)
        self.ui.btnBrowseOutputPath.clicked.connect(self.browseOutputPath)
        self.ui.btnAddPattern.clicked.connect(self.addPattern)
        self.ui.btnEditPattern.clicked.connect(self.editPattern)
        self.ui.btnRemovePattern.clicked.connect(self.removePattern)
        self.ui.btnSortFiles.clicked.connect(self.sortFiles)
        self.ui.btnSaveSettings.clicked.connect(self.saveSettingsClicked)
        self.ui.btnLoadSettings.clicked.connect(self.loadSettingsClicked)
        self.ui.chkMaxFilesPerFolder.toggled['bool'].connect(lambda state:
             self.enableMaxFilesPerFolder(state))
        self.loadSettings()
        self.ui.btnReadme.clicked.connect(self.openReadme)
        self.ui.btnFacebook.clicked.connect(self.openFacebook)
        self.ui.btnSourceForge.clicked.connect(self.openSourceForge)
        self.exec()

    def openReadme(self):
        if sys.platform=='win32':
            os.startfile('README.txt')
        else:
            opener = "open" if sys.platform == "darwin" else "xdg-open"
            subprocess.call([opener, 'README.txt'])

    def openFacebook(self):
        webbrowser.open('https://www.facebook.com/groups/zxpokemaster/')

    def openSourceForge(self):
        webbrowser.open('https://sourceforge.net/projects/zx-pokemaster/?source=updater')

    def enableMaxFilesPerFolder(self, state):
        self.ui.txtMaxFilesPerFolder.setEnabled(state)
        self.ui.txtBundleKeyLength.setEnabled(state)

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
        kwargs = self.readSettings()
        if not is_pathname_valid(kwargs['output_location']):
            QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr('Invalid output path'))
            return
        for format in kwargs['include_only']:
            if format not in GAME_EXTENSIONS:
                QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr('Format %s is not recognized') % format)
                return
        self.saveSettings(kwargs)
        if not kwargs['input_locations']:
            QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr('Please add one or more input path(s).'))
            return
        if kwargs['delete_source_files']:
            reply = QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr("""Warning!
All files in selected source folders will be deleted after sorting!
Continue only if you have a backup or uncheck "Delete source files after sorting" on "File filtering" tab.
Do you wish to continue?"""), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
                return
        if kwargs['include_supplementary_files']:
            reply = QMessageBox.warning(self, MESSAGE_BOX_TITLE, self.tr("""Warning!
You have checked the option "Include supplementary files". It it advised to use it only if you know what you are doing.
Otherwise you may end up waiting for HOURS instead of MINUTES untill all your files are renamed and sorted.
Do you wish to continue?"""), QMessageBox.Yes | QMessageBox.No)
            if reply == QMessageBox.No:
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
        self.bar.raise_()
        self.bar.activateWindow()
        s.sortFiles()
        self.bar.hide()
        if s.should_cancel:
            QMessageBox.information(self, MESSAGE_BOX_TITLE, self.tr('Operation was canceled.'))
        else:
            message = self.tr('Sorting successfully finished.')
            message += self.tr('\nFiles sorted: {}'.format(s.files_sorted))
            if s.errors:
                message += self.tr('\nSome errors occured during sorting. Please see {}')\
                    .format(s.log_path)
            QMessageBox.information(self, MESSAGE_BOX_TITLE, message)
        self.bar.close()

    def readSettings(self):
        output_folder_structure, output_filename_structure = self.getOutputPathStructure()
        kwargs = {
            'input_locations':self.getInputLocations(),
            'traverse_subdirectories':self.ui.chkTraverseSubdirectories.isChecked(),
            'output_location':self.ui.txtOutputPath.text(),
            # 'formats_preference':self.getFormatsPreference(),
            'include_only':self.getIncludeOnlyList(),
            'exclude':self.getExcludeList(),
            # 'format_filter_on':self.ui.chkFormatsPreference.isChecked(),
            'include_filter_on':self.ui.chkIncludeExtensions.isChecked(),
            'exclude_filter_on':self.ui.chkExcludeExtensions.isChecked(),
            'languages':self.getLanguages(),
            'output_folder_structure':output_folder_structure,
            'output_filename_structure':output_filename_structure,
            'max_files_per_folder':self.getMaxFilesPerFolder(),
            'bundle_key_length':self.ui.txtBundleKeyLength.value(),
            'include_alternate':self.ui.chkIncludeAlternate.isChecked(),
            'include_alternate_formats':self.ui.chkIncludeAlternateFileFormats.isChecked(),
            'include_rereleases':self.ui.chkIncludeRereleases.isChecked(),
            'include_hacks':self.ui.chkIncludeHacked.isChecked(),
            'include_xrated':self.ui.chkIncludeXRated.isChecked(),
            'include_supplementary_files':self.ui.chkIncludeSupplementaryFiles.isChecked(),
            'include_unknown_files':self.ui.chkIncludeUnknownFiles.isChecked(),
            'separate_unknown_files':self.ui.chkSeparateUnknownFiles.isChecked(),
            'retain_relative_structure':self.ui.chkRetainFoldersForUnknownFiles.isChecked(),
            'max_archive_size':self.ui.txtMaxArchiveSize.value(),
            'use_camel_case':self.ui.chkCamelCase.isChecked(),
            'short_filenames':self.ui.chkShortFilenames.isChecked(),
            'delete_source_files':self.ui.chkDeleteSourceFiles.isChecked(),
            'place_pok_files_in_pokes_subfolders':self.ui.chkPlacePokFilesIntoPOKESSubfolders.isChecked(),
        }
        return kwargs

    def getInputLocations(self):
        input_locations = []
        for i in range(self.ui.lstInputPaths.count()):
            input_locations.append(self.ui.lstInputPaths.item(i).text())
        return input_locations

    # def getFormatsPreference(self):
    #     formats = self.ui.txtFormatPreference.text()
    #     formats = formats.replace(';', ',').lower()
    #     formats = [x.strip() for x in formats.split(',') if x]
    #     return formats

    def getIncludeOnlyList(self):
        include_only = self.ui.txtIncludeExtensions.text()
        include_only = include_only.replace(';', ',').lower()
        include_only = [x.strip() for x in include_only.split(',') if x]
        return include_only

    def getExcludeList(self):
        exclude = self.ui.txtExcludeExtensions.text()
        exclude = exclude.replace(';', ',').lower()
        exclude = [x.strip() for x in exclude.split(',') if x]
        return exclude

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
        if current_value==max_value:
            current_value -= 1
        self.bar.setValue(current_value)
        if max_value:
            self.bar.setMaximum(max_value)
        if label:
            self.bar.setLabelText(self.tr(label))
        QCoreApplication.instance().processEvents()

    def saveSettingsClicked(self):
        path, type = QFileDialog.getSaveFileName(self,
                                           self.tr('Save settings to...'),
                                           None,
                                           self.tr('Settings files (*.json)'))
        if not path:
            return
        print(path)
        path = path.replace('/', os.sep).replace('\\', os.sep)
        kwargs = self.readSettings()
        self.saveSettings(kwargs, path)

    def loadSettingsClicked(self):
        path, type = QFileDialog.getOpenFileName(self,
                                           self.tr('Load settings from...'),
                                           None,
                                           self.tr('Settings files (*.json)'))
        if not path:
            return
        path = path.replace('/', os.sep).replace('\\', os.sep)
        self.loadSettings(path)

    def saveSettings(self, kwargs, path=''):
        if not path:
            path = getDefaultSettingsPath()
        kwargs['patterns'] = self.getOutputFolderStructurePatterns()
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w+', encoding='utf-8') as f:
            json.dump(kwargs, f, indent=4)

    def loadSettings(self, path=''):
        if not path:
            path = getDefaultSettingsPath()
        if not os.path.exists(path):
            path = 'default_settings/settings.json'
        try:
            with open(path, 'r', encoding='utf-8') as f:
                settings = json.load(f)
                self.loadOutputPathStructures(settings)
                self.ui.lstInputPaths.clear()
                self.ui.lstInputPaths.addItems(settings.get('input_locations', []))
                self.ui.chkTraverseSubdirectories.setChecked(settings.get('traverse_subridrectories', True))
                self.ui.txtOutputPath.setText(settings.get('output_location', ''))
                # self.ui.txtFormatPreference.setText(','.join(settings.get('formats_preference',
                #   self.getDefaultFormatPreference())))
                self.ui.txtIncludeExtensions.setText(','.join(settings.get('include_only', '')))
                self.ui.txtExcludeExtensions.setText(','.join(settings.get('exclude', '')))
                # self.ui.chkFormatsPreference.setChecked(settings.get('format_filter_on', False))
                self.ui.chkIncludeExtensions.setChecked(settings.get('include_filter_on', False))
                self.ui.chkExcludeExtensions.setChecked(settings.get('exclude_filter_on', False))
                self.ui.txtLanguages.setText(','.join(settings.get('languages',
                  self.getDefaultLanguages())))
                self.ui.chkCamelCase.setChecked(settings.get('use_camel_case', False))
                self.ui.chkShortFilenames.setChecked(settings.get('short_filenames', False))
                self.ui.chkIncludeAlternate.setChecked(settings.get('include_alternate', False))
                self.ui.chkIncludeAlternateFileFormats.setChecked(settings.get('include_alternate_formats', True))
                self.ui.chkIncludeRereleases.setChecked(settings.get('include_rereleases', True))
                self.ui.chkIncludeHacked.setChecked(settings.get('include_hacks', True))
                self.ui.chkIncludeXRated.setChecked(settings.get('include_xrated', True))
                self.ui.chkIncludeUnknownFiles.setChecked(settings.get('include_unknown_files', True))
                self.ui.chkSeparateUnknownFiles.setChecked(settings.get('separate_unknown_files', True))
                self.ui.chkRetainFoldersForUnknownFiles.setChecked(settings.get('retain_relative_structure', False))
                self.ui.chkIncludeSupplementaryFiles.setChecked(settings.get('include_supplementary_files', False))
                self.ui.chkDeleteSourceFiles.setChecked(settings.get('delete_source_files', False))
                self.ui.chkPlacePokFilesIntoPOKESSubfolders.setChecked(settings.get('place_pok_files_in_pokes_subfolders', True))
                self.ui.txtMaxArchiveSize.setValue(settings.get('max_archive_size', 1))
                if settings.get('max_files_per_folder') and \
                   type(settings['max_files_per_folder'])==int:
                    self.ui.chkMaxFilesPerFolder.toggle()
                    self.ui.txtMaxFilesPerFolder.setValue(settings['max_files_per_folder'])
                self.ui.txtBundleKeyLength.setValue(settings['bundle_key_length'])
        except:
            print(traceback.format_exc())
            display_items = [self.getDisplayItemFromOutputPattern(pattern) for pattern in PREDEFINED_OUTPUT_PATH_STRUCTURES]
            for item in display_items:
                self.ui.cmbOutputPathStructure.addItem(*item)
            self.ui.cmbOutputPathStructure.setCurrentIndex(0)
            self.ui.txtOutputPath.setText(os.getcwd())
            # self.ui.txtFormatPreference.setText(self.getDefaultFormatPreference())

    def loadOutputPathStructures(self, settings):
        self.ui.cmbOutputPathStructure.clear()
        patterns = settings.get('patterns', PREDEFINED_OUTPUT_PATH_STRUCTURES)
        patterns = [pattern.replace('{Name}', '{GameName}') for pattern in patterns]
        display_items = [self.getDisplayItemFromOutputPattern(pattern) for pattern in
                         patterns]
        selected_output_path_structure = settings.get('output_folder_structure')+'\\'+settings.get('output_filename_structure')
        for i, display_item in enumerate(display_items):
            self.ui.cmbOutputPathStructure.addItem(*display_item)
            if display_item[1] == selected_output_path_structure:
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

    def getOutputFolderStructurePatterns(self):
        return [self.ui.cmbOutputPathStructure.itemData(i) \
         for i in range(self.ui.cmbOutputPathStructure.count())]

    def closeEvent(self, event):
        kwargs = self.readSettings()
        self.saveSettings(kwargs)
        QDialog.closeEvent(self, event)

if __name__=='__main__':
    sys.excepthook = PyQtExceptHook
    app = QApplication(sys.argv)
    pokemaster = MainDialog()
