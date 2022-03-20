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
import socketio

class recv_parser(QThread):
    def __init__(self, parent, flex_recv_queue, flex_send_queue, flex_recv_parser):
        super(recv_parser, self).__init__()
        self.parent = parent
        self.flex_recv_queue = flex_recv_queue
        self.flex_send_queue = flex_send_queue
        self.flex_recv_parser = flex_recv_parser

    def run(self):
        while True:
            self.parser_data = self.flex_recv_queue.get()
            self.parser(self.parser_data)
            self.flex_recv_parser.put(self.parser_data)

    def parser(self, par_data):
        cid = par_data[0] + par_data[1] * 16 * 16
        self.parser_cid(cid, par_data)

    def parser_cid(self, p_cid, pa_data):
        cid = p_cid
        device_data = pa_data
        if cid == protocol.CID_ALIVE_RES:
            data = unpack(protocol.STRUCT_CID_ALIVE_RES, device_data)
            intID = int(data[2].decode())
            print("alive response : {}".format(intID))
            if intID == 1:
                if data[3] == 1:
                    self.parent.Main_Sys_1.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Main_Sys_1.setStyleSheet("background-color: #FF0000")
                if data[4] == 1:
                    self.parent.Main_Radar_1.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Main_Radar_1.setStyleSheet("background-color: #FF0000")
                if data[5] == 1:
                    self.parent.Sub_Sys_1.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Sub_Sys_1.setStyleSheet("background-color: #FF0000")
                if data[6] == 1:
                    self.parent.Sub_Radar_1.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Sub_Radar_1.setStyleSheet("background-color: #FF0000")
                self.parent.db.insert(protocol.CID_ALIVE_RES, intID, data)
            elif intID == 2:
                if data[3] == 1:
                    self.parent.Main_Sys_2.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Main_Sys_2.setStyleSheet("background-color: #FF0000")
                if data[4] == 1:
                    self.parent.Main_Radar_2.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Main_Radar_2.setStyleSheet("background-color: #FF0000")
                if data[5] == 1:
                    self.parent.Sub_Sys_2.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Sub_Sys_2.setStyleSheet("background-color: #FF0000")
                if data[6] == 1:
                    self.parent.Sub_Radar_2.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Sub_Radar_2.setStyleSheet("background-color: #FF0000")
                    self.parent.db.insert(protocol.CID_ALIVE_RES, intID, data)

        elif cid == protocol.CID_ALIVE_REP:
            data = unpack(protocol.STRUCT_CID_ALIVE_RES, device_data)
            intID = int(data[2].decode())
            print("alive report : {}".format(intID))
            if intID == 1:
                if data[3] == 1:
                    self.parent.Main_Sys_1.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Main_Sys_1.setStyleSheet("background-color: #FF0000")
                if data[4] == 1:
                    self.parent.Main_Radar_1.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Main_Radar_1.setStyleSheet("background-color: #FF0000")
                if data[5] == 1:
                    self.parent.Sub_Sys_1.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Sub_Sys_1.setStyleSheet("background-color: #FF0000")
                if data[6] == 1:
                    self.parent.Sub_Radar_1.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Sub_Radar_1.setStyleSheet("background-color: #FF0000")
            elif intID == 2:
                if data[3] == 1:
                    self.parent.Main_Sys_2.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Main_Sys_2.setStyleSheet("background-color: #FF0000")
                if data[4] == 1:
                    self.parent.Main_Radar_2.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Main_Radar_2.setStyleSheet("background-color: #FF0000")
                if data[5] == 1:
                    self.parent.Sub_Sys_2.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Sub_Sys_2.setStyleSheet("background-color: #FF0000")
                if data[6] == 1:
                    self.parent.Sub_Radar_2.setStyleSheet("background-color: #00FF00")
                else:
                    self.parent.Sub_Radar_2.setStyleSheet("background-color: #FF0000")
                self.parent.db.insert(protocol.CID_ALIVE_REP, intID, data)
        elif cid == protocol.CID_GET_BDINFO_RES:
            print("get board response")
        elif cid == protocol.CID_SET_BDINFO_RES:
            print("set board response")
        elif cid == protocol.CID_GET_PROFILE_RES:
            print("get profile response")
        elif cid == protocol.CID_SET_PROFILE_RES:
            print("set profile response")
        elif cid == protocol.CID_ACQ_DATA_REP:
            data = unpack(protocol.STRUCT_CID_ACQ_DATA_REP, device_data)
            intID = int(data[2].decode())
            print("data report ID : {}".format(intID))
            self.parent.db.insert(protocol.CID_ACQ_DATA_REP, intID, data)
        elif cid == protocol.CID_ALARM_REP:
            print("alarm report")
        elif cid == protocol.CID_RESET_RES:
            print("reset response")
        elif cid == protocol.CID_FW_DL_RES:
            print("firmware download response")
        elif cid == protocol.CID_FW_DL_REP:
            print("firmware download report")
        elif cid == protocol.CID_FW_DATA_RES:
            print("firmware data response")
        elif cid == protocol.CID_SIG_DATA_RES:
            print("signal data response")
        elif cid == protocol.CID_SIG_DATA_REP:
            print("signal data report")
        elif cid == protocol.CID_LOG_START_RES:
            print("log start resposne")
        elif cid == protocol.CID_LOG_DATA_REP:
            print("log data report")
        elif cid == protocol.CID_LOG_END_REP:
            print("log end report")
        elif cid == protocol.CID_GET_WIFIINFO_RES:
            print("get wifi response")
        elif cid == protocol.CID_SET_WIFIINFO_RES:
            print("set wifi response")
        elif cid == protocol.CID_IRDATA_REP:
            print("IR data report")


class send_parser:
    def __init__(self, parent, flex_recv_queue, flex_send_queue):
        super(send_parser, self).__init__()
        self.parent = parent
        self.flex_recv_queue = flex_recv_queue
        self.flex_send_queue = flex_send_queue

    def send(self, data):
        cid = data
        if cid == protocol.CID_ALIVE_REQ:
            print("alive request in parser")
            self.parser_data = protocol.CID_FW_DATA_REQ
        elif cid == protocol.CID_GET_BDINFO_REQ:
            print("get board request")
        elif cid == protocol.CID_SET_BDINFO_REQ:
            print("set board request")
        elif cid == protocol.CID_GET_PROFILE_REQ:
            print("get profile request")
        elif cid == protocol.CID_SET_PROFILE_REQ:
            print("set profile request")
        elif cid == protocol.CID_RESET_REQ:
            print("reset request")
        elif cid == protocol.CID_FW_DL_REQ:
            print("firmware download request")
        elif cid == protocol.CID_FW_DATA_REQ:
            print("firmware data request")
        elif cid == protocol.CID_SIG_DATA_REQ:
            print("signal data request")
        elif cid == protocol.CID_LOG_START_REQ:
            print("log start request")
        elif cid == protocol.CID_GET_WIFIINFO_REQ:
            print("get wifi request")
        elif cid == protocol.CID_SET_WIFIINFO_REQ:
            print("set wifi request")

        self.flex_send_queue.put(self.parser_data)