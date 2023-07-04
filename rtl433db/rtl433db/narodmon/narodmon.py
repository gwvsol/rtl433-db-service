import socket

from rtl433db.log import logging as log
from rtl433db.conf import Rtl433Conf as rtl433_conf
from rtl433db.conf import NarodMonConf as narodmon_conf


def format_data(data: tuple) -> bytes:

    TEMP, HUM, DTIME, NAME = data

    if TEMP is None or DTIME is None or NAME is None:
        return

    MAC = narodmon_conf.sensor
    OWNER = narodmon_conf.login
    LAT = narodmon_conf.lat
    LONG = narodmon_conf.long
    TIME: int = int(round(DTIME.timestamp()))

    DATA: str = "#{}#{}\n#OWNER#{}\n".format(MAC, NAME, OWNER)

    if LAT and LONG:
        DATA: str = "{}#LAT#{}\n#LON#{}\n".format(DATA, LAT, LONG)

    if TEMP:
        DATA: str = "{}#TEMP1#{}#{}#OUTDOOR\n".format(DATA, TEMP, TIME)

    if HUM:
        DATA: str = "{}#HUM1#{}#{}#OUTDOOR\n".format(DATA, HUM, TIME)

    DATA: str = "{}##".format(DATA)

    if TIME:
        return bytes(DATA, 'utf-8')
    else:
        return


def send(sensors):
    """ Отправка данных в сервис мониторинга NarodMon """

    data = format_data(sensors(model=narodmon_conf.sensor_model))

    recv = b'ERROR'

    if data:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:

                s.connect((narodmon_conf.host, narodmon_conf.port))
                s.send(data)

                recv = s.recv(1024)
        except ConnectionRefusedError as err:
            log.error("error => {}".format(err))

    if rtl433_conf.log_out:
        if data:
            log.info("=>\n{}".format(data.decode()))
        if recv != b'OK\n':
            log.info("<= {}".format(recv.decode()))
