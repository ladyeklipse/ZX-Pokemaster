# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'OutputFolderStructureEditor.ui'
#
# Created: Mon Jul 17 03:00:01 2017
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
        Dialog.resize(316, 480)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(10, 420, 291, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.txtOutputPath = QtGui.QLineEdit(Dialog)
        self.txtOutputPath.setGeometry(QtCore.QRect(10, 40, 291, 22))
        self.txtOutputPath.setObjectName(_fromUtf8("txtOutputPath"))
        self.label = QtGui.QLabel(Dialog)
        self.label.setGeometry(QtCore.QRect(10, 10, 191, 16))
        self.label.setObjectName(_fromUtf8("label"))
        self.label_2 = QtGui.QLabel(Dialog)
        self.label_2.setGeometry(QtCore.QRect(20, 190, 91, 16))
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.lblExample = QtGui.QLabel(Dialog)
        self.lblExample.setGeometry(QtCore.QRect(20, 220, 291, 41))
        self.lblExample.setText(_fromUtf8(""))
        self.lblExample.setWordWrap(True)
        self.lblExample.setObjectName(_fromUtf8("lblExample"))
        self.btnGenre = QtGui.QPushButton(Dialog)
        self.btnGenre.setGeometry(QtCore.QRect(10, 290, 93, 28))
        self.btnGenre.setObjectName(_fromUtf8("btnGenre"))
        self.btnMachineType = QtGui.QPushButton(Dialog)
        self.btnMachineType.setGeometry(QtCore.QRect(110, 290, 93, 28))
        self.btnMachineType.setObjectName(_fromUtf8("btnMachineType"))
        self.btnNumberOfPlayers = QtGui.QPushButton(Dialog)
        self.btnNumberOfPlayers.setGeometry(QtCore.QRect(110, 350, 131, 28))
        self.btnNumberOfPlayers.setObjectName(_fromUtf8("btnNumberOfPlayers"))
        self.btnPublisher = QtGui.QPushButton(Dialog)
        self.btnPublisher.setGeometry(QtCore.QRect(10, 320, 93, 28))
        self.btnPublisher.setObjectName(_fromUtf8("btnPublisher"))
        self.btnYear = QtGui.QPushButton(Dialog)
        self.btnYear.setGeometry(QtCore.QRect(210, 290, 93, 28))
        self.btnYear.setObjectName(_fromUtf8("btnYear"))
        self.btnLetter = QtGui.QPushButton(Dialog)
        self.btnLetter.setGeometry(QtCore.QRect(10, 350, 93, 28))
        self.btnLetter.setObjectName(_fromUtf8("btnLetter"))
        self.btnGameName = QtGui.QPushButton(Dialog)
        self.btnGameName.setGeometry(QtCore.QRect(110, 320, 93, 28))
        self.btnGameName.setObjectName(_fromUtf8("btnGameName"))
        self.btnLanguage = QtGui.QPushButton(Dialog)
        self.btnLanguage.setGeometry(QtCore.QRect(210, 320, 93, 28))
        self.btnLanguage.setObjectName(_fromUtf8("btnLanguage"))
        self.btnSlash = QtGui.QPushButton(Dialog)
        self.btnSlash.setGeometry(QtCore.QRect(250, 350, 51, 28))
        self.btnSlash.setObjectName(_fromUtf8("btnSlash"))
        self.btnFormat = QtGui.QPushButton(Dialog)
        self.btnFormat.setGeometry(QtCore.QRect(10, 380, 93, 28))
        self.btnFormat.setObjectName(_fromUtf8("btnFormat"))
        self.label_3 = QtGui.QLabel(Dialog)
        self.label_3.setGeometry(QtCore.QRect(10, 70, 191, 16))
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.txtOutputFileNamePattern = QtGui.QLineEdit(Dialog)
        self.txtOutputFileNamePattern.setGeometry(QtCore.QRect(10, 100, 291, 22))
        self.txtOutputFileNamePattern.setText(_fromUtf8(""))
        self.txtOutputFileNamePattern.setObjectName(_fromUtf8("txtOutputFileNamePattern"))

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
        self.btnFormat.setText(_translate("Dialog", "{Format}", None))
        self.label_3.setText(_translate("Dialog", "Output folder structure pattern:", None))

