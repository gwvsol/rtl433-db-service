import os
import sys
import copy
import psycopg2
import sqlalchemy
from sqlalchemy.exc import ProgrammingError, \
                           OperationalError

from rtl433db.log import logging as log


# =====================================================

on: list = ['on', 'On', 'ON', '1', 'True', 'TRUE', 'true']
log.info(f'Python {sys.version.title()}')

# =====================================================

postgresql_host = os.getenv('POSTGRESQL_HOST', default=None)
if postgresql_host is None:
    log.error('POSTGRESQL_HOST ERROR in env')
    sys.exit(os.EX_SOFTWARE)
log.info(f"POSTGRESQL_HOST     => {postgresql_host}")

postgresql_port = os.getenv('POSTGRESQL_PORT', default=None)
if postgresql_port and postgresql_port.isdigit():
    postgresql_port = int(postgresql_port)
else:
    log.error('POSTGRESQL_PORT ERROR in env')
    sys.exit(os.EX_SOFTWARE)
log.info(f"POSTGRESQL_PORT     => {postgresql_port}")

postgresql_user = os.getenv('POSTGRESQL_USER', default=None)
if postgresql_user is None:
    log.error('POSTGRESQL_USER ERROR in env')
    sys.exit(os.EX_SOFTWARE)
log.info(f"POSTGRESQL_USER     => {postgresql_user}")

postgresql_password = os.getenv('POSTGRESQL_PASSWORD', default=None)
if postgresql_password is None:
    log.error('POSTGRESQL_PASSWORD ERROR in env')
    sys.exit(os.EX_SOFTWARE)
log.info("POSTGRESQL_PASSWORD => **********")

postgresql_dbname = os.getenv('POSTGRESQL_DBNAME', default=None)
if postgresql_dbname is None:
    log.error('POSTGRESQL_DBNAME ERROR in env')
    sys.exit(os.EX_SOFTWARE)
log.info(f"POSTGRESQL_DBNAME   => {postgresql_dbname}")

# =====================================================

rtl433db_log = os.getenv('RTL433DB_LOG', default='off')
rtl433db_log = True if rtl433db_log in on else False
log.info(f"RTL433DB_LOG        => {rtl433db_log}")

# =====================================================

weatherapi_key = os.getenv('WEATHERAPI_KEY', default=None)
if weatherapi_key is None:
    log.warning('WEATHERAPI       => DISABLE')
else:
    log.info("WEATHERAPI_KEY      => **********")

weatherapi_location = os.getenv('WEATHERAPI_LOCATION', default=None)
if weatherapi_key and weatherapi_location is None:
    log.warning('WEATHERAPI       => DISABLE')
else:
    if weatherapi_key:
        log.info(f"WEATHERAPI_LOCATION => {weatherapi_location}")

weatherapi_url = 'https://api.weatherapi.com/v1/current.json'
# weatherapi_lang = 'ru'
weatherapi_air_quality = 'no'

# weatherapi_url = "{}?key={}&q={}&aqi={}&lang={}".format(
#     weatherapi_url, weatherapi_key,
#     weatherapi_location, weatherapi_air_quality,
#     weatherapi_lang)

weatherapi_url = "{}?key={}&q={}&aqi={}".format(
    weatherapi_url, weatherapi_key,
    weatherapi_location, weatherapi_air_quality)

weatherapi_enable = True if weatherapi_key and weatherapi_location else False

# =====================================================

narodmon_host = os.getenv('NARODMON_HOST', default=None)
if narodmon_host is None:
    log.warning('NARODMON         => DISABLE')
else:
    log.info(f"NARODMON_HOST       => {narodmon_host}")

narodmon_port = os.getenv('NARODMON_PORT', default=None)
if narodmon_host and narodmon_port is None:
    log.warning('NARODMON         => DISABLE')
else:
    if narodmon_port and narodmon_port.isdigit():
        narodmon_port = int(narodmon_port)
        log.info(f"NARODMON_PORT       => {narodmon_port}")
    else:
        narodmon_port = None

narodmon_enable = True if narodmon_host and narodmon_port else False

narodmon_login = os.getenv('NARODMON_LOGIN', default=None)
if narodmon_enable and narodmon_login is None:
    log.error('NARODMON_LOGIN ERROR in env')
    sys.exit(os.EX_SOFTWARE)
else:
    log.info(f"NARODMON_LOGIN      => {narodmon_login}")

narodmon_sensor = os.getenv('NARODMON_SENSOR', default=None)
if narodmon_enable and narodmon_sensor is None:
    log.error('NARODMON_SENSOR ERROR in env')
    sys.exit(os.EX_SOFTWARE)
else:
    log.info(f"NARODMON_SENSOR     => {narodmon_sensor}")

narodmon_sensor_model = os.getenv('NARODMON_SENSOR_MODEL', default=None)
if narodmon_enable and narodmon_sensor_model is None:
    log.error('NARODMON_SENSOR_MODEL ERROR in env')
    sys.exit(os.EX_SOFTWARE)
else:
    log.info(f"NARODMON_SENSOR_MODEL => {narodmon_sensor_model}")

narodmon_sensor_latitude = os.getenv('NARODMON_SENSOR_LATITUDE',
                                     default=None)
if narodmon_enable:
    log.info(f"NARODMON_SENSOR_LATITUDE => {narodmon_sensor_latitude}")

narodmon_sensor_longitude = os.getenv('NARODMON_SENSOR_LONGITUDE',
                                      default=None)
if narodmon_enable and narodmon_sensor_longitude:
    log.info(f"NARODMON_SENSOR_LONGITUDE => {narodmon_sensor_longitude}")

# =====================================================


class Rtl433Conf:
    command: str = 'rtl_433 -F json'
    name: str = 'rtl433 process'
    log_out: bool = rtl433db_log


class WeatherApiConf:
    url: str = weatherapi_url
    api_key: str = weatherapi_key
    # интервал запроса погоды в секундах
    interval: int = 300
    timeout: int = 3
    enable: bool = weatherapi_enable


class NarodMonConf:
    host: str = narodmon_host
    port: int = narodmon_port
    login: str = narodmon_login
    # интервал отправки данных в секундах
    # interval: int = 180
    interval: int = 10
    enable: bool = narodmon_enable
    sensor: str = narodmon_sensor
    sensor_model: str = narodmon_sensor_model
    latitude: str = narodmon_sensor_latitude
    longitude: str = narodmon_sensor_longitude


# =====================================================


_postgresql_url = 'postgresql+psycopg2://{}:{}@{}:{}'.format(
            postgresql_user, postgresql_password,
            postgresql_host, postgresql_port
        )
postgresql_url = '{}/{}'.format(_postgresql_url, postgresql_dbname)


try:
    db_log_url = copy.deepcopy(
        postgresql_url).replace(postgresql_password, '**********')
    log.info(f"POSTGRESQL          => {db_log_url}")
    with sqlalchemy.create_engine(
        postgresql_url,
        isolation_level='AUTOCOMMIT'
    ).connect() as connection:
        log.info(f"DATABASE: {postgresql_dbname}  => exists")
except (psycopg2.OperationalError, OperationalError):
    try:
        with sqlalchemy.create_engine(
            _postgresql_url,
            isolation_level='AUTOCOMMIT'
        ).connect() as connection:
            connection.execute(f"CREATE DATABASE {postgresql_dbname};")
            log.info(f"DATABASE: {postgresql_dbname}  => created")
    except (ProgrammingError, OperationalError) as err:
        log.error(err)
        sys.exit(os.EX_SOFTWARE)


# =====================================================
