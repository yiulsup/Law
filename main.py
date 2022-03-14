import sys
import socket
from struct import *
import numpy as np
from PyQt5 import uic
from PyQt5.QtWidgets import QApplication, QMainWindow, QDialog
from PyQt5.QtCore import QThread, QTimer, Qt
from PyQt5.QtGui import QImage, QPixmap

class thread_socket_recv(QThread):
    def __init__(self):

class socketIO(QThread):
    def __int__(self, parent):
        super(socketIO, self).__int__()
        self.parent = parent
        self.HOST = "0.0.0.0"
        self.PORT = 1234
    def run(self):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.HOST, self.PORT))
        self.server.listen()
        while True:
            self.server_thread, addr = self.server.accept()
            self.recv = thread_socket_recv()
            self.send = thread_socket_send()
            self.recv.start()
            self.send.start()

class management_system(QMainWindow):
    def __init__(self):
        super(management_system, self).__init__()
        uic.loadUi("./UI/management_system.ui", self)
        self.show()
        self.sWidget.setCurrentIndex(7)

app = QApplication(sys.argv)
window = management_system()
app.exec_()