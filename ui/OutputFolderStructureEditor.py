# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OutputFolderStructureEditor.ui'
#
# Created: Tue Aug  1 01:25:41 2017
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
        Dialog.resize(422, 424)
        self.gridLayout = QtGui.QGridLayout(Dialog)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setObjectName(_fromUtf8("label"))
        self.gridLayout.addWidget(self.label, 0, 0, 1, 2)
        self.btnYear = QtGui.QPushButton(Dialog)
        self.btnYear.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnYear.setObjectName(_fromUtf8("btnYear"))
        self.gridLayout.addWidget(self.btnYear, 6, 1, 1, 1)
        self.btnGameName = QtGui.QPushButton(Dialog)
        self.btnGameName.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnGameName.setObjectName(_fromUtf8("btnGameName"))
        self.gridLayout.addWidget(self.btnGameName, 8, 1, 1, 1)
        self.btnLetter = QtGui.QPushButton(Dialog)
        self.btnLetter.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnLetter.setObjectName(_fromUtf8("btnLetter"))
        self.gridLayout.addWidget(self.btnLetter, 7, 1, 1, 1)
        self.btnZXDB_ID = QtGui.QPushButton(Dialog)
        self.btnZXDB_ID.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnZXDB_ID.setObjectName(_fromUtf8("btnZXDB_ID"))
        self.gridLayout.addWidget(self.btnZXDB_ID, 6, 3, 1, 1)
        self.btnHyphen = QtGui.QPushButton(Dialog)
        self.btnHyphen.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnHyphen.setObjectName(_fromUtf8("btnHyphen"))
        self.gridLayout.addWidget(self.btnHyphen, 8, 3, 1, 1)
        self.txtOutputFileNameStructure = QtGui.QLineEdit(Dialog)
        self.txtOutputFileNameStructure.setText(_fromUtf8(""))
        self.txtOutputFileNameStructure.setObjectName(_fromUtf8("txtOutputFileNameStructure"))
        self.gridLayout.addWidget(self.txtOutputFileNameStructure, 3, 0, 1, 4)
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.gridLayout.addWidget(self.label_3, 2, 0, 1, 2)
        self.btnGenre = QtGui.QPushButton(Dialog)
        self.btnGenre.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnGenre.setObjectName(_fromUtf8("btnGenre"))
        self.gridLayout.addWidget(self.btnGenre, 6, 0, 1, 1)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setFocusPolicy(QtCore.Qt.NoFocus)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.gridLayout.addWidget(self.buttonBox, 12, 1, 1, 3)
        self.btnFormat = QtGui.QPushButton(Dialog)
        self.btnFormat.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnFormat.setObjectName(_fromUtf8("btnFormat"))
        self.gridLayout.addWidget(self.btnFormat, 9, 0, 1, 1)
        self.btnNumberOfPlayers = QtGui.QPushButton(Dialog)
        self.btnNumberOfPlayers.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnNumberOfPlayers.setObjectName(_fromUtf8("btnNumberOfPlayers"))
        self.gridLayout.addWidget(self.btnNumberOfPlayers, 8, 0, 1, 1)
        self.btnUnderscore = QtGui.QPushButton(Dialog)
        self.btnUnderscore.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnUnderscore.setObjectName(_fromUtf8("btnUnderscore"))
        self.gridLayout.addWidget(self.btnUnderscore, 9, 3, 1, 1)
        self.btnSlash = QtGui.QPushButton(Dialog)
        self.btnSlash.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnSlash.setObjectName(_fromUtf8("btnSlash"))
        self.gridLayout.addWidget(self.btnSlash, 7, 3, 1, 1)
        self.btnModFlags = QtGui.QPushButton(Dialog)
        self.btnModFlags.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnModFlags.setObjectName(_fromUtf8("btnModFlags"))
        self.gridLayout.addWidget(self.btnModFlags, 8, 2, 1, 1)
        self.btnLanguage = QtGui.QPushButton(Dialog)
        self.btnLanguage.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnLanguage.setObjectName(_fromUtf8("btnLanguage"))
        self.gridLayout.addWidget(self.btnLanguage, 7, 2, 1, 1)
        self.btnPublisher = QtGui.QPushButton(Dialog)
        self.btnPublisher.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnPublisher.setObjectName(_fromUtf8("btnPublisher"))
        self.gridLayout.addWidget(self.btnPublisher, 6, 2, 1, 1)
        self.btnSide = QtGui.QPushButton(Dialog)
        self.btnSide.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnSide.setObjectName(_fromUtf8("btnSide"))
        self.gridLayout.addWidget(self.btnSide, 9, 2, 1, 1)
        self.btnMachineType = QtGui.QPushButton(Dialog)
        self.btnMachineType.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnMachineType.setObjectName(_fromUtf8("btnMachineType"))
        self.gridLayout.addWidget(self.btnMachineType, 7, 0, 1, 1)
        self.txtOutputFolderStructure = QtGui.QLineEdit(Dialog)
        self.txtOutputFolderStructure.setObjectName(_fromUtf8("txtOutputFolderStructure"))
        self.gridLayout.addWidget(self.txtOutputFolderStructure, 1, 0, 1, 4)
        self.btnPart = QtGui.QPushButton(Dialog)
        self.btnPart.setFocusPolicy(QtCore.Qt.NoFocus)
        self.btnPart.setObjectName(_fromUtf8("btnPart"))
        self.gridLayout.addWidget(self.btnPart, 9, 1, 1, 1)
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.gridLayout.addWidget(self.label_2, 10, 0, 1, 1)
        self.lblExample = QtGui.QLabel(Dialog)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.lblExample.sizePolicy().hasHeightForWidth())
        self.lblExample.setSizePolicy(sizePolicy)
        self.lblExample.setMinimumSize(QtCore.QSize(0, 100))
        self.lblExample.setText(_fromUtf8(""))
        self.lblExample.setAlignment(QtCore.Qt.AlignLeading|QtCore.Qt.AlignLeft|QtCore.Qt.AlignTop)
        self.lblExample.setWordWrap(True)
        self.lblExample.setObjectName(_fromUtf8("lblExample"))
        self.gridLayout.addWidget(self.lblExample, 11, 0, 1, 4)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)
        Dialog.setTabOrder(self.txtOutputFileNameStructure, self.txtOutputFolderStructure)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Edit output folder structure", None))
        self.label.setText(_translate("Dialog", "Output folder structure pattern:", None))
        self.btnYear.setText(_translate("Dialog", "{Year}", None))
        self.btnGameName.setText(_translate("Dialog", "{GameName}", None))
        self.btnLetter.setText(_translate("Dialog", "{Letter}", None))
        self.btnZXDB_ID.setText(_translate("Dialog", "{ZXDB_ID}", None))
        self.btnHyphen.setText(_translate("Dialog", "Hyphen ( - )", None))
        self.label_3.setText(_translate("Dialog", "Output file name structure pattern:", None))
        self.btnGenre.setText(_translate("Dialog", "{Genre}", None))
        self.btnFormat.setText(_translate("Dialog", "{Format}", None))
        self.btnNumberOfPlayers.setText(_translate("Dialog", "{MaxPlayers}", None))
        self.btnUnderscore.setText(_translate("Dialog", "Underscore(_)", None))
        self.btnSlash.setText(_translate("Dialog", "Slash (\\)", None))
        self.btnModFlags.setText(_translate("Dialog", "{ModFlags}", None))
        self.btnLanguage.setText(_translate("Dialog", "{Language}", None))
        self.btnPublisher.setText(_translate("Dialog", "{Publisher}", None))
        self.btnSide.setText(_translate("Dialog", "{Side}", None))
        self.btnMachineType.setText(_translate("Dialog", "{MachineType}", None))
        self.btnPart.setText(_translate("Dialog", "{Part}", None))
        self.label_2.setText(_translate("Dialog", "Examples:", None))
