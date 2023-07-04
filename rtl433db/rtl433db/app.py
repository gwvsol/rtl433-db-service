import time
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue
from apscheduler.schedulers.background import BackgroundScheduler

from rtl433db.weather import wget
from rtl433db.rtl433 import rtl433
from rtl433db.narodmon import send
from rtl433db.log import logging as log
from rtl433db.db import Base, engine, write, sensors
from rtl433db.conf import Rtl433Conf as rtl433_conf
from rtl433db.conf import WeatherApiConf as weathew_conf
from rtl433db.conf import NarodMonConf as narodmon_conf


def run_app():
    """ Старт приложения rtl_433 """
    w_queue = Queue()

    proc = Popen(rtl433_conf.command.split(), stdout=PIPE)
    process = Process(target=rtl433,
                      args=(w_queue, proc),
                      name=rtl433_conf.name)

    if weathew_conf.enable or narodmon_conf.enable:
        scheduler = BackgroundScheduler()
        log.getLogger('apscheduler').propagate = False

    if weathew_conf.enable:
        wget(queue=w_queue)
        scheduler.add_job(wget,
                          'interval',
                          kwargs=dict(queue=w_queue),
                          seconds=weathew_conf.interval)

    if narodmon_conf.enable:
        send(sensors=sensors)
        scheduler.add_job(send,
                          'interval',
                          kwargs=dict(sensors=sensors),
                          seconds=narodmon_conf.interval)

    if weathew_conf.enable or narodmon_conf.enable:
        scheduler.start()

    # создаем таблицы
    Base.metadata.create_all(bind=engine)

    try:
        process.start()
        while True:
            if not w_queue.empty():
                data = w_queue.get_nowait()
                if data == "JSONDecodeError":
                    break
                write(**data)
            time.sleep(1)
        proc.kill()
        proc.communicate()
        process.join()
        log.error("TUNER DVB-T/T2/C FM & DAB => NOT FOUND => STOP")
    except (KeyboardInterrupt, SystemExit):

        if weathew_conf.enable:
            scheduler.shutdown()

        proc.kill()
        proc.communicate()
        process.join()
