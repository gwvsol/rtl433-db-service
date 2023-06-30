import time
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue
from apscheduler.schedulers.background import BackgroundScheduler

from rtl433db.weather import wget
from rtl433db.rtl433 import rtl433
from rtl433db.log import logging as log
from rtl433db.db import Base, engine, write
from rtl433db.conf import Rtl433Conf as rtl433_conf
from rtl433db.conf import WeatherApiConf as weathew_conf


def run_app():
    """ Старт приложения rtl_433 """
    w_queue = Queue()
    wget(queue=w_queue)

    scheduler = BackgroundScheduler()
    log.getLogger('apscheduler').propagate = False

    proc = Popen(rtl433_conf.command.split(), stdout=PIPE)
    process = Process(target=rtl433,
                      args=(w_queue, proc),
                      name=rtl433_conf.name)

    scheduler.add_job(wget,
                      'interval',
                      kwargs=dict(queue=w_queue),
                      seconds=weathew_conf.interval)
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
        scheduler.shutdown()
        proc.kill()
        proc.communicate()
        process.join()
