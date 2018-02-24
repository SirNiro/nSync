# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'register.ui'
#
# Created: Mon Feb 19 14:56:35 2018
#      by: pyside-uic 0.2.15 running on PySide 1.2.4
#
# WARNING! All changes made in this file will be lost!

from PySide import QtCore, QtGui

class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(400, 300)
        font = QtGui.QFont()
        font.setWeight(75)
        font.setBold(True)
        Form.setFont(font)
        self.register_label = QtGui.QLabel(Form)
        self.register_label.setGeometry(QtCore.QRect(170, 20, 71, 21))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(12)
        self.register_label.setFont(font)
        self.register_label.setObjectName("register_label")
        self.label = QtGui.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(80, 75, 71, 20))
        self.label.setObjectName("label")
        self.label_2 = QtGui.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(100, 120, 46, 13))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtGui.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(80, 155, 61, 20))
        self.label_3.setObjectName("label_3")
        self.register_button = QtGui.QPushButton(Form)
        self.register_button.setGeometry(QtCore.QRect(150, 200, 111, 51))
        self.register_button.setObjectName("register_button")
        self.back_button = QtGui.QPushButton(Form)
        self.back_button.setGeometry(QtCore.QRect(10, 270, 61, 20))
        self.back_button.setObjectName("back_button")
        self.widget = QtGui.QWidget(Form)
        self.widget.setGeometry(QtCore.QRect(150, 60, 161, 131))
        self.widget.setObjectName("widget")
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.verticalLayout.setObjectName("verticalLayout")
        self.lineEdit = QtGui.QLineEdit(self.widget)
        self.lineEdit.setObjectName("lineEdit")
        self.verticalLayout.addWidget(self.lineEdit)
        self.lineEdit_2 = QtGui.QLineEdit(self.widget)
        self.lineEdit_2.setObjectName("lineEdit_2")
        self.verticalLayout.addWidget(self.lineEdit_2)
        self.lineEdit_3 = QtGui.QLineEdit(self.widget)
        self.lineEdit_3.setEchoMode(QtGui.QLineEdit.Password)
        self.lineEdit_3.setObjectName("lineEdit_3")
        self.verticalLayout.addWidget(self.lineEdit_3)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(QtGui.QApplication.translate("Form", "Form", None, QtGui.QApplication.UnicodeUTF8))
        self.register_label.setText(QtGui.QApplication.translate("Form", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.label.setText(QtGui.QApplication.translate("Form", "Username:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_2.setText(QtGui.QApplication.translate("Form", "E-mail:", None, QtGui.QApplication.UnicodeUTF8))
        self.label_3.setText(QtGui.QApplication.translate("Form", "Password:", None, QtGui.QApplication.UnicodeUTF8))
        self.register_button.setText(QtGui.QApplication.translate("Form", "Register", None, QtGui.QApplication.UnicodeUTF8))
        self.back_button.setText(QtGui.QApplication.translate("Form", "Back", None, QtGui.QApplication.UnicodeUTF8))

