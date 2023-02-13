import time
import json
from functools import wraps
from subprocess import Popen, PIPE
from sqlalchemy.orm import Session
from json.decoder import JSONDecodeError
from multiprocessing import Process, Queue
from apscheduler.schedulers.background import BackgroundScheduler

from rtl433db.conf import Rtl433Conf as rtl433_conf
from rtl433db.conf import WeatherApiConf as weathew_conf
from rtl433db.log import logging as log
from rtl433db.db import Base, Sensors, Temperature, \
                        Weather, WeatherLocation, engine
from rtl433db.weather import weatherapi


def format_data_temp(fun):
    """ Декоратор для форматирования данных """
    @wraps(fun)
    def decorator(*args, **kwargs):
        data: dict = kwargs.get('data', None)
        if isinstance(data, dict):
            if data.get('sensor', None):
                kwargs = data.pop('sensor')
            if data.get('weather', None):
                kwargs = data.pop('weather')
        return fun(*args, **kwargs)
    return decorator


@format_data_temp
def add_data(sensor: dict = None,
             weather: dict = None,
             data: dict = dict()):
    """ Запись данных в базу данных """

    with Session(autoflush=False, bind=engine) as db:

        if sensor:
            _sensor = db.query(Sensors).filter(
                Sensors.model == sensor.get('model')).first()

            if _sensor and isinstance(sensor.get('sensor_data'), dict):
                db.add(Temperature(sensor_id=_sensor.id,
                                   **sensor.get('sensor_data')))
                db.commit()

            elif _sensor is None:
                db.add(Sensors(**sensor.get('sensor')))
                db.commit()

            else:
                pass

        if weather:
            weatherlocation = db.query(WeatherLocation).filter(
                WeatherLocation.location == weather.get('name')).first()

            if weatherlocation and isinstance(weather.get('weather'), dict):
                db.add(Weather(location=weatherlocation.id,
                               **weather.get('weather')))
                db.commit()

            elif weatherlocation is None:
                db.add(WeatherLocation(**weather.get('location')))
                db.commit()

            else:
                pass


def rtl433(queue: Queue, proc: Popen):
    """ Чтения данных с Astrometa DVB-T/T2/C FM & DAB """
    from rtl433db.schemas import SensorSchema
    log.info("=> start")
    sensor = SensorSchema()
    try:
        while True:
            line: bytes = proc.stdout.readline()
            rtl433_data = json.loads(line.decode('utf-8'))
            queue.put(dict(sensor=sensor.validate(rtl433_data)))
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

    w_queue = Queue()

    weatherapi(queue=w_queue)

    scheduler = BackgroundScheduler()
    log.getLogger('apscheduler').propagate = False

    proc = Popen(rtl433_conf.command.split(), stdout=PIPE)

    process = Process(target=rtl433,
                      args=(w_queue, proc),
                      name=rtl433_conf.name)

    scheduler.add_job(weatherapi,
                      'interval',
                      kwargs=dict(queue=w_queue),
                      seconds=weathew_conf.interval)
    scheduler.start()

    # создаем таблицы
    Base.metadata.create_all(bind=engine)

    try:
        process.start()
        log.info(" => start")
        while True:
            if not w_queue.empty():
                data = w_queue.get_nowait()
                if rtl433_conf.log_out:
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
