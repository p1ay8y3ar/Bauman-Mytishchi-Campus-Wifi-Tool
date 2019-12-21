# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'bmstu_login.ui'
#
# Created by: PyQt5 UI code generator 5.13.1
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(310, 402)
        Form.setStyleSheet("*{\n"
"font-family:century gothic;\n"
"font-size:25px;\n"
"}\n"
"\n"
"\n"
"QFrame{\n"
"background:rgba(33, 33, 33, 80%);;\n"
"border-radius:15px;\n"
"}\n"
"\n"
"QPushButton#btn_login{\n"
"background:red;\n"
"border-radius:15px;\n"
"}\n"
"\n"
"QPushButton:hover#btn_login{\n"
"color:#333;\n"
"border-radius:15px;\n"
"background:#49ebff;\n"
"}\n"
"\n"
"QToolButton{\n"
"color:white;\n"
"background:red;\n"
"border-radius:40px;\n"
"}\n"
"\n"
"QLabel{\n"
"background:transparent;\n"
"font-size:20px;\n"
"color:white;\n"
"}\n"
"QLabel#info_label{\n"
"background:transparent;\n"
"font-size:15px;\n"
"color:orange;\n"
"}\n"
"QLineEdit\n"
"{\n"
"font-size:18px;\n"
"background:transparent;\n"
"border:none;\n"
"color:white;\n"
"border-bottom:1px solid #717072;\n"
"\n"
"}\n"
"\n"
"QCheckBox{\n"
"font-size:12px;\n"
"background:transparent;\n"
"border:none;\n"
"color:red;\n"
"}\n"
"")
        self.frame = QtWidgets.QFrame(Form)
        self.frame.setGeometry(QtCore.QRect(30, 70, 251, 281))
        self.frame.setFrameShape(QtWidgets.QFrame.StyledPanel)
        self.frame.setFrameShadow(QtWidgets.QFrame.Raised)
        self.frame.setObjectName("frame")
        self.label = QtWidgets.QLabel(self.frame)
        self.label.setGeometry(QtCore.QRect(20, 30, 221, 41))
        self.label.setObjectName("label")
        self.btn_login = QtWidgets.QPushButton(self.frame)
        self.btn_login.setGeometry(QtCore.QRect(20, 220, 191, 31))
        self.btn_login.setObjectName("btn_login")
        self.lineEdit_name = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_name.setGeometry(QtCore.QRect(20, 100, 191, 21))
        self.lineEdit_name.setAcceptDrops(False)
        self.lineEdit_name.setInputMask("")
        self.lineEdit_name.setText("")
        self.lineEdit_name.setObjectName("lineEdit_name")
        self.lineEdit_pwd = QtWidgets.QLineEdit(self.frame)
        self.lineEdit_pwd.setGeometry(QtCore.QRect(20, 150, 191, 21))
        self.lineEdit_pwd.setAcceptDrops(False)
        self.lineEdit_pwd.setText("")
        self.lineEdit_pwd.setEchoMode(QtWidgets.QLineEdit.Password)
        self.lineEdit_pwd.setObjectName("lineEdit_pwd")
        self.remberme = QtWidgets.QCheckBox(self.frame)
        self.remberme.setGeometry(QtCore.QRect(20, 190, 121, 21))
        self.remberme.setObjectName("remberme")
        self.info_label = QtWidgets.QLabel(self.frame)
        self.info_label.setEnabled(True)
        self.info_label.setGeometry(QtCore.QRect(20, 100, 201, 71))
        self.info_label.setAlignment(QtCore.Qt.AlignJustify|QtCore.Qt.AlignVCenter)
        self.info_label.setObjectName("info_label")
        self.toolButton = QtWidgets.QToolButton(Form)
        self.toolButton.setGeometry(QtCore.QRect(110, 20, 81, 81))
        self.toolButton.setText("")
        self.toolButton.setObjectName("toolButton")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.label.setText(_translate("Form", "М Г Т У Network Tool"))
        self.btn_login.setText(_translate("Form", "Login"))
        self.lineEdit_name.setPlaceholderText(_translate("Form", "username"))
        self.lineEdit_pwd.setPlaceholderText(_translate("Form", "password"))
        self.remberme.setText(_translate("Form", "rember me"))
        self.info_label.setText(_translate("Form", "TextLabel"))
