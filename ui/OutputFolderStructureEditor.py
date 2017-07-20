# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OutputFolderStructureEditor.ui'
#
# Created: Thu Jul 20 03:55:24 2017
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
        Dialog.resize(417, 449)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(110, 410, 291, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.txtOutputPath = QtGui.QLineEdit(Dialog)
        self.txtOutputPath.setGeometry(QtCore.QRect(10, 40, 391, 22))
        self.txtOutputPath.setObjectName(_fromUtf8("txtOutputPath"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(10, 190, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lblExample = QtGui.QLabel(Dialog)
        self.lblExample.setGeometry(QtCore.QRect(10, 220, 391, 61))
        self.lblExample.setText(_fromUtf8(""))
        self.lblExample.setWordWrap(True)
        self.lblExample.setObjectName(_fromUtf8("lblExample"))
        self.btnGenre = QtGui.QPushButton(Dialog)
        self.btnGenre.setGeometry(QtCore.QRect(10, 290, 93, 28))
        self.btnGenre.setObjectName(_fromUtf8("btnGenre"))
        self.btnMachineType = QtGui.QPushButton(Dialog)
        self.btnMachineType.setGeometry(QtCore.QRect(10, 320, 93, 28))
        self.btnMachineType.setObjectName(_fromUtf8("btnMachineType"))
        self.btnNumberOfPlayers = QtGui.QPushButton(Dialog)
        self.btnNumberOfPlayers.setGeometry(QtCore.QRect(10, 350, 91, 28))
        self.btnNumberOfPlayers.setObjectName(_fromUtf8("btnNumberOfPlayers"))
        self.btnPublisher = QtGui.QPushButton(Dialog)
        self.btnPublisher.setGeometry(QtCore.QRect(210, 290, 93, 28))
        self.btnPublisher.setObjectName(_fromUtf8("btnPublisher"))
        self.btnYear = QtGui.QPushButton(Dialog)
        self.btnYear.setGeometry(QtCore.QRect(110, 290, 93, 28))
        self.btnYear.setObjectName(_fromUtf8("btnYear"))
        self.btnLetter = QtGui.QPushButton(Dialog)
        self.btnLetter.setGeometry(QtCore.QRect(110, 320, 93, 28))
        self.btnLetter.setObjectName(_fromUtf8("btnLetter"))
        self.btnGameName = QtGui.QPushButton(Dialog)
        self.btnGameName.setGeometry(QtCore.QRect(110, 350, 93, 28))
        self.btnGameName.setObjectName(_fromUtf8("btnGameName"))
        self.btnLanguage = QtGui.QPushButton(Dialog)
        self.btnLanguage.setGeometry(QtCore.QRect(210, 320, 93, 28))
        self.btnLanguage.setObjectName(_fromUtf8("btnLanguage"))
        self.btnSlash = QtGui.QPushButton(Dialog)
        self.btnSlash.setGeometry(QtCore.QRect(310, 320, 91, 28))
        self.btnSlash.setObjectName(_fromUtf8("btnSlash"))
        self.btnFormat = QtGui.QPushButton(Dialog)
        self.btnFormat.setGeometry(QtCore.QRect(10, 380, 93, 28))
        self.btnFormat.setObjectName(_fromUtf8("btnFormat"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 191, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.txtOutputFileNamePattern = QtGui.QLineEdit(Dialog)
        self.txtOutputFileNamePattern.setGeometry(QtCore.QRect(10, 100, 391, 22))
        self.txtOutputFileNamePattern.setText(_fromUtf8(""))
        self.txtOutputFileNamePattern.setObjectName(_fromUtf8("txtOutputFileNamePattern"))
        self.chkCamelCase = QtGui.QCheckBox(Dialog)
        self.chkCamelCase.setGeometry(QtCore.QRect(10, 130, 291, 20))
        self.chkCamelCase.setObjectName(_fromUtf8("chkCamelCase"))
        self.chkUseEightChars = QtGui.QCheckBox(Dialog)
        self.chkUseEightChars.setGeometry(QtCore.QRect(10, 160, 291, 20))
        self.chkUseEightChars.setObjectName(_fromUtf8("chkUseEightChars"))
        self.btnModFlags = QtGui.QPushButton(Dialog)
        self.btnModFlags.setGeometry(QtCore.QRect(210, 350, 93, 28))
        self.btnModFlags.setObjectName(_fromUtf8("btnModFlags"))
        self.btnFormat_3 = QtGui.QPushButton(Dialog)
        self.btnFormat_3.setGeometry(QtCore.QRect(310, 290, 93, 28))
        self.btnFormat_3.setObjectName(_fromUtf8("btnFormat_3"))
        self.btnPart = QtGui.QPushButton(Dialog)
        self.btnPart.setGeometry(QtCore.QRect(110, 380, 93, 28))
        self.btnPart.setObjectName(_fromUtf8("btnPart"))
        self.btnSide = QtGui.QPushButton(Dialog)
        self.btnSide.setGeometry(QtCore.QRect(210, 380, 93, 28))
        self.btnSide.setObjectName(_fromUtf8("btnSide"))
        self.btnHyphen = QtGui.QPushButton(Dialog)
        self.btnHyphen.setGeometry(QtCore.QRect(310, 350, 91, 28))
        self.btnHyphen.setObjectName(_fromUtf8("btnHyphen"))
        self.btnUnderscore = QtGui.QPushButton(Dialog)
        self.btnUnderscore.setGeometry(QtCore.QRect(310, 380, 91, 28))
        self.btnUnderscore.setObjectName(_fromUtf8("btnUnderscore"))

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), Dialog.accept)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Edit output folder structure", None))
        self.label.setText(_translate("Dialog", "Output folder structure pattern:", None))
        self.label_2.setText(_translate("Dialog", "Example:", None))
        self.btnGenre.setText(_translate("Dialog", "{Genre}", None))
        self.btnMachineType.setText(_translate("Dialog", "{MachineType}", None))
        self.btnNumberOfPlayers.setText(_translate("Dialog", "{MaxPlayers}", None))
        self.btnPublisher.setText(_translate("Dialog", "{Publisher}", None))
        self.btnYear.setText(_translate("Dialog", "{Year}", None))
        self.btnLetter.setText(_translate("Dialog", "{Letter}", None))
        self.btnGameName.setText(_translate("Dialog", "{GameName}", None))
        self.btnLanguage.setText(_translate("Dialog", "{Language}", None))
        self.btnSlash.setText(_translate("Dialog", "Slash (\\)", None))
        self.btnFormat.setText(_translate("Dialog", "{Format}", None))
        self.label_3.setText(_translate("Dialog", "Output file name pattern:", None))
        self.chkCamelCase.setText(_translate("Dialog", "CamelCaseInsteadOfSpaces", None))
        self.chkUseEightChars.setText(_translate("Dialog", "Use 8.3 naming scheme", None))
        self.btnModFlags.setText(_translate("Dialog", "{ModFlags}", None))
        self.btnFormat_3.setText(_translate("Dialog", "{ZXDB_ID}", None))
        self.btnPart.setText(_translate("Dialog", "{Part}", None))
        self.btnSide.setText(_translate("Dialog", "{Side}", None))
        self.btnHyphen.setText(_translate("Dialog", "Hyphen ( - )", None))
        self.btnUnderscore.setText(_translate("Dialog", "Underscore(_)", None))

