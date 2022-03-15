import sqlite3
import pandas as pd
import cv2
import numpy as np
import sys
import socket
import time
import sqlite3
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import QTimer, QThread
from PyQt5.QtGui import QImage, QPixmap

class dbTest(QMainWindow):
    def __init__(self):
        super(dbTest, self).__init__()
        uic.loadUi("./UI/list.ui", self)
        self.show()
        self.db_init()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.db_timer)
        self.timer.start()

        self.timer1 = QTimer(self)
        self.timer1.setInterval(2000)
        self.timer1.timeout.connect(self.db_timer1)
        self.timer1.start()

        self.var_cnt = 0
        self.var_cnt1 = 0

    def db_init(self):
        self.conn = sqlite3.connect("dbTest.db")
        self.cur = self.conn.cursor()
        self.cur.execute("DROP TABLE vitals")
        self.conn.commit()
        self.conn = sqlite3.connect("dbTest.db")
        self.cur = self.conn.cursor()
        self.cur.execute("CREATE TABLE IF NOT EXISTS vitals (breath real, heart real)")
        self.conn.commit()

    def db_timer(self):
        self.var_cnt = self.var_cnt + 1
        self.var_cnt1 = self.var_cnt1 + 2
        self.var_breath = "{}".format(self.var_cnt)
        self.var_heart = "{}".format(self.var_cnt1)
        sql = "INSERT INTO vitals(breath, heart) VALUES(?, ?)"
        self.cur.execute(sql, (self.var_cnt, self.var_cnt1))
        self.conn.commit()

    def db_timer1(self):
        self.cur.execute("SELECT * FROM vitals")
        rows = self.cur.fetchall()
        cols = [column[0] for column in self.cur.description]

        data_df = pd.DataFrame.from_records(data=rows, columns=cols)
        data_df = data_df + 3
        print(data_df)

app = QApplication(sys.argv)
window = dbTest()
app.exec_()
