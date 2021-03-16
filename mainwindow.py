# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'mainwindow.ui'
#
# Created by: PyQt5 UI code generator 5.10.1
#
# WARNING! All changes made in this file will be lost!

from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtCore, QtGui, QtWidgets
import numpy as np
import cv2
import db_event
import global_
from car_id_detect import *
from svm_train import *
from card_seg import *
import datetime
import math
global_._init()



def on_btn_letout_clicked(self,User,Park):
    picdlg(self)
    if(self.comboBox.currentText == "免费"):
        db_event.user_edit(User[0],User[1],str(int(User[2])+1),str(int(User[3])+1),User[4],User[5])
    else:
        db_event.user_edit(User[0],str(int(User[1])+int(self.l_charge.text())),User[2],str(int(User[3])+1),str(int(User[4])+1),str(int(User[5])+int(self.l_charge.text())))
    db_event.park_edit(str(int(Park[1])-1),str(int(Park[2])+1))
    QMessageBox.information(self,"提示","操作成功！")
    Park = db_event.getParkInfo()
    User = db_event.getUserInfo(global_.get_value('UID'))
    self.l_pinfo1.setText(Park[0])
    self.l_pinfo2.setText(Park[1])
    self.l_pinfo3.setText(Park[2])
    self.l_pinfo4.setText(Park[3])
    self.l_chinfo1.setText(User[0])
    self.l_chinfo3.setText(User[1])
    self.l_chinfo4.setText(User[2])
    self.l_chinfo5.setText(User[3])
    self.l_chinfo6.setText(User[4])
    self.l_chinfo7.setText(User[5])
    self.btn_letout.setEnabled(False)



def pcharge(self):
    if(self.l_ninfo1.text() != ""):
            charge = int(self.l_ninfo1.text().replace("小时",""))*5-int(self.comboBox.currentText().replace("元",""))
            self.l_charge.setText(str(charge))
    else:
        return

@pyqtSlot()
def on_btn_pic2_clicked(self):
    """
    加载图像
    """
    print("加载图像")
    try:
        self.file_dir_temp,_ = QFileDialog.getOpenFileName(self,"选择被检测的车辆",global_.get_value('PATH')+"/CIMS/test_img")
        self.file_dir = self.file_dir_temp.replace("\\","/")
        print(self.file_dir)

        roi, l_exitCam, color = CaridDetect(self.file_dir)
        seg_dict, _, pre = Cardseg([roi],[color],None)

        # segment
        cv2.imwrite(os.path.join(global_.get_value('PATH')+"/CIMS/temp/seg_card.jpg"),roi)
        seg_img = cv2.imread(global_.get_value('PATH')+"/CIMS/temp/seg_card.jpg")
        seg_rows, seg_cols, seg_channels = seg_img.shape
        bytesPerLine = seg_channels * seg_cols
        cv2.cvtColor(seg_img, cv2.COLOR_BGR2RGB,seg_img)
        QImg = QImage(seg_img.data, seg_cols, seg_rows,bytesPerLine, QImage.Format_RGB888)

        # reg result
        pre.insert(2,"·")
        res = "".join(pre)
        self.l_exitNum.setText(res)
        car = db_event.car_find(res)
        try:
            self.l_exitCarinfo.setText("临时车")
            for i in car:
                print(i)
                if(i[1] == "固定车"):
                    self.l_exitCarinfo.setText("固定车")
                    break
                else:
                    continue
            self.l_ninfo2.setText(car[0][3].strftime("%Y-%m-%d %H:%M:%S"))
            self.l_ninfo3.setText(datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            total_seconds = (datetime.datetime.now() - (car[0][3])).total_seconds()
            hour_sub = math.ceil(total_seconds / 3600)
            self.l_ninfo1.setText(str(hour_sub) + "小时")
            charge = int(self.l_ninfo1.text().replace("小时",""))*5-int(self.comboBox.currentText().replace("元",""))
            self.l_charge.setText(str(charge))
            self.btn_letout.setEnabled(True)
        except Exception as e:
            QMessageBox.warning(self,"错误提示","[错误提示(请联系开发人员处理)]：\n" + str(e)+"\n或识别失败导致")
            QMessageBox.warning(self,"错误提示","此车没有在场登记！")

        frame = cv2.imread(self.file_dir)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img_rows, img_cols, channels = frame.shape
        bytesPerLine = channels * img_cols
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB,frame)
        QImg = QImage(frame.data, img_cols, img_rows,bytesPerLine, QImage.Format_RGB888)
        self.l_exitCam.setPixmap(QPixmap.fromImage(QImg).scaled(self.l_exitCam.size(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation))
        QtWidgets.QApplication.processEvents()

    except Exception as e:
        QMessageBox.warning(self,"错误提示","[错误提示(请联系开发人员处理)]：\n" + str(e)+"\n或识别失败导致")

@pyqtSlot()
def on_btn_pic_clicked(self):
    """
    加载图像
    """
    print("加载图像")
    try:
        self.file_dir_temp,_ = QFileDialog.getOpenFileName(self,"选择被检测的车辆","D:/Qt_for_py/XSN721/CIMS/test_img")
        self.file_dir = self.file_dir_temp.replace("\\","/")
        print(self.file_dir)

        roi, l_enterCam, color = CaridDetect(self.file_dir)
        seg_dict, _, pre = Cardseg([roi],[color],None)

        # segment
        cv2.imwrite(os.path.join(global_.get_value('PATH')+"/CIMS/temp/seg_card.jpg"),roi)
        seg_img = cv2.imread(global_.get_value('PATH')+"/CIMS/temp/seg_card.jpg")
        seg_rows, seg_cols, seg_channels = seg_img.shape
        bytesPerLine = seg_channels * seg_cols
        cv2.cvtColor(seg_img, cv2.COLOR_BGR2RGB,seg_img)
        QImg = QImage(seg_img.data, seg_cols, seg_rows,bytesPerLine, QImage.Format_RGB888)

        # reg result
        pre.insert(2,"·")
        res = "".join(pre)
        self.l_enterNum.setText(res)
        car = db_event.car_find(res)
        try:
            self.l_enterCarinfo.setText("临时车")
            for i in car:
                if(i[1] == "固定车"):
                    self.l_enterCarinfo.setText("固定车")
                    break
                else:
                    continue
        except Exception as e:
            self.l_enterCarinfo.setText("临时车")
        frame = cv2.imread(self.file_dir)
        font = cv2.FONT_HERSHEY_SIMPLEX
        img_rows, img_cols, channels = frame.shape
        bytesPerLine = channels * img_cols
        cv2.cvtColor(frame, cv2.COLOR_BGR2RGB,frame)
        QImg = QImage(frame.data, img_cols, img_rows,bytesPerLine, QImage.Format_RGB888)
        self.l_enterCam.setPixmap(QPixmap.fromImage(QImg).scaled(self.l_enterCam.size(),
            Qt.KeepAspectRatio, Qt.SmoothTransformation))
        QtWidgets.QApplication.processEvents()

    except Exception as e:
        QMessageBox.warning(self,"错误提示","[错误提示(请联系开发人员处理)]：\n" + str(e)+"\n或识别失败导致")


@pyqtSlot()
def on_btn_vid_clicked(self):
    """
    加载视频
    """
    print("加载视频")
    QMessageBox.information(self,"加载实时视频","未检测到实时视频源或暂未开通该服务！")

def exit(self,Park):
    Park = db_event.getParkInfo()
    cid = self.l_exitNum.text()
    if(cid != ""):
            car = db_event.car_find(cid)
            try:
                flag = 0
                for i in car:
                    if(i[1] == "固定车"):
                        flag = 1
                        break
                    else:
                        continue
                if(flag == 1):
                    db_event.car_exitRegister(cid,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    QMessageBox.information(self, "固定车", "操作成功！")
                    self.l_exitNum.setText("")
                    self.l_exitCarinfo.setText("")
                else:
                    db_event.car_addexit(cid,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    QMessageBox.information(self, "临时车", "操作成功！")
                    self.l_exitNum.setText("")
                    self.l_exitCarinfo.setText("")

            except Exception as e:
                QMessageBox.warning(self,"错误提示","[错误提示(请联系开发人员处理)]：\n" + str(e)+"\n或识别失败导致")
    else:
        QMessageBox.information(self, "提示", "没有检测到车辆，无需抬杆！")
    db_event.park_edit(str(int(Park[1])+1),str(int(Park[2])-1))
    self.l_pinfo2.setText(str(int(Park[1])+1))
    self.l_pinfo3.setText(str(int(Park[2])-1))
    carexitlist = db_event.car_getallexit()
    for row in range(len(carexitlist)):
        for column in range(4):
            item=QStandardItem(str(carexitlist[row][column]))
            self.model2.setItem(row,column,item)


def enter(self,Park):
    Park = db_event.getParkInfo()
    cid = self.l_enterNum.text()
    if(cid != ""):
        if(int(Park[1])>0):
            car = db_event.car_find(cid)
            try:
                flag = 0
                for i in car:
                    if(i[1] == "固定车"):
                        flag = 1
                        break
                    else:
                        continue
                if(flag == 1):
                    db_event.car_enterRegister(cid,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    QMessageBox.information(self, "固定车", "操作成功！")
                    self.l_enterNum.setText("")
                    self.l_enterCarinfo.setText("")
                elif(int(Park[1])-int(Park[3])>0):
                    db_event.car_addenter(cid,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                    QMessageBox.information(self, "提示", "操作成功！")
                    self.l_enterNum.setText("")
                    self.l_enterCarinfo.setText("")

            except:
                db_event.car_addenter(cid,datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
                QMessageBox.information(self, "临时车", "操作成功！")
                self.l_enterNum.setText("")
                self.l_enterCarinfo.setText("")
        else:
            QMessageBox.information(self, "提示", "停车位已满！")
            self.l_enterNum.setText("")
            self.l_enterCarinfo.setText("")
    else:
        QMessageBox.information(self, "提示", "没有检测到车辆，无需抬杆！")
    db_event.park_edit(str(int(Park[1])-1),str(int(Park[2])+1))
    self.l_pinfo2.setText(str(int(Park[1])-1))
    self.l_pinfo3.setText(str(int(Park[2])+1))
    carenterlist = db_event.car_getallenter()
    for row in range(len(carenterlist)):
        for column in range(4):
            item=QStandardItem(str(carenterlist[row][column]))
            self.model.setItem(row,column,item)


def c_edit(dialog,self,a,b,c,x):
    res = [0 for i in range(3)]
    res[0] = a
    res[1] = b
    res[2] = c
    db_event.car_edit(res,x)
    QMessageBox.information(dialog, "提示", "修改成功！")
    carexitlist = db_event.car_getallenter()
    for row in range(len(carexitlist)):
        for column in range(4):
            item=QStandardItem(str(carexitlist[row][column]))
            self.model2.setItem(row,column,item)
    carenterlist = db_event.car_getallenter()
    for row in range(len(carenterlist)):
        for column in range(4):
            item=QStandardItem(str(carenterlist[row][column]))
            self.model.setItem(row,column,item)
    dialog.close()

def c_add(dialog,self,a,b,c):
    res = [0 for i in range(3)]
    res[0] = a
    res[1] = b
    res[2] = c
    db_event.car_add(res)
    QMessageBox.information(dialog, "提示", "添加成功！")
    carexitlist = db_event.car_getallenter()
    for row in range(len(carexitlist)):
        for column in range(4):
            item=QStandardItem(str(carexitlist[row][column]))
            self.model2.setItem(row,column,item)
    carenterlist = db_event.car_getallenter()
    for row in range(len(carenterlist)):
        for column in range(4):
            item=QStandardItem(str(carenterlist[row][column]))
            self.model.setItem(row,column,item)
    dialog.close()

def c_del(dialog,self,y):
    data = db_event.car_find(y)
    if(data):
        db_event.car_del(data)
        QMessageBox.information(dialog, "提示", "删除成功！")
        carexitlist = db_event.car_getallenter()
        for row in range(len(carexitlist)):
            for column in range(4):
                item=QStandardItem(str(carexitlist[row][column]))
                self.model2.setItem(row,column,item)
        carenterlist = db_event.car_getallenter()
        for row in range(len(carenterlist)):
            for column in range(4):
                item=QStandardItem(str(carenterlist[row][column]))
                self.model.setItem(row,column,item)
    else:
        QMessageBox.information(dialog, "提示", "查无此车。")
    dialog.close()

def picdlg(self):
    dialog = QDialog()
    dialog.resize(400,400)
    label1 = QLabel(dialog)
    label1.setGeometry(QtCore.QRect(20,20, 300, 300))
    label1.setStyleSheet("QLabel{border-image: url(D:/example.jpg);}")#替换一张二维码
    dialog.setWindowTitle("收款")
    dialog.setWindowModality(Qt.ApplicationModal)
    dialog.exec()


def addCarDlg(self):
    dialog = QDialog()
    dialog.resize(400,400)
    label1 = QLabel(dialog)
    label1.setText("车牌号：")
    label1.setGeometry(QtCore.QRect(50,50, 121, 31))
    label2 = QLabel(dialog)
    label2.setText("车辆类型：")
    label2.setGeometry(QtCore.QRect(50,100, 121, 31))
    label3 = QLabel(dialog)
    label3.setText("状态：")
    label3.setGeometry(QtCore.QRect(50,150, 121, 31))
    label4 = QLabel(dialog)
    label4.setText("进场时间：")
    label4.setGeometry(QtCore.QRect(50,200, 121, 31))
    label5 = QLabel(dialog)
    label5.setText("离场时间：")
    label5.setGeometry(QtCore.QRect(50,250, 121, 31))


    l_name = QLineEdit(dialog)
    l_name.setGeometry(QtCore.QRect(150,50, 121, 31))
    l_name.setObjectName("l_name")

    comboBox = QComboBox(dialog)
    comboBox.setGeometry(QtCore.QRect(150,100, 121, 31))
    comboBox.setObjectName("comboBox")
    comboBox.addItem("临时车")
    comboBox.addItem("固定车")

    comboBox2 = QComboBox(dialog)
    comboBox2.setGeometry(QtCore.QRect(150,150, 121, 31))
    comboBox2.setObjectName("comboBox2")
    comboBox2.addItem("离场")
    comboBox2.addItem("在场")

    l_startdate = QLineEdit(dialog)
    l_startdate.setGeometry(QtCore.QRect(150,200, 200, 31))
    l_startdate.setObjectName("l_startdate")
    l_startdate.setEnabled(False)

    l_enddate = QLineEdit(dialog)
    l_enddate.setGeometry(QtCore.QRect(150,250,200, 31))
    l_enddate.setObjectName("l_enddate")
    l_enddate.setEnabled(False)

    button = QPushButton('确定',dialog)
    button.clicked.connect(lambda:c_add(dialog,self,l_name.text(),comboBox.currentText(),comboBox2.currentText()))
    button.move(150,300)
    dialog.setWindowTitle("添加")
    dialog.setWindowModality(Qt.ApplicationModal)
    dialog.exec()

def editCarDlg(dlg,self,cid):
        res = db_event.car_find(cid)
        if(res):
            dlg.close()
            dialog = QDialog()
            dialog.resize(400,400)
            label1 = QLabel(dialog)
            label1.setText("车牌号：")
            label1.setGeometry(QtCore.QRect(50,50, 121, 31))
            label2 = QLabel(dialog)
            label2.setText("车辆类型：")
            label2.setGeometry(QtCore.QRect(50,100, 121, 31))
            label3 = QLabel(dialog)
            label3.setText("状态：")
            label3.setGeometry(QtCore.QRect(50,150, 121, 31))
            label4 = QLabel(dialog)
            label4.setText("进场时间：")
            label4.setGeometry(QtCore.QRect(50,200, 121, 31))
            label5 = QLabel(dialog)
            label5.setText("离场时间：")
            label5.setGeometry(QtCore.QRect(50,250, 121, 31))

            l_name = QLineEdit(dialog)
            l_name.setGeometry(QtCore.QRect(150,50, 121, 31))
            l_name.setObjectName("l_name")
            l_name.setText(res[0][0].strip())

            comboBox = QComboBox(dialog)
            comboBox.setGeometry(QtCore.QRect(150,100, 121, 31))
            comboBox.setObjectName("comboBox")
            comboBox.addItem("临时车")
            comboBox.addItem("固定车")
            if res[0][1] == "固定车":
                comboBox.setCurrentIndex(1)

            comboBox2 = QComboBox(dialog)
            comboBox2.setGeometry(QtCore.QRect(150,150, 121, 31))
            comboBox2.setObjectName("comboBox2")
            comboBox2.setCurrentText(res[0][2])
            comboBox2.addItem("离场")
            comboBox2.addItem("在场")
            if res[0][1] == "在场":
                comboBox.setCurrentIndex(1)

            l_startdate = QLineEdit(dialog)
            l_startdate.setGeometry(QtCore.QRect(150,200, 200, 31))
            l_startdate.setObjectName("l_startdate")
            l_startdate.setText(str(res[0][3]))
            l_startdate.setEnabled(False)

            l_enddate = QLineEdit(dialog)
            l_enddate.setGeometry(QtCore.QRect(150,250,200, 31))
            l_enddate.setObjectName("l_enddate")
            l_enddate.setText(str(res[0][4]))
            l_enddate.setEnabled(False)


            button = QPushButton('确定',dialog)
            button.clicked.connect(lambda:c_edit(dialog,self,l_name.text(),comboBox.currentText(),comboBox2.currentText(),cid))
            button.move(150,300)
            dialog.setWindowTitle("修改")
            dialog.setWindowModality(Qt.ApplicationModal)
            dialog.exec()
        else:
            QMessageBox.information(dlg, "提示", "查无此车。")


#def WrittingNotOfOther(self,tag):
#    if tag == 1:
#        dlg.label2.setText("请输入车牌号：")
#        dlg.lineEdit.show()
#    if tag == 2:
#        dlg.label2.setText("请选择车辆类型：")
#        dlg.lineEdit.hide()
#        cb = QComboBox(dlg)
#        cb.setGeometry(QtCore.QRect(150,100, 121, 31))
#        cb.addItem("临时车")
#        cb.addItem("固定车")
#    if tag == 2:
#        dlg.label2.setText("请选择状态：")
#        dlg.lineEdit.hide()
#        cb = QComboBox(dlg)
#        cb.setGeometry(QtCore.QRect(150,100, 121, 31))
#        cb.addItem("离场")
#        cb.addItem("在场")


def findCarDlg(self,way):
    dialog = QDialog()
    dialog.resize(400,300)
    label2 = QLabel(dialog)
    label2.setText("请输入车牌号：")
    label2.setGeometry(QtCore.QRect(50,100, 121, 31))
    label2.setObjectName("label2")

#    comboBox = QComboBox(dialog)
#    comboBox.setGeometry(QtCore.QRect(150,50, 121, 31))
#    comboBox.setObjectName("comboBox")
#    comboBox.addItem("车牌号")
#    comboBox.addItem("车辆类型")
#    comboBox.addItem("状态")
#    comboBox.currentIndexChanged.connect(lambda: WrittingNotOfOther(dialog,comboBox.currentIndex()))

    lineEdit = QLineEdit(dialog)
    lineEdit.setGeometry(QtCore.QRect(150,100, 121, 31))
    lineEdit.setObjectName("lineEdit")

    button = QPushButton('确定',dialog)
    if way == "查找":
        button.clicked.connect(lambda:find(dialog,self,lineEdit.text()))
#    elif way == "借书":
#        button.clicked.connect(lambda:borrow(dialog,self,comboBox.currentText(),lineEdit.text()))
#    elif way == "还书":
#        button.clicked.connect(lambda:breturn(dialog,self,comboBox.currentText(),lineEdit.text()))
#    elif way == "处理逾期书籍":
#        button.clicked.connect(lambda:dispose(dialog,self,comboBox.currentText(),lineEdit.text()))
    elif way == "删除":
        button.clicked.connect(lambda:c_del(dialog,self,lineEdit.text()))
    elif way == "修改":
        button.clicked.connect(lambda:editCarDlg(dialog,self,lineEdit.text()))

    button.move(150,200)
    dialog.setWindowTitle(way)
    dialog.setWindowModality(Qt.ApplicationModal)
    dialog.exec()

def find(dlg,self,y):
    res = db_event.car_find(y)
    if(res):
        dlg.close()
        dialog = QDialog()
        dialog.resize(400,300)
        label1 = QLabel(dialog)
        label1.setText("车牌号：")
        label1.setGeometry(QtCore.QRect(50,50, 121, 31))
        label2 = QLabel(dialog)
        label2.setText("车辆类型：")
        label2.setGeometry(QtCore.QRect(50,100, 121, 31))
        label3 = QLabel(dialog)
        label3.setText("状态：")
        label3.setGeometry(QtCore.QRect(50,150, 121, 31))
        label4 = QLabel(dialog)
        label4.setText("进场时间：")
        label4.setGeometry(QtCore.QRect(50,200, 121, 31))
        label5 = QLabel(dialog)
        label5.setText("离场时间：")
        label5.setGeometry(QtCore.QRect(50,250, 121, 31))

        l_name = QLineEdit(dialog)
        l_name.setGeometry(QtCore.QRect(150,50, 121, 31))
        l_name.setObjectName("l_name")
        l_name.setText(res[0][0].strip())
        l_name.setEnabled(False)

        comboBox = QComboBox(dialog)
        comboBox.setGeometry(QtCore.QRect(150,100, 121, 31))
        comboBox.setObjectName("comboBox")
        comboBox.addItem("临时车")
        comboBox.addItem("固定车")
        if res[0][1] == "固定车":
            comboBox.setCurrentIndex(1)
        comboBox.setEnabled(False)

        comboBox2 = QComboBox(dialog)
        comboBox2.setGeometry(QtCore.QRect(150,150, 121, 31))
        comboBox2.setObjectName("comboBox2")
        comboBox2.setCurrentText(res[0][2])
        comboBox2.addItem("离场")
        comboBox2.addItem("在场")
        if res[0][1] == "在场":
            comboBox2.setCurrentIndex(1)
        comboBox2.setEnabled(False)

        l_startdate = QLineEdit(dialog)
        l_startdate.setGeometry(QtCore.QRect(150,200, 200, 31))
        l_startdate.setObjectName("l_startdate")
        l_startdate.setText(str(res[0][3]))
        l_startdate.setEnabled(False)

        l_enddate = QLineEdit(dialog)
        l_enddate.setGeometry(QtCore.QRect(150,250,200, 31))
        l_enddate.setObjectName("l_enddate")
        l_enddate.setText(str(res[0][4]))
        l_enddate.setEnabled(False)
        dialog.setWindowTitle("查找结果")
        dialog.setWindowModality(Qt.ApplicationModal)
        dialog.exec()
    else:
        QMessageBox.information(dlg, "提示", "查无此车。")



class Ui_Form(QtWidgets.QWidget):
    def __init__(self):
        super(Ui_Form,self).__init__()
        self.setupUi(self)

    def setupUi(self, Form):
        Park = db_event.getParkInfo()
        User = db_event.getUserInfo(global_.get_value('UID'))

        Form.setObjectName("Form")
        Form.resize(1248, 811)
        self.l_enterCam = QtWidgets.QLabel(Form)
        self.l_enterCam.setGeometry(QtCore.QRect(460, 40, 391, 271))
        self.l_enterCam.setText("")
        self.l_enterCam.setObjectName("l_enterCam")

        self.l_exitCam = QtWidgets.QLabel(Form)
        self.l_exitCam.setGeometry(QtCore.QRect(460, 440, 391, 271))
        self.l_exitCam.setText("")
        self.l_exitCam.setObjectName("l_exitCam")

        self.l_enterNum = QtWidgets.QLabel(Form)
        self.l_enterNum.setGeometry(QtCore.QRect(630, 320, 111, 21))
        self.l_enterNum.setText("")
        self.l_enterNum.setObjectName("l_enterNum")

        self.l_exitNum = QtWidgets.QLabel(Form)
        self.l_exitNum.setGeometry(QtCore.QRect(630, 720, 111, 21))
        self.l_exitNum.setText("")
        self.l_exitNum.setObjectName("l_exitNum")

        self.l_enterCarinfo = QtWidgets.QLabel(Form)
        self.l_enterCarinfo.setGeometry(QtCore.QRect(560, 360, 72, 15))
        self.l_enterCarinfo.setText("")
        self.l_enterCarinfo.setObjectName("l_enterCarinfo")

        self.l_exitCarinfo = QtWidgets.QLabel(Form)
        self.l_exitCarinfo.setGeometry(QtCore.QRect(560, 760, 72, 15))
        self.l_exitCarinfo.setText("")
        self.l_exitCarinfo.setObjectName("l_exitCarinfo")

        self.l_charge = QtWidgets.QLabel(Form)
        self.l_charge.setGeometry(QtCore.QRect(1010, 620, 101, 41))
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(15)
        self.l_charge.setFont(font)
        self.l_charge.setStyleSheet("color:rgb(200,101,102)")
        self.l_charge.setText("")
        self.l_charge.setAlignment(QtCore.Qt.AlignCenter)
        self.l_charge.setObjectName("l_charge")

        self.l_pinfo1 = QtWidgets.QLabel(Form)
        self.l_pinfo1.setGeometry(QtCore.QRect(970, 90, 72, 15))
        self.l_pinfo1.setText(Park[0])
        self.l_pinfo1.setObjectName("l_pinfo1")

        self.l_pinfo2 = QtWidgets.QLabel(Form)
        self.l_pinfo2.setGeometry(QtCore.QRect(970, 113, 72, 15))
        self.l_pinfo2.setText(Park[1])
        self.l_pinfo2.setObjectName("l_pinfo2")

        self.l_pinfo3 = QtWidgets.QLabel(Form)
        self.l_pinfo3.setGeometry(QtCore.QRect(970, 137, 72, 15))
        self.l_pinfo3.setText(Park[2])
        self.l_pinfo3.setObjectName("l_pinfo3")

        self.l_pinfo4 = QtWidgets.QLabel(Form)
        self.l_pinfo4.setGeometry(QtCore.QRect(970, 161, 72, 15))
        self.l_pinfo4.setText(Park[3])
        self.l_pinfo4.setObjectName("l_pinfo4")

        self.l_chinfo1 = QtWidgets.QLabel(Form)
        self.l_chinfo1.setGeometry(QtCore.QRect(980, 239, 72, 15))
        self.l_chinfo1.setText(User[0])
        self.l_chinfo1.setObjectName("l_chinfo1")

        self.l_chinfo2 = QtWidgets.QLabel(Form)
        self.l_chinfo2.setGeometry(QtCore.QRect(980, 262, 200, 15))
        self.l_chinfo2.setText(QDateTime.currentDateTime().toString())
        self.l_chinfo2.setObjectName("l_chinfo2")

        self.l_chinfo3 = QtWidgets.QLabel(Form)
        self.l_chinfo3.setGeometry(QtCore.QRect(980, 286, 72, 15))
        self.l_chinfo3.setText(User[1])
        self.l_chinfo3.setObjectName("l_chinfo3")

        self.l_chinfo4 = QtWidgets.QLabel(Form)
        self.l_chinfo4.setGeometry(QtCore.QRect(980, 310, 72, 15))
        self.l_chinfo4.setText(User[2])
        self.l_chinfo4.setObjectName("l_chinfo4")

        self.l_chinfo5 = QtWidgets.QLabel(Form)
        self.l_chinfo5.setGeometry(QtCore.QRect(980, 335, 72, 15))
        self.l_chinfo5.setText(User[3])
        self.l_chinfo5.setObjectName("l_chinfo5")

        self.l_chinfo6 = QtWidgets.QLabel(Form)
        self.l_chinfo6.setGeometry(QtCore.QRect(980, 359, 72, 15))
        self.l_chinfo6.setText(User[4])
        self.l_chinfo6.setObjectName("l_chinfo6")

        self.l_chinfo7 = QtWidgets.QLabel(Form)
        self.l_chinfo7.setGeometry(QtCore.QRect(980, 383, 72, 15))
        self.l_chinfo7.setText(User[5])
        self.l_chinfo7.setObjectName("l_chinfo7")

        self.l_ninfo1 = QtWidgets.QLabel(Form)
        self.l_ninfo1.setGeometry(QtCore.QRect(970, 500, 200, 15))
        self.l_ninfo1.setText("")
        self.l_ninfo1.setObjectName("l_ninfo3")

        self.l_ninfo2 = QtWidgets.QLabel(Form)
        self.l_ninfo2.setGeometry(QtCore.QRect(970, 453, 200, 15))
        self.l_ninfo2.setText("")
        self.l_ninfo2.setObjectName("l_ninfo2")

        self.l_ninfo3 = QtWidgets.QLabel(Form)
        self.l_ninfo3.setGeometry(QtCore.QRect(970, 476, 200, 15))
        self.l_ninfo3.setText("")
        self.l_ninfo3.setObjectName("l_ninfo1")



        self.centralwidget2 = QtWidgets.QWidget(Form)
        self.centralwidget2.setObjectName("centralwidget2")
        self.t_exitinfo = QtWidgets.QTableView(self.centralwidget2)
        self.t_exitinfo.horizontalHeader().setDefaultSectionSize(80)
        self.t_exitinfo.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.t_exitinfo.setGeometry(QtCore.QRect(30, 440, 411, 341))
        self.t_exitinfo.setObjectName("t_exitinfo")
        self.model2= QStandardItemModel(1000,4)
        self.model2.setHorizontalHeaderLabels(['车牌号','车辆类型','状态','离场时间'])
        carexitlist = db_event.car_getallexit()
        for row in range(len(carexitlist)):
            for column in range(4):
                item=QStandardItem(str(carexitlist[row][column]))
                self.model2.setItem(row,column,item)
        self.t_exitinfo.setModel(self.model2)


        self.centralwidget = QtWidgets.QWidget(Form)
        self.centralwidget.setObjectName("centralwidget")
        self.t_enterinfo = QtWidgets.QTableView(self.centralwidget)
        self.t_enterinfo.horizontalHeader().setDefaultSectionSize(80)
        self.t_enterinfo.horizontalHeader().setSectionResizeMode(QHeaderView.Interactive)
        self.t_enterinfo.setGeometry(QtCore.QRect(30, 40, 411, 341))
        self.t_enterinfo.setObjectName("t_enterinfo")
        self.model= QStandardItemModel(1000,4)
        self.model.setHorizontalHeaderLabels(['车牌号','车辆类型','状态','进场时间'])
        carenterlist = db_event.car_getallenter()
        for row in range(len(carenterlist)):
            for column in range(4):
                item=QStandardItem(str(carenterlist[row][column]))
                self.model.setItem(row,column,item)
        self.t_enterinfo.setModel(self.model)


        self.btn_pic = QtWidgets.QPushButton(Form)
        self.btn_pic.setGeometry(QtCore.QRect(650, 360, 72, 20))
        self.btn_pic.setStyleSheet("background-color:rgb(150,200,50);color:rgb(255,255,255)")
        self.btn_pic.setText("加载图片")
        self.btn_pic.setObjectName("btn_pic")
        self.btn_pic.clicked.connect(lambda:on_btn_pic_clicked(self))


        self.btn_vid = QtWidgets.QPushButton(Form)
        self.btn_vid.setGeometry(QtCore.QRect(740, 360, 72, 20))
        self.btn_vid.setStyleSheet("background-color:rgb(150,200,50);color:rgb(255,255,255)")
        self.btn_vid.setText("加载视频")
        self.btn_vid.setObjectName("btn_vid")
        self.btn_vid.clicked.connect(lambda:on_btn_vid_clicked(self))


        self.btn_pic2 = QtWidgets.QPushButton(Form)
        self.btn_pic2.setGeometry(QtCore.QRect(650, 760, 72, 20))
        self.btn_pic2.setStyleSheet("background-color:rgb(150,200,50);color:rgb(255,255,255)")
        self.btn_pic2.setText("加载图片")
        self.btn_pic2.setObjectName("btn_pic2")
        self.btn_pic2.clicked.connect(lambda:on_btn_pic2_clicked(self))


        self.btn_vid2 = QtWidgets.QPushButton(Form)
        self.btn_vid2.setGeometry(QtCore.QRect(740, 760, 72, 20))
        self.btn_vid2.setStyleSheet("background-color:rgb(150,200,50);color:rgb(255,255,255)")
        self.btn_vid2.setText("加载视频")
        self.btn_vid2.setObjectName("btn_vid2")
        self.btn_vid2.clicked.connect(lambda:on_btn_vid_clicked(self))


        self.btn_enter = QtWidgets.QPushButton(Form)
        self.btn_enter.setGeometry(QtCore.QRect(460, 320, 89, 24))
        self.btn_enter.setStyleSheet("background-color:rgb(150,200,50);color:rgb(255,255,255)")
        self.btn_enter.setObjectName("btn_enter")
        self.btn_enter.clicked.connect(lambda:enter(self,Park))

        self.btn_exit = QtWidgets.QPushButton(Form)
        self.btn_exit.setGeometry(QtCore.QRect(460, 720, 89, 24))
        self.btn_exit.setStyleSheet("background-color:rgb(150,200,50);color:rgb(255,255,255)")
        self.btn_exit.setObjectName("btn_exit")
        self.btn_exit.clicked.connect(lambda:exit(self,Park))

        self.btn_del = QtWidgets.QPushButton(Form)
        self.btn_del.setGeometry(QtCore.QRect(1050, 10, 89, 24))
        self.btn_del.setStyleSheet("background-color:rgb(50,100,150);color:rgb(255,255,255)")
        self.btn_del.setObjectName("btn_del")
        self.btn_del.clicked.connect(lambda:findCarDlg(self,"删除"))

        self.btn_find = QtWidgets.QPushButton(Form)
        self.btn_find.setGeometry(QtCore.QRect(1140, 10, 89, 24))
        self.btn_find.setStyleSheet("background-color:rgb(50,100,150);color:rgb(255,255,255)")
        self.btn_find.setObjectName("btn_find")
        self.btn_find.clicked.connect(lambda:findCarDlg(self,"查找"))

        self.btn_edit = QtWidgets.QPushButton(Form)
        self.btn_edit.setGeometry(QtCore.QRect(960, 10, 89, 24))
        self.btn_edit.setStyleSheet("background-color:rgb(50,100,150);color:rgb(255,255,255)")
        self.btn_edit.setObjectName("btn_edit")
        self.btn_edit.clicked.connect(lambda:findCarDlg(self,"修改"))

        self.btn_add = QtWidgets.QPushButton(Form)
        self.btn_add.setGeometry(QtCore.QRect(870, 10, 89, 24))
        self.btn_add.setStyleSheet("background-color:rgb(50,100,150);color:rgb(255,255,255)")
        self.btn_add.setObjectName("btn_add")
        self.btn_add.clicked.connect(lambda:addCarDlg(self))

        self.label_16 = QtWidgets.QLabel(Form)
        self.label_16.setGeometry(QtCore.QRect(870, 420, 351, 361))
        self.label_16.setStyleSheet("background-color:rgb(50,50,50,50)")
        self.label_16.setText("")
        self.label_16.setObjectName("label_16")

        self.btn_letout = QtWidgets.QPushButton(Form)
        self.btn_letout.setGeometry(QtCore.QRect(1000, 680, 111, 31))
        self.btn_letout.setStyleSheet("background-color:rgb(150,200,50);color:rgb(255,255,255)")
        self.btn_letout.setObjectName("btn_letout")
        self.btn_letout.clicked.connect(lambda:on_btn_letout_clicked(self,User,Park))
        self.btn_letout.setEnabled(False)

        self.btn_errors = QtWidgets.QPushButton(Form)
        self.btn_errors.setGeometry(QtCore.QRect(1000, 730, 111, 31))
        self.btn_errors.setStyleSheet("background-color:rgb(200,100,50);color:rgb(255,255,255)")
        self.btn_errors.setObjectName("btn_errors")
        self.btn_errors.setEnabled(False)

        self.comboBox = QtWidgets.QComboBox(Form)
        self.comboBox.setGeometry(QtCore.QRect(880, 570, 161, 23))
        self.comboBox.setObjectName("comboBox")
        self.comboBox.addItem("0元")
        self.comboBox.addItem("5元")
        self.comboBox.addItem("10元")
        self.comboBox.addItem("15元")
        self.comboBox.addItem("20元")
        self.comboBox.currentIndexChanged.connect(lambda:pcharge(self))


        self.linfo1 = QtWidgets.QLabel(Form)
        self.linfo1.setGeometry(QtCore.QRect(460, 10, 391, 20))
        self.linfo1.setStyleSheet("background-color:rgb(150,150,150);color:rgb(255,255,255)")
        self.linfo1.setAlignment(QtCore.Qt.AlignCenter)
        self.linfo1.setObjectName("linfo1")
        self.linfo3 = QtWidgets.QLabel(Form)
        self.linfo3.setGeometry(QtCore.QRect(460, 410, 391, 20))
        self.linfo3.setStyleSheet("background-color:rgb(150,150,150);color:rgb(255,255,255)")
        self.linfo3.setAlignment(QtCore.Qt.AlignCenter)
        self.linfo3.setObjectName("linfo3")
        self.linfo2 = QtWidgets.QLabel(Form)
        self.linfo2.setGeometry(QtCore.QRect(470, 360, 72, 16))
        self.linfo2.setObjectName("linfo2")
        self.linfo4 = QtWidgets.QLabel(Form)
        self.linfo4.setGeometry(QtCore.QRect(470, 760, 72, 16))
        self.linfo4.setObjectName("linfo4")
        self.linfo1_2 = QtWidgets.QLabel(Form)
        self.linfo1_2.setGeometry(QtCore.QRect(30, 10, 411, 20))
        self.linfo1_2.setStyleSheet("background-color:rgb(150,150,150);color:rgb(255,255,255)")
        self.linfo1_2.setAlignment(QtCore.Qt.AlignCenter)
        self.linfo1_2.setObjectName("linfo1_2")
        self.linfo3_2 = QtWidgets.QLabel(Form)
        self.linfo3_2.setGeometry(QtCore.QRect(30, 410, 411, 20))
        self.linfo3_2.setStyleSheet("background-color:rgb(150,150,150);color:rgb(255,255,255)")
        self.linfo3_2.setAlignment(QtCore.Qt.AlignCenter)
        self.linfo3_2.setObjectName("linfo3_2")
        self.label = QtWidgets.QLabel(Form)
        self.label.setGeometry(QtCore.QRect(870, 50, 351, 141))
        self.label.setStyleSheet("background-color:rgb(50,50,50,50)")
        self.label.setText("")
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(Form)
        self.label_2.setGeometry(QtCore.QRect(870, 200, 351, 211))
        self.label_2.setStyleSheet("background-color:rgb(50,50,50,50)")
        self.label_2.setText("")
        self.label_2.setObjectName("label_2")
        self.label_3 = QtWidgets.QLabel(Form)
        self.label_3.setGeometry(QtCore.QRect(880, 60, 81, 16))
        self.label_3.setStyleSheet("color:rgb(200,101,102)")
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(Form)
        self.label_4.setGeometry(QtCore.QRect(880, 90, 91, 16))
        self.label_4.setObjectName("label_4")
        self.label_5 = QtWidgets.QLabel(Form)
        self.label_5.setGeometry(QtCore.QRect(880, 113, 91, 16))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(Form)
        self.label_6.setGeometry(QtCore.QRect(880, 137, 91, 16))
        self.label_6.setObjectName("label_6")
        self.label_7 = QtWidgets.QLabel(Form)
        self.label_7.setGeometry(QtCore.QRect(880, 161, 91, 16))
        self.label_7.setObjectName("label_7")
        self.label_8 = QtWidgets.QLabel(Form)
        self.label_8.setGeometry(QtCore.QRect(880, 286, 91, 16))
        self.label_8.setObjectName("label_8")
        self.label_9 = QtWidgets.QLabel(Form)
        self.label_9.setGeometry(QtCore.QRect(880, 310, 91, 16))
        self.label_9.setObjectName("label_9")
        self.label_10 = QtWidgets.QLabel(Form)
        self.label_10.setGeometry(QtCore.QRect(880, 262, 91, 16))
        self.label_10.setObjectName("label_10")
        self.label_11 = QtWidgets.QLabel(Form)
        self.label_11.setGeometry(QtCore.QRect(880, 209, 81, 16))
        self.label_11.setStyleSheet("color:rgb(200,101,102)")
        self.label_11.setObjectName("label_11")
        self.label_12 = QtWidgets.QLabel(Form)
        self.label_12.setGeometry(QtCore.QRect(880, 239, 91, 16))
        self.label_12.setObjectName("label_12")
        self.label_13 = QtWidgets.QLabel(Form)
        self.label_13.setGeometry(QtCore.QRect(880, 335, 91, 16))
        self.label_13.setObjectName("label_13")
        self.label_14 = QtWidgets.QLabel(Form)
        self.label_14.setGeometry(QtCore.QRect(880, 359, 91, 16))
        self.label_14.setObjectName("label_14")
        self.label_15 = QtWidgets.QLabel(Form)
        self.label_15.setGeometry(QtCore.QRect(880, 383, 91, 16))
        self.label_15.setObjectName("label_15")
        self.label_17 = QtWidgets.QLabel(Form)
        self.label_17.setGeometry(QtCore.QRect(880, 500, 91, 16))
        self.label_17.setObjectName("label_17")
        self.label_18 = QtWidgets.QLabel(Form)
        self.label_18.setGeometry(QtCore.QRect(880, 423, 81, 16))
        self.label_18.setStyleSheet("color:rgb(200,101,102)")
        self.label_18.setObjectName("label_18")
        self.label_19 = QtWidgets.QLabel(Form)
        self.label_19.setGeometry(QtCore.QRect(880, 476, 91, 16))
        self.label_19.setObjectName("label_19")
        self.label_20 = QtWidgets.QLabel(Form)
        self.label_20.setGeometry(QtCore.QRect(880, 453, 91, 16))
        self.label_20.setObjectName("label_20")
        self.label_21 = QtWidgets.QLabel(Form)
        self.label_21.setGeometry(QtCore.QRect(880, 540, 81, 16))
        self.label_21.setStyleSheet("color:rgb(200,101,102)")
        self.label_21.setObjectName("label_21")

        font = QtGui.QFont()
        font.setPointSize(13)


        self.label_22 = QtWidgets.QLabel(Form)
        self.label_22.setFont(font)
        self.label_22.setGeometry(QtCore.QRect(960, 610, 41, 61))
        self.label_22.setObjectName("label_22")
        self.label_23 = QtWidgets.QLabel(Form)
        self.label_23.setFont(font)
        self.label_23.setGeometry(QtCore.QRect(1120, 610, 41, 61))
        self.label_23.setObjectName("label_23")

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "停车场车辆管理系统"))
        self.linfo1.setText(_translate("Form", "入口"))
        self.linfo3.setText(_translate("Form", "出口"))
        self.btn_enter.setText(_translate("Form", "抬杆(F4)"))
        self.btn_enter.setShortcut(_translate("Form", "F4"))
        self.btn_exit.setText(_translate("Form", "抬杆(F5)"))
        self.btn_exit.setShortcut(_translate("Form", "F5"))
        self.linfo2.setText(_translate("Form", "车辆类型："))
        self.linfo4.setText(_translate("Form", "车辆类型："))
        self.linfo1_2.setText(_translate("Form", "入口车辆历史记录"))
        self.linfo3_2.setText(_translate("Form", "出口车辆历史记录"))
        self.btn_del.setText(_translate("Form", "删除"))
        self.btn_find.setText(_translate("Form", "查找"))
        self.btn_edit.setText(_translate("Form", "修改"))
        self.btn_add.setText(_translate("Form", "添加"))
        self.label_3.setText(_translate("Form", "停车场信息"))
        self.label_4.setText(_translate("Form", "场内停车位："))
        self.label_5.setText(_translate("Form", "剩余停车位："))
        self.label_6.setText(_translate("Form", "临时车数量："))
        self.label_7.setText(_translate("Form", "固定车数量："))
        self.label_8.setText(_translate("Form", "临时车收费："))
        self.label_9.setText(_translate("Form", "免费车次："))
        self.label_10.setText(_translate("Form", "上班时间："))
        self.label_11.setText(_translate("Form", "收费信息"))
        self.label_12.setText(_translate("Form", "操 作 员："))
        self.label_13.setText(_translate("Form", "今日停车总量："))
        self.label_14.setText(_translate("Form", "优惠车数量："))
        self.label_15.setText(_translate("Form", "共收金额："))
        self.label_17.setText(_translate("Form", "计费提示："))
        self.label_18.setText(_translate("Form", "本次计费"))
        self.label_19.setText(_translate("Form", "计费时间："))
        self.label_20.setText(_translate("Form", "停车时间："))
        self.label_21.setText(_translate("Form", "优惠劵"))
        self.label_22.setText(_translate("Form", "收费"))
        self.label_23.setText(_translate("Form", "元"))
        self.btn_letout.setText(_translate("Form", "放行"))
        self.btn_errors.setText(_translate("Form", "异常处理"))

