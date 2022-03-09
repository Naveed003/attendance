from ast import Pass
from ctypes import util
from curses.ascii import EM
from datetime import date
import re
from tkinter.messagebox import YES
from urllib import response
from wsgiref.util import request_uri
from xml.etree.ElementInclude import FatalIncludeError
from apt import ProblemResolver
from cv2 import TonemapDrago
from django.http import QueryDict
from flask import Flask
from flask_restful import Api, Resource
import os

from pkg_resources import to_filename

import utils
import logging
import numpy as np
import face_recognition
import sqlite3
app = Flask(__name__)
api = Api(app)
# log = logging.getLogger('werkzeug')
# log.setLevel(logging.ERROR)


class FirstTime(Resource):
    def get(self, CompanyName, Email, url):

        from ImageExtract import ImageExtractAndSave

        response = utils.ReturnEmplID(CompanyName, Email)
        urls = [url]

        if response != None:
            EMPL_ID = str(response)
            PATH = f"Companies/{CompanyName}"
            li = os.listdir(PATH)
            li = os.listdir(PATH)
            EMPLS = []
            for cl in li:
                EMPLS.append(os.path.splitext(cl)[0])

            if EMPL_ID not in EMPLS:

                temp = ImageExtractAndSave(urls, EMPL_ID, CompanyName)

            import sqlite3
            import datetime
            today = datetime.date.today()
            time = datetime.datetime.now().time()
            time = str(time)[:5]

            PATH = f"Companies/{CompanyName}/db.sql"
            mysql = sqlite3.connect(PATH)
            mycursor = mysql.cursor()
            query = f'''CREATE TABLE "{EMPL_ID}" ("DATE" TEXT,"STATUS" TEXT,"TIME" TEXT,"REASONS" TEXT)'''
            mycursor.execute(query)
            query = f"insert into '{EMPL_ID}' (DATE,STATUS,TIME) VALUES('{str(today)}', 'PRESENT','{time}')"
            mycursor.execute(query)
            mysql.commit()
            mysql.close()
        return True


class MAIN(Resource):
    def get(self, CompanyName, Email, url):
        from ImageExtract import ImageExtractAndReturn
        import cv2
        EMPL_ID = utils.ReturnEmplID(CompanyName, Email)
        img = ImageExtractAndReturn(url, EMPL_ID, CompanyName)
        utils.UPDATEDB(CompanyName, EMPL_ID)
        response = utils.ReturnEncodingsFromFolder(CompanyName)

        KnownEncodings = response[0]
        ClassNames = response[1]
        facesCurrentFrame = face_recognition.face_locations(img)
        Encode = face_recognition.face_encodings(img, facesCurrentFrame)

        for EncodeFace, Location in zip(Encode, facesCurrentFrame):
            matches = face_recognition.compare_faces(
                KnownEncodings, EncodeFace)
            FaceDistance = face_recognition.face_distance(
                KnownEncodings, EncodeFace)
            matchIndex = np.argmin(FaceDistance)

        if matches[matchIndex]:
            name = ClassNames[matchIndex]
            if "-" in name:
                name = name[0:name.index("-")]

            import datetime
            PATH = f"Companies/{CompanyName}/db.sql"
            mysql = sqlite3.connect(PATH)
            mycursor = mysql.cursor()
            today = datetime.date.today()
            time = datetime.datetime.now().time()
            time = str(time)[:5]
            query = f"insert into '{EMPL_ID}' (DATE,STATUS,TIME) VALUES('{str(today)}', 'PRESENT','{time}')"
            mycursor.execute(query)
            mysql.commit()
            mysql.close()

            PATH = f"Companies/{CompanyName}/"
            li = os.listdir(PATH)
            li.remove("Current")
            li.remove("db.sql")
            for i in li.copy():
                if str(EMPL_ID) in i:
                    pass
                    li.append(os.path.splitext(i)[0])
                    li.remove(i)
                else:
                    li.remove(i)

            last = max(li)
            last = int(last[last.index("-")+1:])
            print(last)
            cv2.imwrite(PATH+EMPL_ID+"-"+str(last+1)+".jpg", img)
            return "PRESENT"


class Temp(Resource):
    def get(self, Email):
        print(Email)
        return [Email]


api.add_resource(
    FirstTime, "/firsttime/<string:CompanyName>/<string:Email>/<path:url>")
api.add_resource(Temp, "/Temp/<path:Email>")
api.add_resource(
    MAIN, "/main/<string:CompanyName>/<path:Email>/<path:url>/")

if __name__ == "__main__":
    app.run(debug=True)
