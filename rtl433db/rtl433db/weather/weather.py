from requests import Session
from requests.exceptions import ConnectionError, \
                                ReadTimeout, \
                                InvalidSchema, \
                                JSONDecodeError

from rtl433db.log import logging as log
from rtl433db.conf import WeatherApiConf as conf


def weatherapi() -> tuple:
    """ Получение данных c WeatherAPI """
    status_code, data = 500, dict()
    try:
        with Session() as session:
            resp = session.get(conf.url, timeout=conf.timeout)
            status_code, data = resp.status_code, resp.json()
            log.info(f"{weatherapi.__name__} => {data} <= {status_code}")
    except (ConnectionError, ReadTimeout,
            InvalidSchema, JSONDecodeError) as err:
        log.error(f"error => {err}")
    finally:
        return data, status_code
