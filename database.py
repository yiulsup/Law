import sqlite3
import pandas as pd
import cv2
import numpy as np
import sys
import socket
import time
import datetime
import sqlite3
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QImage, QPixmap
import query
import protocol
from struct import *

class database(QThread):
    def __init__(self, parent, flex_recv_parser):
        super(database, self).__init__()
        self.flex_recv_parser = flex_recv_parser
        self.parent = parent
    def run(self):
        self.conn = sqlite3.connect("dbTest.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE alive")
        self.conn.commit()
        self.cur.execute("DROP TABLE acq_data")
        self.conn.commit()
        self.conn = sqlite3.connect("dbTest.db", check_same_thread=False)
        self.cur = self.conn.cursor()
        self.cur.execute(query.sql_alive_create)
        self.conn.commit()
        self.cur.execute(query.sql_acq_data_create)
        self.conn.commit()
        while True:
            self.data = self.flex_recv_parser.get()
            cid = self.data[0] + self.data[1] * 256
            if cid == 258 or cid == 260:
                data = unpack(protocol.STRUCT_CID_ALIVE_RES, self.data)
                intID = int(data[2].decode())
                self.insert(cid, intID, data)
            elif cid == 0x1104:
                data = unpack(protocol.STRUCT_CID_ACQ_DATA_REP, self.data)
                intID = int(data[2].decode())
                self.insert(cid, intID, data)
            elif cid == 0000:
                data = unpack("HHBBBBBI", self.data)
                self.fetch()


    def insert(self, device_cid, device_id, data):
        db_device_id = device_id
        db_device_cid = device_cid
        db_device_data = data

        print("database : id : {}, cid : {}, data : {}".format(db_device_id, db_device_cid, db_device_data))
        ct = datetime.datetime.now()
        if db_device_cid == 260 or db_device_cid == 258:
            self.cur.execute(query.sql_alive_insert, (ct, db_device_id, db_device_data[3], db_device_data[4], db_device_data[5], db_device_data[6]))
            self.conn.commit()
        elif db_device_cid == 0x1104:
            self.cur.execute(query.sql_acq_data_insert, (ct, db_device_id, db_device_data[8], db_device_data[9], db_device_data[10], db_device_data[11], db_device_data[12], db_device_data[13], db_device_data[14], db_device_data[15], db_device_data[16], db_device_data[17], db_device_data[18], db_device_data[19], db_device_data[20], db_device_data[21], db_device_data[22], db_device_data[23], db_device_data[24], db_device_data[25], db_device_data[26]))
            self.conn.commit()

    def fetch(self):
        self.cur.execute(query.sql_acq_data_fetch)
        rows = self.cur.fetchall()
        cols = [column[0] for column in self.cur.description]
        data_df = pd.DataFrame.from_records(data=rows, columns=cols)
        self.db_data = data_df.to_numpy()
        data_df.to_csv("1.csv")
        plt.plot(data_df['heart_0'])
        plt.savefig("1.png")
        plt.cla()
        plt.plot(data_df['breath_0'])
        plt.savefig("2.png")
        plt.cla()
        self.parent.viewBreath.setPixmap(QPixmap("2.png"))
        self.parent.viewBreath.setScaledContents(1)
        self.parent.viewBreath.show()
        self.parent.viewHeart.setPixmap(QPixmap("1.png"))
        self.parent.viewHeart.setScaledContents(1)
        self.parent.viewHeart.show()
