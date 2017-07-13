# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OutputFolderStructureEditor.ui'
#
# Created: Thu Jul 13 19:15:38 2017
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
        Dialog.resize(328, 313)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(20, 270, 291, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.txtOutputPath = QtGui.QLineEdit(Dialog)
        self.txtOutputPath.setGeometry(QtCore.QRect(10, 40, 301, 22))
        self.txtOutputPath.setObjectName(_fromUtf8("txtOutputPath"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 70, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lblExample = QtGui.QLabel(Dialog)
        self.lblExample.setGeometry(QtCore.QRect(20, 100, 291, 41))
        self.lblExample.setText(_fromUtf8(""))
        self.lblExample.setWordWrap(True)
        self.lblExample.setObjectName(_fromUtf8("lblExample"))
        self.btnGenre = QtGui.QPushButton(Dialog)
        self.btnGenre.setGeometry(QtCore.QRect(10, 170, 93, 28))
        self.btnGenre.setObjectName(_fromUtf8("btnGenre"))
        self.btnMachineType = QtGui.QPushButton(Dialog)
        self.btnMachineType.setGeometry(QtCore.QRect(110, 170, 93, 28))
        self.btnMachineType.setObjectName(_fromUtf8("btnMachineType"))
        self.btnNumberOfPlayers = QtGui.QPushButton(Dialog)
        self.btnNumberOfPlayers.setGeometry(QtCore.QRect(110, 230, 131, 28))
        self.btnNumberOfPlayers.setObjectName(_fromUtf8("btnNumberOfPlayers"))
        self.btnPublisher = QtGui.QPushButton(Dialog)
        self.btnPublisher.setGeometry(QtCore.QRect(10, 200, 93, 28))
        self.btnPublisher.setObjectName(_fromUtf8("btnPublisher"))
        self.btnYear = QtGui.QPushButton(Dialog)
        self.btnYear.setGeometry(QtCore.QRect(220, 170, 93, 28))
        self.btnYear.setObjectName(_fromUtf8("btnYear"))
        self.btnLetter = QtGui.QPushButton(Dialog)
        self.btnLetter.setGeometry(QtCore.QRect(10, 230, 93, 28))
        self.btnLetter.setObjectName(_fromUtf8("btnLetter"))
        self.btnGameName = QtGui.QPushButton(Dialog)
        self.btnGameName.setGeometry(QtCore.QRect(110, 200, 93, 28))
        self.btnGameName.setObjectName(_fromUtf8("btnGameName"))
        self.btnLanguage = QtGui.QPushButton(Dialog)
        self.btnLanguage.setGeometry(QtCore.QRect(220, 200, 93, 28))
        self.btnLanguage.setObjectName(_fromUtf8("btnLanguage"))
        self.btnSlash = QtGui.QPushButton(Dialog)
        self.btnSlash.setGeometry(QtCore.QRect(250, 230, 61, 28))
        self.btnSlash.setObjectName(_fromUtf8("btnSlash"))

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
        self.btnNumberOfPlayers.setText(_translate("Dialog", "{NumberOfPlayers}", None))
        self.btnPublisher.setText(_translate("Dialog", "{Publisher}", None))
        self.btnYear.setText(_translate("Dialog", "{Year}", None))
        self.btnLetter.setText(_translate("Dialog", "{Letter}", None))
        self.btnGameName.setText(_translate("Dialog", "{GameName}", None))
        self.btnLanguage.setText(_translate("Dialog", "{Language}", None))
        self.btnSlash.setText(_translate("Dialog", "\\", None))

