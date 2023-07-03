# import socket

from rtl433db.log import logging as log
from rtl433db.conf import Rtl433Conf as rtl433_conf
from rtl433db.conf import NarodMonConf as narodmon_conf


def format_data(data: tuple) -> bytes:
    login = narodmon_conf.login
    mac = narodmon_conf.sensor
    name = narodmon_conf.sensor_model
    latitude = narodmon_conf.latitude
    longitude = narodmon_conf.longitude
    
    temperature, humidity, datetime, model = data


# with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
#     s.connect((HOST, PORT))
#     s.sendall(b"Hello, world")
#     data = s.recv(1024)
