from datetime import datetime

from .base import JSONSchema


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

        new = dict(model=appstruct.get('model', ''),
                   sensor=dict(
                       model=appstruct.get('model', ''),
                       sensor_id=appstruct.get('id', ''),
                       datetime=appstruct.get('time', datetime.now())),
                   sensor_data=dict(
                       temperature=appstruct.get('temperature_C', 0.0),
                       datetime=appstruct.get('time', datetime.now()))
                   )
        return dict(sensor=new)
