import sys
import socket
import time
from struct import *
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from PyQt5 import uic
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import protocol
import init
from socketio import *
from parser import *
import database
import sqlite3
import query

class ManagementSystem(QMainWindow):
    def __init__(self):
        super(ManagementSystem, self).__init__()
        uic.loadUi("./UI/management_system.ui", self)
        self.show()

        self.sWidget.setCurrentIndex(7)
        self.pHome.clicked.connect(self.home)
        self.pDetails.clicked.connect(self.details)
        self.pInformation.clicked.connect(self.information)
        self.pSelect.clicked.connect(self.select)

        self.flex_recv_queue = queue.Queue()
        self.flex_send_queue = queue.Queue()
        self.flex_recv_parser = queue.Queue()

        for i in range(1, 4):
            item = "device {}".format(i)
            self.cBox.addItem(item)

        timer_alive = QTimer(self)
        timer_alive.setInterval(60000)
        timer_alive.timeout.connect(self.alive_request)
        timer_alive.start()

        self.th = flex_server_socket(self, self.flex_recv_queue, self.flex_send_queue)
        self.th.start()

        self.r = recv_parser(self, self.flex_recv_queue, self.flex_send_queue, self.flex_recv_parser)
        self.r.start()

        self.socket_send = send_parser(self, self.flex_recv_queue, self.flex_send_queue)

        self.db = database.database(self, self.flex_recv_parser)
        self.db.start()

        print("database started")

    def home(self):
        self.sWidget.setCurrentIndex(7)

    def select(self):
        cboxText = self.cBox.currentText()
        if cboxText == "device 1":
            data = pack("HHBBBBBI", 0x00, 0x0, 0x1, 0, 0, 0, 0, 0)
        elif cboxText == "device 2":
            data = pack("HHBBBBBI", 0x00, 0x0, 0x2, 0, 0, 0, 0, 0)
        elif cboxText == "device 3":
            data = pack("HHBBBBBI", 0x00, 0x0, 0x3, 0, 0, 0, 0, 0)

        self.flex_recv_parser.put(data)

    def information(self):
        self.sWidget.setCurrentIndex(5)

    def details(self):
        self.sWidget.setCurrentIndex(6)


    def alive_request(self):
        self.socket_send.send(protocol.CID_ALIVE_REQ)
        print("send alive request at every 60s")


app = QApplication(sys.argv)
window = ManagementSystem()
app.exec_()






