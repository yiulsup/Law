import sys
import socket
import time
from struct import *
import numpy as np
import pandas as pd
import cv2
import zlib
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from protocol import *
from struct import *
import queue
from init import *

class flex_server_socket_send_thread(QThread):
    def __init__(self, flex_conn, flex_send_queue):
        super(flex_server_socket_send_thread, self).__init__()
        self.flex_conn = flex_conn
        self.flex_send_queue = flex_send_queue

    def run(self):
        while True:
            self.flex_data = self.flex_send_queue.get()
            if self.flex_data == protocol.CID_ALIVE_REQ:
                self.socket_data = pack(protocol.STRUCT_CID_ALIVE_REQ, 0x102, 16, "0".encode('utf=8'), 1, 1, 1, 1, 24)
                print("alive request sent through socket")
                self.flex_conn.send(self.socket_data)


class flex_server_socket_recv_thread(QThread):
    def __init__(self, parent, flex_conn, flex_recv_queue):
        super(flex_server_socket_recv_thread, self).__init__()
        self.flex_conn = flex_conn
        self.flex_recv_queue = flex_recv_queue
        self.parent = parent
        self.cnt = 0
        self.parent.pDevice_1.setStyleSheet("background-color: #0000FF")
        self.parent.pDevice_2.setStyleSheet("background-color: #0000FF")

    def run(self):
        while True:
            if self.cnt == 20:
                break
            self.flex_data = self.flex_conn.recv(1024)
            if self.flex_data == b'':
                break
            else:
                self.flex_recv_queue.put(self.flex_data)
                self.tempID = unpack("HH12s", self.flex_data[0:16])



        intID = int(self.tempID[2])
        idText = "pDevice_{}".format(intID)
        mainsys = "Main_Sys_{}".format(intID)
        mainradar = "Main_Radar_{}".format(intID)
        subsys = "Sub_Sys_{}".format(intID)
        subradar = "Sub_Radar_{}".format(intID)

        if intID == 1:
            self.parent.pDevice_1.setStyleSheet("background-color: #FF0000")
            self.parent.Main_Sys_1.setStyleSheet("background-color: #FF0000")
            self.parent.Main_Radar_1.setStyleSheet("background-color: #FF0000")
            self.parent.Sub_Sys_1.setStyleSheet("background-color: #FF0000")
            self.parent.Sub_Radar_1.setStyleSheet("background-color: #FF0000")
        elif intID == 2:
            self.parent.pDevice_2.setStyleSheet("background-color: #FF0000")
            self.parent.Main_Sys_2.setStyleSheet("background-color: #FF0000")
            self.parent.Main_Radar_2.setStyleSheet("background-color: #FF0000")
            self.parent.Sub_Sys_2.setStyleSheet("background-color: #FF0000")
            self.parent.Sub_Radar_2.setStyleSheet("background-color: #FF0000")

        self.flex_conn.close()

class flex_server_socket(QThread):
    def __init__(self, parent, flex_recv_queue, flex_send_queue):
        super(flex_server_socket, self).__init__()
        self.flex_recv_queue = flex_recv_queue
        self.flex_send_queue = flex_send_queue
        self.parent = parent
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()

        print("server listen")

    def run(self):
        while True:
            self.flex_conn, addr = self.server.accept()
            self.th_thread_send = flex_server_socket_send_thread(self.flex_conn, self.flex_send_queue)
            self.th_thread_send.start()
            print("thread send start : {}".format(self.th_thread_send))
            self.th_thread_recv = flex_server_socket_recv_thread(self.parent, self.flex_conn, self.flex_recv_queue)
            self.th_thread_recv.start()
            print("thread recv start : {}".format(self.th_thread_recv))