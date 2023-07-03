from sqlalchemy.orm import Session

from rtl433db.log import logging as log
from rtl433db.conf import Rtl433Conf as rtl433_conf
from rtl433db.db import Sensors, Temperature, Weather, \
                        WeatherLocation, engine


def write(sensor: dict = None, weather: dict = None):
    """ Запись данных в базу данных """

    with Session(autoflush=False, bind=engine) as db:

        if sensor:
            data: dict = sensor.get('sensor')

            if rtl433_conf.log_out and data:
                log.info("     => {}".format(data))

            model = data.get('model')
            _sensor = db.query(Sensors).filter(
                Sensors.model == model).first()

            datetime = data.get('datetime')

            if _sensor and isinstance(
                    data.get('data', dict).get('temperature'),
                    (int, float)):
                db.add(Temperature(sensor_id=_sensor.id,
                                   datetime=datetime,
                                   **data.get('data')))
                db.commit()

            elif _sensor is None:
                db.add(Sensors(model=model,
                               datetime=datetime,
                               sensor_id=data.get('sensor_id')))
                db.commit()

        if weather:
            data: dict = weather.get('weather')

            if rtl433_conf.log_out and data:
                log.info("     => {}".format(data))

            weatherlocation = db.query(WeatherLocation).filter(
                WeatherLocation.location == data.get('name')).first()

            if weatherlocation and isinstance(data, dict):
                db.add(Weather(location=weatherlocation.id,
                               **data.get('weather')))
                db.commit()

            elif weatherlocation is None:
                db.add(WeatherLocation(**data.get('location')))
                db.commit()


def sensors(model: str) -> tuple:
    """ Получение последних данных внешнего
        сенсора погоды из базы данных
        return (temperature, humidity, datetime, model)"""

    response = (None, None, None, None)
    with Session(autoflush=False, bind=engine) as db:
        resp = db.query(
            Temperature.temperature,
            Temperature.humidity,
            Temperature.datetime,
            Sensors.model).join(
                Sensors, Temperature.sensor_id == Sensors.id).filter(
                    Sensors.model == model).order_by(
                        Temperature.datetime.desc()).first()
        response = resp if resp else response

    return response
