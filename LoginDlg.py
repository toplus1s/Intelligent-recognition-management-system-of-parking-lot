# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'logindlg.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

import sys
from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_LoginDlg(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_LoginDlg,self).__init__()
        self.setupUi(self)

    def setupUi(self, LoginDlg):
        LoginDlg.setObjectName("LoginDlg")
        LoginDlg.resize(544, 439)
        self.t_userName = QtWidgets.QLineEdit(LoginDlg)
        self.t_userName.setGeometry(QtCore.QRect(150, 220, 191, 31))
        self.t_userName.setObjectName("t_userName")

        self.t_pwd = QtWidgets.QLineEdit(LoginDlg)
        self.t_pwd.setGeometry(QtCore.QRect(150, 280, 191, 31))
        self.t_pwd.setObjectName("t_pwd")

        self.btn_login = QtWidgets.QPushButton(LoginDlg)
        self.btn_login.setGeometry(QtCore.QRect(150, 340, 191, 31))
        self.btn_login.setObjectName("btn_login")
        #self.btn_login.clicked.connect(self.login)

        self.info = QtWidgets.QLabel(LoginDlg)
        self.info.setGeometry(QtCore.QRect(150, 380, 191, 31))
        self.info.setObjectName("info")
        self.info.setText("用户名或密码错误！")
        self.info.hide()

        self.label = QtWidgets.QLabel(LoginDlg)
        self.label.setGeometry(QtCore.QRect(90, 230, 72, 15))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(LoginDlg)
        self.label_2.setGeometry(QtCore.QRect(90, 280, 72, 15))
        self.label_2.setObjectName("label_2")
        self.btn_signin = QtWidgets.QPushButton(LoginDlg)
        self.btn_signin.setGeometry(QtCore.QRect(370, 220, 89, 31))
        self.btn_signin.setObjectName("btn_signin")
        self.btn_logout = QtWidgets.QPushButton(LoginDlg)
        self.btn_logout.setGeometry(QtCore.QRect(370, 280, 89, 31))
        self.btn_logout.setObjectName("btn_logout")
        self.label_3 = QtWidgets.QLabel(LoginDlg)
        self.label_3.setGeometry(QtCore.QRect(110, 80, 331, 91))
        font = QtGui.QFont()
        font.setFamily("黑体")
        font.setPointSize(28)
        self.label_3.setFont(font)
        self.label_3.setObjectName("label_3")

        self.retranslateUi(LoginDlg)
        QtCore.QMetaObject.connectSlotsByName(LoginDlg)

    def retranslateUi(self, LoginDlg):
        _translate = QtCore.QCoreApplication.translate
        LoginDlg.setWindowTitle(_translate("LoginDlg", "登录"))
        self.btn_login.setText(_translate("LoginDlg", "登  录"))
        self.label.setText(_translate("LoginDlg", "工号："))
        self.label_2.setText(_translate("LoginDlg", "密码："))
        self.btn_signin.setText(_translate("LoginDlg", "登记新账户"))
        self.btn_logout.setText(_translate("LoginDlg", "注销账户"))
        self.label_3.setText(_translate("LoginDlg", "停车场管理系统"))


#    def show():
#        """
#        主函数，用于运行程序
#        :return: None
#        """
#        app = QtWidgets.QApplication(sys.argv)
#        w = QtWidgets.QWidget()
#        ui = Ui_LoginDlg()
#        ui.setupUi(w)
#        w.show()
#        sys.exit(app.exec_())

