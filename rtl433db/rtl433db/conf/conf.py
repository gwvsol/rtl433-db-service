import os
import sys
import psycopg2
import sqlalchemy
from sqlalchemy.exc import ProgrammingError, \
                           OperationalError

from rtl433db.log import logging as log


# =====================================================

on: list = ['on', 'On', 'ON', '1', 'True', 'TRUE', 'true']
log.info(f'Python {sys.version.title()}')

#
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

rtl433db_log = os.getenv('RTL433DB_LOG', default='off')
rtl433db_log = True if rtl433db_log in on else False
log.info(f"RTL433DB_LOG        => {rtl433db_log}")

weatherapi_key = os.getenv('WEATHERAPI_KEY', default=None)
if weatherapi_key is None:
    log.error('WEATHERAPI_KEY ERROR in env')
    sys.exit(os.EX_SOFTWARE)
log.info("WEATHERAPI_KEY      => **********")

weatherapi_location = os.getenv('WEATHERAPI_LOCATION', default=None)
if weatherapi_location is None:
    log.error('WEATHERAPI_LOCATION ERROR in env')
    sys.exit(os.EX_SOFTWARE)
log.info(f"WEATHERAPI_LOCATION => {weatherapi_location}")

weatherapi_url = 'https://api.weatherapi.com/v1/current.json'
# weatherapi_lang = 'ru'
weatherapi_air_quality = 'no'
weatherapi_timeout = 3
weatherapi_interval = 300  # интервал запроса погоды в секундах

# weatherapi_url = "{}?key={}&q={}&aqi={}&lang={}".format(
#     weatherapi_url, weatherapi_key,
#     weatherapi_location, weatherapi_air_quality,
#     weatherapi_lang)

weatherapi_url = "{}?key={}&q={}&aqi={}".format(
    weatherapi_url, weatherapi_key,
    weatherapi_location, weatherapi_air_quality)


class Rtl433Conf:
    command: str = 'rtl_433 -F json'
    name: str = 'rtl433 process'
    log_out: bool = rtl433db_log


class WeatherApiConf:
    url = weatherapi_url
    interval = weatherapi_interval
    timeout = weatherapi_timeout


_postgresql_url = 'postgresql+psycopg2://{}:{}@{}:{}'.format(
            postgresql_user, postgresql_password,
            postgresql_host, postgresql_port
        )
postgresql_url = '{}/{}'.format(_postgresql_url, postgresql_dbname)


try:
    with sqlalchemy.create_engine(
        postgresql_url,
        isolation_level='AUTOCOMMIT'
    ).connect() as connection:
        log.info(f"DATABASE: {postgresql_dbname}  => exists")
        log.info(f"POSTGRESQL          => {postgresql_url}")
except (psycopg2.OperationalError, OperationalError):
    try:
        with sqlalchemy.create_engine(
            _postgresql_url,
            isolation_level='AUTOCOMMIT'
        ).connect() as connection:
            connection.execute(f"CREATE DATABASE {postgresql_dbname};")
            log.info(f"DATABASE: {postgresql_dbname}  => created")
            log.info(f"POSTGRESQL          => {postgresql_url}")
    except (ProgrammingError, OperationalError) as err:
        log.error(err)
        sys.exit(os.EX_SOFTWARE)
