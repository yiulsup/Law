import protocol
from struct import *
import zlib
import numpy as np

HOST = "172.30.1.4"
PORT = 9000

ALIVE_REQ = []

def init_ALIVE_REQ():
    protocol.LENGTH = 32
    protocol.MainSys = 0
    protocol.MainRadar = 0
    protocol.SubSys = 0
    protocol.SubRadar = 0

    for i in range(0, 60):
        protocol.ID = "{}".format(i).encode('utf-8')
        data_without_crc = pack(protocol.BEFORE_STRUCT_CID_ALIVE_REQ, protocol.CID_ALIVE_REQ, protocol.LENGTH, protocol.ID,
                                protocol.MainSys, protocol.MainRadar, protocol.SubSys, protocol.SubRadar)
        protocol.CRC32 = zlib.crc32(data_without_crc) & 0xffffffff
        ALIVE_REQ.append(pack(protocol.STRUCT_CID_ALIVE_REQ, protocol.CID_ALIVE_REQ, protocol.LENGTH, protocol.ID,
                                  protocol.MainSys, protocol.MainRadar, protocol.SubSys, protocol.SubRadar, protocol.CRC32))

ALIVE_RES = []

def init_ALIVE_RES():
    for i in range(0, 60):
        protocol.LENGTH = 32
        protocol.MainSys = 1
        protocol.MainRadar = 1
        protocol.SubSys = 1
        protocol.SubRadar = 1

        protocol.ID = "{}".format(i).encode('utf-8')
        data_without_crc = pack(protocol.BEFORE_STRUCT_CID_ALIVE_RES, protocol.CID_ALIVE_RES, protocol.LENGTH, protocol.ID,
                                protocol.MainSys, protocol.MainRadar, protocol.SubSys, protocol.SubRadar)
        protocol.CRC32 = zlib.crc32(data_without_crc) & 0xffffffff
        ALIVE_RES.append(pack(protocol.STRUCT_CID_ALIVE_RES, protocol.CID_ALIVE_RES, protocol.LENGTH, protocol.ID,
                                  protocol.MainSys, protocol.MainRadar, protocol.SubSys, protocol.SubRadar, protocol.CRC32))
