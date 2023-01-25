from os import getenv
from pathlib import Path
from configparser import ConfigParser
from rtl433db.log import logging as log


class ConfigError(Exception):
    pass


config = ConfigParser()

BASE_PATH = Path(__file__).parent.parent.parent
CONF_PATH = BASE_PATH.parent

on = ['on', 'On', 'ON', '1', 'True', 'TRUE', 'true']
off = ['NONE', 'None', 'none', 'OFF', 'Off',
       'off', 'False', 'FALSE', 'false', '0']

# =====================================================
#
RTL433DB_NAME = getenv('RTL433DB', default=None)
if RTL433DB_NAME is None:
    raise ConfigError('RTL433DB ERROR in env')

#
RTL433DB_CONFIG = getenv('RTL433DB_CONFIG', default=None)
if RTL433DB_CONFIG is None:
    raise ConfigError('RTL433DB_CONFIG ERROR in env')

# =====================================================
#

POSTGRESQL_HOST = getenv('POSTGRESQL_HOST', default=None)
if POSTGRESQL_HOST is None:
    raise ConfigError('POSTGRESQL_HOST ERROR in env')

POSTGRESQL_PORT = getenv('POSTGRESQL_PORT', default=None)
if POSTGRESQL_PORT.isdigit():
    POSTGRESQL_PORT = int(POSTGRESQL_PORT)
else:
    raise ConfigError('POSTGRESQL_PORT ERROR in env')

POSTGRESQL_USER = getenv('POSTGRESQL_USER', default=None)
if POSTGRESQL_USER is None:
    raise ConfigError('POSTGRESQL_USER ERROR in env')

POSTGRESQL_PASSWORD = getenv('POSTGRESQL_PASSWORD', default=None)
if POSTGRESQL_PASSWORD is None:
    raise ConfigError('POSTGRESQL_PASSWORD ERROR in env')

POSTGRESQL_DBNAME = getenv('POSTGRESQL_DBNAME', default=None)
if POSTGRESQL_DBNAME is None:
    raise ConfigError('POSTGRESQL_DBNAME ERROR in env')


config['POSTGRESQL'] = {
    'POSTGRESQL_HOST': POSTGRESQL_HOST,
    'POSTGRESQL_PORT': POSTGRESQL_PORT,
    'POSTGRESQL_USER': POSTGRESQL_USER,
    'POSTGRESQL_PASSWORD': POSTGRESQL_PASSWORD,
    'POSTGRESQL_DBNAME': POSTGRESQL_DBNAME
    }

#
# =====================================================
#


def saveconfig():
    """ Сохраняем настройки в файл """
    RTL433DB_PATH = CONF_PATH/f'{RTL433DB_CONFIG}'
    with open(RTL433DB_PATH.as_posix(), 'w') as configfile:
        config.write(configfile)

    log.info(f"=> {RTL433DB_PATH.as_posix()}")

# =====================================================
