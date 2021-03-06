# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'main_window.ui'
#
# Created by: PyQt5 UI code generator 5.14.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(992, 563)
        icon = QtGui.QIcon()
        icon.addPixmap(QtGui.QPixmap("paw-png.ico"), QtGui.QIcon.Normal, QtGui.QIcon.Off)
        MainWindow.setWindowIcon(icon)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.plainTextEditOriginal = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEditOriginal.setGeometry(QtCore.QRect(20, 140, 421, 321))
        self.plainTextEditOriginal.setObjectName("plainTextEditOriginal")
        self.plainTextEditResult = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.plainTextEditResult.setGeometry(QtCore.QRect(540, 140, 441, 321))
        self.plainTextEditResult.setObjectName("plainTextEditResult")
        self.checkBoxCreateGroup = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxCreateGroup.setGeometry(QtCore.QRect(650, 50, 211, 17))
        self.checkBoxCreateGroup.setObjectName("checkBoxCreateGroup")
        self.frame = QtWidgets.QFrame(self.centralwidget)
        self.frame.setGeometry(QtCore.QRect(190, 30, 111, 61))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.radioButtonNorth = QtWidgets.QRadioButton(self.frame)
        self.radioButtonNorth.setGeometry(QtCore.QRect(20, 20, 82, 17))
        self.radioButtonNorth.setObjectName("radioButtonNorth")
        self.radioButtonSouth = QtWidgets.QRadioButton(self.frame)
        self.radioButtonSouth.setGeometry(QtCore.QRect(20, 40, 82, 17))
        self.radioButtonSouth.setObjectName("radioButtonSouth")
        self.checkBoxIsNBF = QtWidgets.QCheckBox(self.frame)
        self.checkBoxIsNBF.setGeometry(QtCore.QRect(0, 0, 70, 17))
        self.checkBoxIsNBF.setObjectName("checkBoxIsNBF")
        self.frame_2 = QtWidgets.QFrame(self.centralwidget)
        self.frame_2.setGeometry(QtCore.QRect(50, 20, 120, 71))
        self.frame_2.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame_2.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame_2.setObjectName("frame_2")
        self.radioButtonCisco = QtWidgets.QRadioButton(self.frame_2)
        self.radioButtonCisco.setGeometry(QtCore.QRect(20, 30, 82, 17))
        self.radioButtonCisco.setObjectName("radioButtonCisco")
        self.radioButtonFortigate = QtWidgets.QRadioButton(self.frame_2)
        self.radioButtonFortigate.setGeometry(QtCore.QRect(20, 50, 82, 17))
        self.radioButtonFortigate.setObjectName("radioButtonFortigate")
        self.label_4 = QtWidgets.QLabel(self.frame_2)
        self.label_4.setGeometry(QtCore.QRect(30, 10, 47, 13))
        self.label_4.setObjectName("label_4")
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setGeometry(QtCore.QRect(440, 50, 121, 16))
        self.label_2.setObjectName("label_2")
        self.checkBoxCustomNames = QtWidgets.QCheckBox(self.centralwidget)
        self.checkBoxCustomNames.setGeometry(QtCore.QRect(650, 20, 201, 17))
        self.checkBoxCustomNames.setObjectName("checkBoxCustomNames")
        self.pushButtonConvert = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonConvert.setGeometry(QtCore.QRect(450, 280, 75, 23))
        self.pushButtonConvert.setObjectName("pushButtonConvert")
        self.labelResults = QtWidgets.QLabel(self.centralwidget)
        self.labelResults.setGeometry(QtCore.QRect(526, 120, 431, 20))
        self.labelResults.setAlignment(QtCore.Qt.AlignCenter)
        self.labelResults.setObjectName("labelResults")
        self.labelResultsErrors = QtWidgets.QLabel(self.centralwidget)
        self.labelResultsErrors.setGeometry(QtCore.QRect(460, 470, 511, 81))
        self.labelResultsErrors.setAlignment(QtCore.Qt.AlignCenter)
        self.labelResultsErrors.setObjectName("labelResultsErrors")
        self.pushButtonExample = QtWidgets.QPushButton(self.centralwidget)
        self.pushButtonExample.setGeometry(QtCore.QRect(450, 320, 75, 23))
        self.pushButtonExample.setObjectName("pushButtonExample")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setGeometry(QtCore.QRect(106, 120, 141, 20))
        self.label.setObjectName("label")
        self.lineEditComment = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditComment.setGeometry(QtCore.QRect(390, 80, 211, 20))
        self.lineEditComment.setObjectName("lineEditComment")
        self.lineEditGroupName = QtWidgets.QLineEdit(self.centralwidget)
        self.lineEditGroupName.setGeometry(QtCore.QRect(650, 90, 231, 20))
        self.lineEditGroupName.setObjectName("lineEditGroupName")
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setGeometry(QtCore.QRect(710, 70, 91, 16))
        self.label_3.setObjectName("label_3")
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.checkBoxCreateGroup.setText(_translate("MainWindow", "Create group with the objects created"))
        self.radioButtonNorth.setText(_translate("MainWindow", "North"))
        self.radioButtonSouth.setText(_translate("MainWindow", "South"))
        self.checkBoxIsNBF.setText(_translate("MainWindow", "Is NBF ?"))
        self.radioButtonCisco.setText(_translate("MainWindow", "Cisco"))
        self.radioButtonFortigate.setText(_translate("MainWindow", "Fortigate"))
        self.label_4.setText(_translate("MainWindow", "Vendor"))
        self.label_2.setText(_translate("MainWindow", "Insert your comment:"))
        self.checkBoxCustomNames.setText(_translate("MainWindow", "Use custom names for objects"))
        self.pushButtonConvert.setText(_translate("MainWindow", "Convert"))
        self.labelResults.setText(_translate("MainWindow", "Results"))
        self.labelResultsErrors.setText(_translate("MainWindow", "Errors"))
        self.pushButtonExample.setText(_translate("MainWindow", "Example"))
        self.label.setText(_translate("MainWindow", "Insert IP or list of IP\'s here:"))
        self.label_3.setText(_translate("MainWindow", "Group Name:"))
