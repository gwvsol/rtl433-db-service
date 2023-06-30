from .base import JSONSchema
# from rtl433db.log import logging as log


class SensorSchemaBase(JSONSchema):
    """ Базовый валидатор данных Sensor Schema """

    schema = {
        "type": "object",
        "properties": {
            "location": {"type": "object",
                         "properties": {
                             "model": {"type": "string"},
                             "id": {"type": "number"},
                             "time": {"type": "string",
                                      "format": "date-time"}
                            }
                         }
            }
        }


class SensorSchema:
    """ Валидатор данных Sensor Schema """

    def __init__(self):
        self.structure = SensorSchemaBase()

    def validate(self, data) -> dict:
        """ Валидатор и формирование выходных данных """
        appstruct = self.structure.validate(data)
        return self.create_fields(appstruct)

    def create_fields(self, appstruct: dict) -> dict:
        """ Создание структуры данных """

        temp_F = appstruct.get('temperature_F', None)
        temp_C = appstruct.get('temperature_C', None)
        humidity = appstruct.get('humidity', None)

        if isinstance(temp_C, (int, float)):
            temp_C = temp_C
        elif isinstance(temp_F, (int, float)):
            #  Fahrenheit => Celsius
            temp_C = round((temp_F - 32) / 1.8, 2)
        else:
            temp_C = None

        new = dict(model=appstruct.get('model', ''),
                   datetime=self.structure.to_utc(
                           appstruct.get('time', None)),
                   sensor_id=appstruct.get('id', ''),
                   data=dict(temperature=temp_C),
                   )

        if humidity:
            new.get('data').update(humidity=humidity)

        return dict(sensor=new)
