import copy
import jsonschema


class ValidationError(Exception):
    """ Обработка исключений ValidationError """
    pass


class JSONSchema:
    """ Проверка данных в соответствии с Draft 4 JSON Schema """

    schema = {}

    def __init__(self):
        format_checker = jsonschema.FormatChecker()
        self.validator = jsonschema.Draft4Validator(
            self.schema, format_checker=format_checker
        )

    def validate(self, data):
        """
        Проверка данных в соответствии со схемой.

        :param data: данные для проверки
        :returns: проверенные данные
        :raises ValidationError: если данные не вылидны
        """
        appstruct = copy.deepcopy(data)

        errors = list(self.validator.iter_errors(appstruct))
        if errors:
            msg = ", ".join([_format_jsonschema_error(e) for e in errors])
            raise ValidationError(msg)
        return appstruct


def _format_jsonschema_error(error):
    """ Форматирование
        :py:class:`jsonschema.ValidationError` как строка """

    if error.path:
        dotted_path = ".".join([str(c) for c in error.path])
        return f"{dotted_path}: {error.message}"
    return error.message
