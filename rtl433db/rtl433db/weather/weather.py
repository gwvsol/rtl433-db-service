from requests import Session
from requests.exceptions import ConnectionError, \
                                ReadTimeout, \
                                InvalidSchema, \
                                JSONDecodeError
from multiprocessing import Queue

from rtl433db.log import logging as log
from rtl433db.conf import WeatherApiConf as conf
from rtl433db.conf import Rtl433Conf as rtl433_conf
from rtl433db.schemas import WeatherSchema


def wget(queue: Queue) -> tuple:
    """ Получение данных c WeatherAPI """
    status_code, weather = 500, dict(weather=dict())
    try:
        with Session() as session:
            resp = session.get(conf.url, timeout=conf.timeout)
            status_code, weather = resp.status_code, resp.json()
            if rtl433_conf.log_out:
                log.info(f" <= {weather} <= {status_code}")
            if status_code == 200:
                weather = WeatherSchema().validate(weather)
                queue.put(dict(weather=weather))
    except (ConnectionError, ReadTimeout,
            InvalidSchema, JSONDecodeError) as err:
        log.error(f"error => {err}")
    finally:
        return weather, status_code
