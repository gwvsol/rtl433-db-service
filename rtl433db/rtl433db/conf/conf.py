import os
import sys
import psycopg2
import sqlalchemy
from pathlib import Path
from shutil import copy as shutil_copy
from configparser import ConfigParser
from sqlalchemy.exc import ProgrammingError, \
                           OperationalError

from rtl433db.log import logging as log


base_dir = Path(__file__).parent.parent.parent
conf_path = base_dir.parent
config_file = 'rtl433db.conf'


if conf_path.as_posix() in sys.executable:
    config = base_dir.parent/config_file
else:
    config = Path(sys.executable).parent
    config = config/config_file
    if not config.exists():
        confbase = base_dir/config_file
        log.info(f'confbase => {confbase.as_posix()}')
        log.info(f'config => {config.as_posix()}')
        shutil_copy(src=confbase.as_posix(), dst=config.as_posix())

conf = ConfigParser()
conf.read(config)

# =====================================================
#
try:
    _postgresql = conf['postgresql']
    postgresql_host = _postgresql.get('postgresql_host')
    postgresql_port = _postgresql.getint('postgresql_port')
    postgresql_user = _postgresql.get('postgresql_user')
    postgresql_password = _postgresql.get('postgresql_password')
    postgresql_dbname = _postgresql.get('postgresql_dbname')
    _postgresql_url = 'postgresql+psycopg2://{}:{}@{}:{}'.format(
            postgresql_user, postgresql_password,
            postgresql_host, postgresql_port
        )
    postgresql_url = '{}/{}'.format(_postgresql_url, postgresql_dbname)
except KeyError as err:
    log.error(f'KeyError => {err}')
    log.error('postgresql error in conf')
    sys.exit(os.EX_SOFTWARE)


try:
    with sqlalchemy.create_engine(
        postgresql_url,
        isolation_level='AUTOCOMMIT'
    ).connect() as connection:
        log.info(f"DATABASE: {postgresql_dbname} => exists")
        log.info(f"POSTGRESQL => {postgresql_url}")
except (psycopg2.OperationalError, OperationalError):
    try:
        with sqlalchemy.create_engine(
            _postgresql_url,
            isolation_level='AUTOCOMMIT'
        ).connect() as connection:
            connection.execute(f"CREATE DATABASE {postgresql_dbname};")
            log.info(f"DATABASE: {postgresql_dbname} => created")
            log.info(f"POSTGRESQL => {postgresql_url}")
    except (ProgrammingError, OperationalError) as err:
        log.error(err)

try:
    _rtl433db = conf['rtl433db']
    rtl433db_log = _rtl433db.getboolean('rtl433db_log')
except KeyError as err:
    log.warn(f'KeyError => {err}')
    rtl433db_log = False


class Rtl433Conf:
    command: str = 'rtl_433 -F json'
    name: str = 'rtl433 process'
    log_out: bool = rtl433db_log


try:
    _weatherapi = conf['weatherapi']
    weatherapi_key = _weatherapi.get('weatherapi_key')
    weatherapi_location = _weatherapi.get('weatherapi_location')
    weatherapi_url = 'https://api.weatherapi.com/v1/current.json'
    weatherapi_lang = 'ru'
    weatherapi_air_quality = 'no'
    weatherapi_timeout = 3
    weatherapi_interval = 300  # интервал запроса погоды в секундах

    # weatherapi_url = "{}?key={}&q={}&aqi={}&lang={}".format(
    #     weatherapi_url, weatherapi_key,
    #     weatherapi_location, weatherapi_air_quality,
    #     weatherapi_lang
    # )

    weatherapi_url = "{}?key={}&q={}&aqi={}".format(
        weatherapi_url, weatherapi_key,
        weatherapi_location, weatherapi_air_quality
    )
except KeyError as err:
    log.error(f'KeyError => {err}')
    log.error('weatherapi error in conf')
    sys.exit(os.EX_SOFTWARE)


class WeatherApiConf:
    url = weatherapi_url
    interval = weatherapi_interval
    timeout = weatherapi_timeout
