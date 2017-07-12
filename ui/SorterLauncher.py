# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'SorterLauncher.ui'
#
# Created: Wed Jul 12 20:04:03 2017
#      by: PyQt4 UI code generator 4.10.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(470, 527)
        Dialog.setContextMenuPolicy(QtCore.Qt.DefaultContextMenu)
        Dialog.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedKingdom))
        Dialog.setSizeGripEnabled(False)
        self.btnSortFiles = QtGui.QPushButton(Dialog)
        self.btnSortFiles.setGeometry(QtCore.QRect(370, 490, 93, 28))
        self.btnSortFiles.setObjectName(_fromUtf8("btnSortFiles"))
        self.txtOutputPath = QtGui.QLineEdit(Dialog)
        self.txtOutputPath.setGeometry(QtCore.QRect(100, 220, 321, 22))
        self.txtOutputPath.setObjectName(_fromUtf8("txtOutputPath"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(20, 220, 81, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.groupBox = QtGui.QGroupBox(Dialog)
        self.groupBox.setGeometry(QtCore.QRect(20, 10, 441, 201))
        self.groupBox.setObjectName(_fromUtf8("groupBox"))
        self.btnAddPath = QtGui.QPushButton(self.groupBox)
        self.btnAddPath.setGeometry(QtCore.QRect(330, 30, 93, 28))
        self.btnAddPath.setObjectName(_fromUtf8("btnAddPath"))
        self.btnRemovePaths = QtGui.QPushButton(self.groupBox)
        self.btnRemovePaths.setGeometry(QtCore.QRect(330, 70, 93, 28))
        self.btnRemovePaths.setObjectName(_fromUtf8("btnRemovePaths"))
        self.lstInputPaths = QtGui.QListWidget(self.groupBox)
        self.lstInputPaths.setGeometry(QtCore.QRect(10, 20, 311, 171))
        self.lstInputPaths.setObjectName(_fromUtf8("lstInputPaths"))
        self.chkIncludeAlternate = QtGui.QCheckBox(Dialog)
        self.chkIncludeAlternate.setGeometry(QtCore.QRect(20, 390, 451, 20))
        self.chkIncludeAlternate.setObjectName(_fromUtf8("chkIncludeAlternate"))
        self.chkIncludeRereleases = QtGui.QCheckBox(Dialog)
        self.chkIncludeRereleases.setGeometry(QtCore.QRect(20, 410, 451, 20))
        self.chkIncludeRereleases.setChecked(True)
        self.chkIncludeRereleases.setObjectName(_fromUtf8("chkIncludeRereleases"))
        self.chkIncludeAlternateFileFormats = QtGui.QCheckBox(Dialog)
        self.chkIncludeAlternateFileFormats.setGeometry(QtCore.QRect(20, 430, 451, 20))
        self.chkIncludeAlternateFileFormats.setChecked(True)
        self.chkIncludeAlternateFileFormats.setObjectName(_fromUtf8("chkIncludeAlternateFileFormats"))
        self.chkIncludeHacked = QtGui.QCheckBox(Dialog)
        self.chkIncludeHacked.setGeometry(QtCore.QRect(20, 450, 451, 20))
        self.chkIncludeHacked.setChecked(True)
        self.chkIncludeHacked.setObjectName(_fromUtf8("chkIncludeHacked"))
        self.txtFormatPreference = QtGui.QLineEdit(Dialog)
        self.txtFormatPreference.setGeometry(QtCore.QRect(180, 250, 281, 22))
        self.txtFormatPreference.setInputMask(_fromUtf8(""))
        self.txtFormatPreference.setObjectName(_fromUtf8("txtFormatPreference"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 250, 161, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.groupBox_2 = QtGui.QGroupBox(Dialog)
        self.groupBox_2.setGeometry(QtCore.QRect(20, 290, 441, 91))
        self.groupBox_2.setObjectName(_fromUtf8("groupBox_2"))
        self.cmbOutputFolderStructure = QtGui.QComboBox(self.groupBox_2)
        self.cmbOutputFolderStructure.setGeometry(QtCore.QRect(10, 20, 421, 22))
        self.cmbOutputFolderStructure.setEditable(False)
        self.cmbOutputFolderStructure.setProperty("currentText", _fromUtf8(""))
        self.cmbOutputFolderStructure.setObjectName(_fromUtf8("cmbOutputFolderStructure"))
        self.btnAddPattern = QtGui.QPushButton(self.groupBox_2)
        self.btnAddPattern.setGeometry(QtCore.QRect(10, 50, 131, 28))
        self.btnAddPattern.setObjectName(_fromUtf8("btnAddPattern"))
        self.chkPlacePokFilesIntoPOKESSubfolder = QtGui.QCheckBox(Dialog)
        self.chkPlacePokFilesIntoPOKESSubfolder.setGeometry(QtCore.QRect(20, 470, 441, 20))
        self.chkPlacePokFilesIntoPOKESSubfolder.setChecked(True)
        self.chkPlacePokFilesIntoPOKESSubfolder.setObjectName(_fromUtf8("chkPlacePokFilesIntoPOKESSubfolder"))
        self.btnBrowseOutputPath = QtGui.QToolButton(Dialog)
        self.btnBrowseOutputPath.setGeometry(QtCore.QRect(430, 220, 27, 22))
        self.btnBrowseOutputPath.setObjectName(_fromUtf8("btnBrowseOutputPath"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "ZX Pokemaster", None))
        self.btnSortFiles.setText(_translate("Dialog", "Sort files", None))
        self.label.setText(_translate("Dialog", "Output path:", None))
        self.groupBox.setTitle(_translate("Dialog", "Input paths", None))
        self.btnAddPath.setText(_translate("Dialog", "Add path...", None))
        self.btnRemovePaths.setText(_translate("Dialog", "Remove path", None))
        self.chkIncludeAlternate.setText(_translate("Dialog", "Include alternate files (marked [a] in TOSEC)", None))
        self.chkIncludeRereleases.setText(_translate("Dialog", "Include re-releases", None))
        self.chkIncludeAlternateFileFormats.setText(_translate("Dialog", "Include alternate file formats (see formats preference order)", None))
        self.chkIncludeHacked.setText(_translate("Dialog", "Include files marked as cracked, hacked or modded", None))
        self.txtFormatPreference.setPlaceholderText(_translate("Dialog", "tzx,tap,z80,sna,dsk,trd,img,mgt,rom,scl,slt,szx", None))
        self.label_2.setText(_translate("Dialog", "Formats preference order:", None))
        self.groupBox_2.setTitle(_translate("Dialog", "Output folder structure pattern", None))
        self.btnAddPattern.setText(_translate("Dialog", "Custom pattern...", None))
        self.chkPlacePokFilesIntoPOKESSubfolder.setText(_translate("Dialog", "Place .POK files into POKES subfolder", None))
        self.btnBrowseOutputPath.setText(_translate("Dialog", "...", None))

