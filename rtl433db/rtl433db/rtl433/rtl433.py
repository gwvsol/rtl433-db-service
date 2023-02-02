import time
import json
from functools import wraps
from subprocess import Popen, PIPE
from sqlalchemy.orm import Session
from json.decoder import JSONDecodeError
from multiprocessing import Process, Queue
from apscheduler.schedulers.background import BackgroundScheduler

from rtl433db.conf import rtl433_command as command
from rtl433db.conf import WeatherApiConf as weathew_conf
from rtl433db.log import logging as log
from rtl433db.db import Base, Sensors, Temperature, engine
from rtl433db.weather import weatherapi


def format_data_temp(fun):
    """ Декоратор для форматирования данных """
    @wraps(fun)
    def decorator(*args, **kwargs):
        data = kwargs.pop('data', dict())
        kwargs.update(model=data.get('model', None),
                      datetime=data.get('time', None),
                      temp=data.get('temperature_C', None),
                      sensor_id=data.get('id', None))
        return fun(*args, **kwargs)
    return decorator


@format_data_temp
def add_data(model: str = None,
             datetime: str = None,
             temp: str = None,
             sensor_id: str = None,
             data: dict = dict()):
    """ Запись данных в базу данных """

    with Session(autoflush=False, bind=engine) as db:

        sensor = db.query(Sensors).filter(Sensors.model == model).first()

        if sensor and isinstance(temp, (int, float)):
            sensor_id = sensor.id
            temperature = Temperature(sensor_id=sensor.id,
                                      temperature=temp,
                                      datetime=datetime)
            db.add(temperature)
            db.commit()

        elif sensor is None:
            if model and isinstance(sensor_id, (int, str)):
                new_sensor = dict(model=model, sensor_id=str(sensor_id))
                if datetime:
                    new_sensor.update(datetime=datetime)
                new_sensor = Sensors(**new_sensor)
                db.add(new_sensor)
                db.commit()

        else:
            pass


def rtl433(queue: Queue, proc: Popen):
    """ Чтения данных с Astrometa DVB-T/T2/C FM & DAB """
    log.info("=> start")
    try:
        while True:
            line: bytes = proc.stdout.readline()
            rtl433_data = json.loads(line.decode('utf-8'))
            queue.put(rtl433_data)
            time.sleep(1)
    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()
    except JSONDecodeError as err:
        log.error(f"error => {err}")
        queue.put("JSONDecodeError")
        proc.kill()
        proc.communicate()


def main():
    """ Старт приложения rtl_433 """

    scheduler = BackgroundScheduler()
    log.getLogger('apscheduler').propagate = False

    queue = Queue()
    proc = Popen(command.split(), stdout=PIPE)

    process = Process(target=rtl433,
                      args=(queue, proc),
                      name='rtl433 process')

    scheduler.add_job(weatherapi,
                      'interval',
                      seconds=weathew_conf.interval)
    scheduler.start()

    # создаем таблицы
    Base.metadata.create_all(bind=engine)

    try:
        process.start()
        log.info(" => start")
        while True:
            if not queue.empty():
                data = queue.get_nowait()
                log.info(f"<= {data}")
                if data == "JSONDecodeError":
                    break
                add_data(data=data)
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
