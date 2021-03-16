# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'signindlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_SigninDlg(QtWidgets.QDialog):
    def __init__(self):
        super(Ui_SigninDlg,self).__init__()
        self.setupUi(self)

    def setupUi(self, SigninDlg):
        SigninDlg.setObjectName("SigninDlg")
        SigninDlg.resize(487, 376)
        self.label = QtWidgets.QLabel(SigninDlg)
        self.label.setGeometry(QtCore.QRect(70, 100, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(SigninDlg)
        self.label_2.setGeometry(QtCore.QRect(70, 150, 72, 15))
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(SigninDlg)
        self.label_3.setGeometry(QtCore.QRect(70, 200, 72, 15))
        self.label_3.setObjectName("label_3")
        self.t_phoneNum = QtWidgets.QLineEdit(SigninDlg)
        self.t_phoneNum.setGeometry(QtCore.QRect(170, 90, 181, 31))
        self.t_phoneNum.setObjectName("t_phoneNum")
        self.t_pwd = QtWidgets.QLineEdit(SigninDlg)
        self.t_pwd.setGeometry(QtCore.QRect(170, 140, 181, 31))
        self.t_pwd.setObjectName("t_pwd")
        self.t_pwdagain = QtWidgets.QLineEdit(SigninDlg)
        self.t_pwdagain.setGeometry(QtCore.QRect(170, 190, 181, 31))
        self.t_pwdagain.setObjectName("t_pwdagain")
        self.btn_signin = QtWidgets.QPushButton(SigninDlg)
        self.btn_signin.setGeometry(QtCore.QRect(170, 250, 181, 31))
        self.btn_signin.setObjectName("btn_signin")
        self.info = QtWidgets.QLabel(SigninDlg)
        self.info.setGeometry(QtCore.QRect(200, 300, 141, 16))
        self.info.setObjectName("info")
        self.info.hide()

        self.retranslateUi(SigninDlg)
        QtCore.QMetaObject.connectSlotsByName(SigninDlg)

    def retranslateUi(self, SigninDlg):
        _translate = QtCore.QCoreApplication.translate
        SigninDlg.setWindowTitle(_translate("SigninDlg", "登记"))
        self.label.setText(_translate("SigninDlg", "工号："))
        self.label_2.setText(_translate("SigninDlg", "密码："))
        self.label_3.setText(_translate("SigninDlg", "确认密码："))
        self.btn_signin.setText(_translate("SigninDlg", "登  记"))
        self.info.setText(_translate("SigninDlg", "此工号已登记！"))

