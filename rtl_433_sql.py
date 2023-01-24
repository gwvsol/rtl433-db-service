import time
import json
import logging as log
from subprocess import Popen, PIPE
from multiprocessing import Process, Queue

command = 'rtl_433 -F json'

log_format = '%(asctime)s.%(msecs)d|%(levelname)s\
|%(module)s.%(funcName)s:%(lineno)d %(message)s'


log.basicConfig(level=log.INFO,
                format=log_format,
                datefmt='%Y-%m-%d %H:%M:%S')


def rtl433(queue: Queue, proc: Popen):
    """ Чтения данных с Astrometa DVB-T/T2/C FM & DAB """
    log.info("=> start")
    try:
        while True:
            line: bytes = proc.stdout.readline()
            rtl433_data = json.loads(line.decode('utf-8'))
            queue.put(rtl433_data)
            # log.info(f"queue => {rtl433_data}")
            time.sleep(1)
    except KeyboardInterrupt:
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
            time.sleep(1)

    except KeyboardInterrupt:
        proc.kill()
        proc.communicate()
        process.join()


if __name__ == "__main__":
    main()
