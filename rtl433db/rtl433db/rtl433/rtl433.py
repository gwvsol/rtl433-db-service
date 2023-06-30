import time
import json
import copy
from subprocess import Popen
from multiprocessing import Queue
from json.decoder import JSONDecodeError

from rtl433db.log import logging as log
from rtl433db.conf import Rtl433Conf as rtl433_conf


def rtl433(queue: Queue, proc: Popen):
    """ Чтения данных с Astrometa DVB-T/T2/C FM & DAB """
    from rtl433db.schemas import SensorSchema
    sensor = SensorSchema()
    data_: dict = dict()
    try:
        while True:
            line: bytes = proc.stdout.readline()
            rtl433_data = json.loads(line.decode('utf-8'))
            data = dict(sensor=sensor.validate(rtl433_data))
            if data != data_:
                if rtl433_conf.log_out:
                    log.info(f"<= {rtl433_data}")
                queue.put(data)
                data_ = copy.deepcopy(data)
            time.sleep(1)
    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()
    except JSONDecodeError as err:
        log.error(f"error => {err}")
        queue.put("JSONDecodeError")
        proc.kill()
        proc.communicate()
