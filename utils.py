from datetime import timedelta
from pickle import READONLY_BUFFER
import sqlite3
import os
from turtle import update
import cv2
import face_recognition
import numpy as np


def ReturnEmplID(CompanyName, Email):
    PATH = f"Companies/{CompanyName}/db.sql"
    mysql = sqlite3.connect(PATH)
    mycursor = mysql.cursor()
    query = f"select EMPL_ID from EMPL where EMPL_EMAIL='{Email}'"
    mycursor.execute(query)
    response = mycursor.fetchall()
    if response != []:
        EMPL_ID = str(response[0][0])
        return EMPL_ID
    else:
        return None


def PiltoND(img):
    pass


def rgbcovert(img):
    return cv2.cvtColor(img, cv2.COLOR_BGR2RGB)


def GiveEncode(img):
    return face_recognition.face_encodings(img)[0]


def FindEncodings(imgs):
    encodings = []
    for img in imgs:
        # img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        img = rgbcovert(img)
        encode = GiveEncode(img)
        encodings.append(encode)

    return encodings


def ReturnEncodingsFromFolder(CompanyName):

    PATH = f"Companies/{CompanyName}"
    images = []
    ClassNames = []
    li = os.listdir(PATH)
    li.remove("Current")
    li.remove("db.sql")

    for cl in li:
        img = cv2.imread(f"{PATH}/{cl}")
        images.append(img)
        ClassNames.append(os.path.splitext(cl)[0])

    KnownEncodings = FindEncodings(images)
    return [KnownEncodings, ClassNames]


def DateDifference(start, end):
    from datetime import datetime, timedelta
    delta = end - start  # as timedelta
    days = [str(start + timedelta(days=i))[:10] for i in range(delta.days + 1)]
    return days


def UPDATEDB(CompanyName, EMPL_ID):
    PATH = f"Companies/{CompanyName}/db.sql"
    mysql = sqlite3.connect(PATH)
    mycursor = mysql.cursor()
    import datetime
    today = datetime.date.today()
    # yesterday = today-datetime.timedelta(1)
    yesterday = "2022-03-03"
    query = f"SELECT DATE FROM '{EMPL_ID}';"
    mycursor.execute(query)
    response = mycursor.fetchall()
    dates = []
    for i in response:
        for j in i:
            dates.append(j)

    if dates != []:
        start = datetime.datetime(int(dates[-1][:4]), int(dates[-1][5:7]), int(
            dates[-1][-2:]))

        end = datetime.datetime(int(str(today)[:4]), int(str(today)[
            5:7]), int(str(today)[-2:]))
        end = end+timedelta(days=-1)
        if start < end:
            a = DateDifference(start, end)
            print(a)

            for date in a:
                query = f"INSERT INTO '{EMPL_ID}' (DATE,STATUS) VALUES ('{date}','ABSENT')"
                mycursor.execute(query)
                mysql.commit()
