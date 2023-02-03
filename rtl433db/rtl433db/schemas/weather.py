from datetime import datetime

from .base import JSONSchema


class WeatherSchemaBase(JSONSchema):
    """ Базовый валидатор данных Weather Schema """

    schema = {
        "type": "object",
        "properties": {
            "location": {"type": "object",
                         "properties": {
                             "name": {"type": "string"},
                             "country": {"type": "string"},
                             "lat": {"type": "number"},
                             "lon": {"type": "number"},
                            }
                         },
            "current": {"type": "object",
                        "properties": {
                             "temp_c": {"type": "number"}
                            }
                        }
            }
        }


class WeatherSchema:
    """ Валидатор данных Weather Schema """

    def __init__(self):
        self.structure = WeatherSchemaBase()

    def validate(self, data) -> dict:
        """ Валидатор и формирование выходных данных """
        appstruct = self.structure.validate(data)
        return self.create_fields(appstruct)

    def create_fields(self, appstruct: dict) -> dict:
        """ Создание структуры данных """
        location: dict = appstruct.get('location', dict())
        current: dict = appstruct.get('current', dict())

        pressure_mb = current.get('pressure_mb', None)
        if isinstance(pressure_mb, (int, float)):
            pressure_mmhg = pressure_mb * 0.750062
        else:
            pressure_mmhg = None

        new = dict(name=location.get('name', '').lower(),
                   location=dict(
                       location=location.get('name', '').lower(),
                       country=location.get('country', '').lower(),
                       lat=location.get('lat', 0.0),
                       lon=location.get('lon', 0.0),
                       datetime=location.get('localtime', datetime.now())),
                   weather=dict(
                       temp_c=current.get('temp_c', 0.0),
                       temp_feelslike_c=current.get('feelslike_c', 0.0),
                       wind_kph=current.get('wind_kph', 0.0),
                       wind_degree=current.get('wind_degree', 0),
                       wind_dir=current.get('wind_dir', ''),
                       pressure_mb=pressure_mb,
                       pressure_mmhg=pressure_mmhg,
                       precip_mm=current.get('precip_mm', 0.0),
                       humidity=current.get('humidity', 0),
                       gust_kph=current.get('gust_kph', 0.0),
                       datetime=current.get('last_updated', datetime.now()))
                   )
        return dict(weather=new)
