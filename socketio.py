import sys
import socket
import time
from struct import *
import numpy as np
import pandas as pd
import cv2
import matplotlib.pyplot as plt
from PyQt5.QtCore import *
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
import protocol

HOST = "localhost"
PORT = 1234

class thread_send(QThread):
    def __init__(self, parent, thread_server):
        super(thread_send, self).__init__()
        self.parent = parent
        self.thread_server = thread_server


    def run(self):
        data = pack("")
        while True:
            self.thread_server.send(data)


class thread_recv(QThread):
    def __init__(self, parent, thread_server):
        super(thread_recv, self).__init__()
        self.parent = parent
        self.thread_server = thread_server

    def run(self):
        while True:
            data = self.thread_server.recv(1056)
            print(data)

class socketio(QThread):
    global HOST
    global PORT
    def __init__(self):
        super(socketio, self).__init__()

    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((HOST, PORT))
        self.server.listen()

        while True:
            self.thread_server, addr = self.server.accept()
            self.th_send = thread_send(self, self.thread_server)
            self.th_send.start()
            self.th_recv = thread_recv(self, self.thread_server)
            self.th_recv.start()