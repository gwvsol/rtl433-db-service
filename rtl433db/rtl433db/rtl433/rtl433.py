import time
import json
from json.decoder import JSONDecodeError
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue

from rtl433db.conf import rtl433_command as command
from rtl433db.log import logging as log


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

    try:
        process.start()
        log.info(" => start")
        while True:
            if not queue.empty():
                data = queue.get_nowait()
                log.info(f"<= {data}")
                if data == "JSONDecodeError":
                    break
            time.sleep(1)
        proc.kill()
        proc.communicate()
        process.join() # 
        log.error("TUNER DVB-T/T2/C FM & DAB => NOT FOUND => STOP")
    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()
        process.join()
