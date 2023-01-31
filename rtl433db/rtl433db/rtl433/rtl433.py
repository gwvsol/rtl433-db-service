import time
import json
from json.decoder import JSONDecodeError
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue
from sqlalchemy.orm import Session

from rtl433db.conf import rtl433_command as command
from rtl433db.log import logging as log

from rtl433db.db import Base, Sensors, Temperature, engine


def add_data(data: dict):
    """ Запись данных в базу данных """

    model = data.get('model', None)
    datetime = data.get('time', None)
    temp = data.get('temperature_C', None)
    sensor_id = data.get('id', None)

    with Session(autoflush=False, bind=engine) as db:
        sensor = db.query(Sensors).filter(Sensors.model == model).first()

        if sensor and isinstance(temp, int):
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

    queue = Queue()
    proc = Popen(command.split(), stdout=PIPE)

    process = Process(target=rtl433,
                      args=(queue, proc),
                      name='rtl433 process')

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
                add_data(data)
            time.sleep(1)
        proc.kill()
        proc.communicate()
        process.join() # 
        log.error("TUNER DVB-T/T2/C FM & DAB => NOT FOUND => STOP")
    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()
        process.join()
