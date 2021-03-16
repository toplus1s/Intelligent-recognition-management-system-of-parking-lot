# _*_ coding:utf-8 _*_
import pymssql
import random
import string
import global_
global_._init()

def park_edit(b,c):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "update parkInfo set PLEFT='"+b+"',PTEMP='"+c+"'"
    cursor.execute(sql)
    db.commit()
    db.close()

def user_create(uid,pwd):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "INSERT INTO userInfo(UID,PWD) values('"+uid+"','"+pwd+"') "
    cursor.execute(sql)
    db.commit()
    db.close()

def getParkInfo():
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "SELECT * FROM parkInfo "
    cursor.execute(sql)
    res = cursor.fetchone()  #读取查询结果,
    res = list(res)
    if res:              #循环读取所有结果
       return res
    else:
       return 0
    db.close()


def user_login(uid, pwd):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "SELECT UID,PWD FROM userInfo WHERE UID='"+ uid +"'"
    cursor.execute(sql)
    row = cursor.fetchone()  #读取查询结果,
    while row:
          #循环读取所有结果
        if pwd == row[1]:
            global_.set_value('UID',uid)
            return 1
        else:
            return 0
        row = cursor.fetchone()
    db.close()

def user_signin(uid, pwd):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "SELECT UID FROM userInfo "
    cursor.execute(sql)
    row = cursor.fetchone()  #读取查询结果,
    while row:      #循环读取所有结果
        if uid == row[0]:
            return 0
        row = cursor.fetchone()
    user_create(uid, pwd)
    global_.set_value('UID',uid)
    return 1
    db.close()



def user_logout(uid):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "delete userInfo where UID= '" + uid + "' "
    cursor.execute(sql)
    db.commit()
    db.close()


def getUserInfo(uid):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "SELECT UID,TCHARGE,FREENUM,HANDLET,SALENUM,AMOUNT FROM userInfo WHERE UID='"+ uid +"'"
    cursor.execute(sql)
    res = cursor.fetchone()  #读取查询结果,
    res = list(res)
    if res:              #循环读取所有结果
       return res
    else:
       return 0
    db.close()

def user_edit(uid,a,b,c,d,e):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "update userInfo set TCHARGE='"+a+"',FREENUM='"+b+"',HANDLET='"+c+"',SALENUM='"+d+"',AMOUNT='"+e+"' WHERE UID='"+ uid +"'"
    cursor.execute(sql)
    db.commit()
    db.close()

def car_addexit(cid,datetime):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "insert into carInfo(CID,CTYPE,STATE,END_TIME) values('"+cid+"','临时车','离场','"+datetime+"')"
    cursor.execute(sql)
    db.commit()
    db.close()

def car_addenter(cid,datetime):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "insert into carInfo(CID,CTYPE,STATE,START_TIME) values('"+cid+"','临时车','在场','"+datetime+"')"
    cursor.execute(sql)
    db.commit()
    db.close()

def car_exitRegister(cid,datetime):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "update carInfo set STATE='离场',END_TIME='"+datetime+"' WHERE CTYPE = '固定车' and CID='"+ cid +"'"
    cursor.execute(sql)
    db.commit()
    db.close()

def car_enterRegister(cid,datetime):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "update carInfo set STATE='在场',START_TIME='"+datetime+"' WHERE CTYPE = '固定车' and CID='"+ cid +"' "
    cursor.execute(sql)
    db.commit()
    db.close()

def car_getallenter():
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = " select CID,CTYPE,STATE,START_TIME from carInfo WHERE START_TIME is not NULL "
    cursor.execute(sql)
    row = cursor.fetchall()
    return row
    db.commit()
    db.close()

def car_getallexit():
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = " select CID,CTYPE,STATE,END_TIME from carInfo WHERE END_TIME is not NULL "
    cursor.execute(sql)
    row = cursor.fetchall()
    return row
    db.commit()
    db.close()

def car_edit(res,x):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "update carInfo set CID='"+res[0]+"',CTYPE='"+res[1]+"',STATE='"+res[2]+"' WHERE CID='"+ x +"'"
    cursor.execute(sql)
    db.commit()
    db.close()

def car_add(res):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    sql = "insert into carInfo(CID,CTYPE,STATE) values('"+res[0]+"','"+res[1]+"','"+res[2]+"')"
    cursor.execute(sql)
    db.commit()
    db.close()

def car_del(res):
    db = pymssql.connect("localhost", "saa", "saa", "CIMS")
    cursor = db.cursor()
    i = 0
    while i < len(res):
        sql = "delete carInfo where CID= '" + res[i][0] + "' "
        cursor.execute(sql)
        i += 1
        db.commit()
    db.close()


def car_find(y):
        db = pymssql.connect("localhost", "saa", "saa", "CIMS")
        cursor = db.cursor()
        sql = "SELECT * FROM carInfo WHERE  CID = '" + y + "' "
        cursor.execute(sql)
        row = cursor.fetchall()
        if row:
            return row
        else:
            return 0
        db.close()




