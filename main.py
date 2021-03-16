# This Python file uses the following encoding: utf-8
import sys
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
from mainwindow import *
from LoginDlg import *
from SigninDlg import *
import db_event


def login(l):
    if db_event.user_login(l.t_userName.text(), l.t_pwd.text()):
        m = Ui_Form()
        m.show()
        l.hide()
    else:
        l.info.show()

def ltos(s,l):
    s.show()
    l.hide()

def signin(s):
    if db_event.user_signin(s.t_phoneNum.text(), s.t_pwd.text()):
        m = Ui_Form()
        m.show()
        s.hide()
    else:
        s.info.show()

if __name__ == "__main__":
    global_.set_value('PATH',"D:/Qt_for_py/XSN721") #文件夹地址，请自行修改#
    app = QtWidgets.QApplication(sys.argv)
    l = Ui_LoginDlg()
    s = Ui_SigninDlg()
    l.show();
    l.btn_login.clicked.connect(lambda:login(l))
    l.btn_signin.clicked.connect(lambda:ltos(s,l))
    s.btn_signin.clicked.connect(lambda:signin(s))
    # ...
    sys.exit(app.exec_())

